#!/usr/bin/env python3
"""Claim audit for renthospitalbed.my against the canonical claim registry
(katil-hospital-bed.my data/official-facts.json, claimRules).

Counts, per rule, the published claims that break the registry: mustNotPublish
items, delivery-time promises without the written-confirmation qualifier,
non-canonical prices, unverified counts and unverified instalment terms.

    python scripts/audit_claims.py            # summary
    python scripts/audit_claims.py -v         # every hit with its sentence
    python scripts/audit_claims.py --strict   # exit 1 if anything is found

Published text = visible text + meta/alt/title attributes + JSON-LD. Other
<script>, <style> and HTML comments are ignored.
"""
from __future__ import annotations
import collections, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
I = re.I

MUST_NOT = {
    "RM715 Ultra rental": r"RM\s?715",
    "2-year warranty": r"(?:\b2|dua|two)[- ]?(?:tahun|years?)\s*(?:waranti|warranty|jaminan|guarantee)|(?:waranti|warranty|jaminan)\s*(?:2|dua)\s*tahun|2\s*年保修|两年保修|2\s*ஆண்டு\s*உத்தரவாத",
    "98% on time": r"98\s*%",
    "lowest-price claim": r"termurah|harga paling murah|lowest[- ]price|cheapest|price match|最便宜|最低价|மிகக் குறைந்த விலை",
    "10,000+ families/beds": r"10[,.]?000\s*\+?\s*(?:keluarga|families|beds|katil|pelanggan|customers)",
    "mattress included": r"(?:sewa|harga|rental|price)(?:(?!tidak)[^.|]){0,40}(?<!tidak )termasuk[^.|]{0,40}tilam(?![^.|]{0,40}jika disenaraikan)|tilam,? rel sisi,? IV pole[^.|]{0,30}(?:dalam pakej|lengkap)|including (?:a )?(?:medical-grade )?mattress|mattress included|include[^.|]{0,40}mattress(?![^.|]{0,60}only when)|包括床垫|包含床垫|免费床垫",
    "MDA/KKM certified": r"lulus\s+KKM|KKM\s*(?:&|dan|and)?\s*MDA[- ]licensed|berdaftar KKM|approved by KKM|KKM approval|certified by|diluluskan oleh|approved by\b|KKM认证|通过KKM|MDA\s*认证|认证产品|certified products?|KKM[^.|]{0,40}அங்கீகரிக்கப்பட்ட|(?<!\": \")certification\b|pensijilan KKM",
    "Superbrands winner": r"superbrand",
    "universal free delivery": r"penghantaran percuma|free delivery|免费送货|இலவச டெலிவரி|Lembah Klang Percuma|hantar(?:an)? percuma",
    "universal free setup": r"pemasangan percuma|pemasangan\s*(?:<[^>]+>\s*)?PERCUMA|pasang percuma|setup percuma|free (?:professional )?(?:setup|installation)|免费安装|இலவச நிறுவல்|PERCUMA\s*:\s*Setup|pemasangan dan latihan percuma|FREE:\s*Setup|免费：\s*安装|இலவசம்:\s*செட்அப்",
    "Malay placeholder in zh/ta": r"(?:分期|தவணை)\s*[:：]\s*sebut harga bertulis",
}
DT = (r"\b\d+(?:\s*[-–]\s*\d+)?\s*jam\b|\b\d+(?:\s*[-–]\s*\d+)?\s*hari\b(?!\s*seminggu)|same[- ]day|hari yang sama|hari ini|"
      r"\b\d+(?:\s*[-–]\s*\d+)?[- ]hours?\b|\bdeliver[^.|]{0,20}today|"
      r"\d+(?:\s*[-–]\s*\d+)?\s*(?:个)?小时|当天|今天就送|"
      r"\d+(?:\s*[-–]\s*\d+)?\s*மணி\s*நேர")
DELIVERY_CTX = r"hantar|penghantaran|sampai|delivery|deliver|送|到|டெலிவரி|setup|pasang|install|安装|நிறுவ"
EXEMPT_CTX = (r"hotline|kecemasan|emergency|sokongan|support|热线|紧急|அவசர|ஹாட்லைன்|24/7|operasi|beroperasi|"
              r"respons|response|hubungi balik|semak slot|check today|查询今天|சரிபாருங்கள்|online|jam sehari|hours a day|tersedia 24|posisi|position|bedsore|"
              r"kudis|褥疮|தொழில்நுட்ப|technician|servis|service|维修|pengesahan bertulis|minit|minute|分钟")
QUAL = r"bertulis|in writing|written|书面|எழுத்துப்பூர்வ"
# Customer testimonials report one past delivery; they are not an offer.
TESTIMONIALS = ("abang yang pasang", "Delivered the same day, and the installer", "4个小时就送到",
                "当天就送到了", "4 மணி நேரத்தில் Shah Alam வீட்டிற்கு", "Katil sampai dalam 3 jam je")
# The fastest publishable time is 3 hours (selected Klang Valley orders, in writing).
SUB3 = (r"\b[12](?:\s*[-–]\s*\d+)?\s*jam\b|\b\d+(?:\s*[-–]\s*\d+)?\s*minit\b|kurang dari sejam|"
        r"\bwithin [12] hours?|\b[12]-hour|(?<!\d)[12]\s*小时|(?<!\d)[12]\s*மணி")
SUB3_EXEMPT = (r"setup|pasang|pemasangan|install|bacaan|respons|response|dari gudang kami,|jam dari gudang|perjalanan|"
               r"tukar|posisi|position|tersedia|hubungi balik|hubungi anda|hotline|kecemasan|proses \d+ minit")
# Market prices quoted for other sellers' second-hand beds or repairs are not our price.
PRICE_EXEMPT = r"second hand|sekali bayar|nampak murah|tanggung sendiri|TTPM"

def is_unqualified_delivery(seg: str) -> bool:
    return bool(re.search(DT, seg, I) and re.search(DELIVERY_CTX, seg, I) and not re.search(QUAL, seg, I)
                and not re.search(EXEMPT_CTX, seg, I) and not any(t in seg for t in TESTIMONIALS)
                and not re.search(r"memaklumkan|notify", seg, I))
COUNTS = r"\b\d{2,3}[,.]?\d{0,3}\s*\+\s*(?:keluarga|families|family|pelanggan|customers|ulasan|reviews|Malaysian families)|\d+\+\s*(?:家庭|马来西亚家庭|评论)|\d[\d,]*\+\s*(?:குடும்ப|மதிப்புரை|திருப்தியான)|10\+\s*(?:Tahun|Years|年|ஆண்டு)|\b\d{2}%\s*(?:pelanggan|of customers|客户|வாடிக்கையாளர)"
INSTAL = r"0\s*%\s*(?:faedah|interest|instal|分期|利息|தவணை|வட்டி)|ansuran\s*0\s*%|0\s*%\s*(?:sehingga|up to)|tanpa faedah|interest[- ]free|RM\s?(?:33|158|159|249|259)\b"

RENT = [150, 250, 450]
BUY = [799, 1349, 2799, 5500]
ALLOWED = set(RENT + BUY + [199, 399, 280, 50000])
for r in RENT:
    for n in range(1, 25):
        ALLOWED.add(r * n)
        for b in BUY:
            ALLOWED.add(abs(b - r * n))
for n in (1, 3, 6, 9, 12):
    ALLOWED.add(100 * n)  # 3F minus 2F monthly difference x months (comparison tables)
MONTHLY = r"RM\s?(\d[\d,]*)(?:\s*[-–]\s*(?:RM\s?)?(\d[\d,]*))?\s*(?:/\s*|\s+)(?:bulan|sebulan|month|mo|月|மாதம்)"

def published_text(raw: str) -> str:
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S | I)
    raw = re.sub(r"<script(?![^>]*ld\+json).*?</script>", " ", raw, flags=re.S | I)
    attrs = re.findall(r'\b(?:content|alt|title|aria-label)="([^"]*)"', raw)
    raw = re.sub(r"<(?:br|/p|/h\d|/li|/td|/th|/div|/summary|/title|/button|/label)[^>]*>", " | ", raw, flags=I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(raw + " | " + " | ".join(attrs))
    return re.sub(r"\s+", " ", text)

def segments(text: str):
    for s in re.split(r"(?<=[.!?。！？])\s+|\s\|\s|\n|\"\s*,\s*\"|[{}]", text):
        s = s.strip(" |\"")
        if s:
            yield s

def audit(verbose=False):
    files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "TEMPLATE" not in p.name)
    hits = collections.defaultdict(list)
    for f in files:
        text = published_text(f.read_text(encoding="utf-8", errors="ignore"))
        rel = f.relative_to(ROOT).as_posix()
        for name, rx in MUST_NOT.items():
            for m in re.finditer(rx, text, I):
                hits["mustNotPublish: " + name].append((rel, text[max(0, m.start()-60):m.end()+60]))
        for seg in segments(text):
            if is_unqualified_delivery(seg) and not seg.rstrip().endswith("?"):
                hits["unqualified delivery-time promise"].append((rel, seg[:220]))
            if re.search(SUB3, seg, I) and re.search(DELIVERY_CTX, seg, I) and not re.search(SUB3_EXEMPT, seg, I) \
               and not any(t in seg for t in TESTIMONIALS):
                hits["sub-3-hour delivery promise"].append((rel, seg[:220]))
        for m in re.finditer(COUNTS, text, I):
            hits["unverified count"].append((rel, text[max(0, m.start()-50):m.end()+50]))
        for m in re.finditer(INSTAL, text, I):
            hits["unverified instalment term"].append((rel, text[max(0, m.start()-50):m.end()+50]))
        for m in re.finditer(MONTHLY, text, I):
            if re.search(r"perbezaan|difference|beza", text[max(0, m.start()-25):m.start()], I):
                continue  # a price difference, not a monthly rent
            vals = [int(g.replace(",", "")) for g in m.groups() if g]
            if any(v not in RENT for v in vals):
                hits["non-canonical monthly rent"].append((rel, text[max(0, m.start()-60):m.end()+40]))
        for m in re.finditer(r"RM\s?(\d{1,3}(?:,\d{3})+|\d+)(?:\s*[-–]\s*RM?\s?(\d{1,3}(?:,\d{3})+|\d+))?", text):
            if re.search(PRICE_EXEMPT, text[max(0, m.start()-80):m.end()+40], I):
                continue
            for g in m.groups():
                if g and int(g.replace(",", "")) not in ALLOWED:
                    hits["non-canonical price"].append((rel, text[max(0, m.start()-60):m.end()+40]))
                    break
    return files, hits

if __name__ == "__main__":
    verbose = "-v" in sys.argv
    files, hits = audit(verbose)
    print(f"{len(files)} HTML files audited")
    total = 0
    for rule in sorted(hits):
        n = len(hits[rule]); total += n
        fs = len({h[0] for h in hits[rule]})
        print(f"  {n:6}  {rule}  ({fs} files)")
        if verbose:
            seen = collections.Counter(re.sub(r"\s+", " ", h[1]) for h in hits[rule])
            for s, c in seen.most_common(40):
                print(f"          {c:4}x  {s}")
    print(f"  {total:6}  TOTAL")
    if "--strict" in sys.argv and total:
        sys.exit(1)
