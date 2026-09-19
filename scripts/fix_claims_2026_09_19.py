#!/usr/bin/env python3
"""One-off claim fix, 2026-09-19. Brings renthospitalbed.my in line with the
canonical claim registry (katil-hospital-bed.my data/official-facts.json).

Principles:
- Delivery positioning is QUALIFIED, not deleted: every fixed time becomes
  "seawal <time>" plus the written-confirmation qualifier. Sub-3-hour promises
  become "seawal 3 jam" (3 hours is the fastest the registry allows, for
  selected Klang Valley orders confirmed in writing).
- Setup, delivery, mattress and service are never described as universally
  free or included; the written quotation controls.
- Prices follow the registry: rent 150/250/450, buy 799/1,349/2,799/5,500.
- MDA registration stays (owner confirmed 2026-09-19 every model is
  registered); "KKM approved"/"certified" wording goes.
- Unverified counts, ratings and instalment terms are removed.

Idempotent: re-running changes nothing. Re-check with scripts/audit_claims.py.
"""
from __future__ import annotations
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

DT = r"(?P<dt>\d+(?:\s*[-–]\s*\d+)?\s*(?:[Jj]am|[Hh]ari))"

def seawal(dt: str, word: str = "seawal") -> str:
    dt = re.sub(r"\s+", " ", dt).strip().lower()
    m = re.match(r"(\d+)(?:\s*[-–]\s*(\d+))?\s*(jam|hari)", dt)
    if not m:
        return f"{word} {dt}"
    a, unit = int(m.group(1)), m.group(3)
    if unit == "jam" and a < 3:
        a = 3
    return f"{word} {a} {unit}"

def cap(s: str) -> str:
    return s[:1].upper() + s[1:]

# ---------------------------------------------------------------- regex rules
# (pattern, replacement-or-callable). Applied to every HTML file, in order.
R: list[tuple[str, object]] = [
    # botched earlier edits: "224 Jam", "2224 Jam"
    (r"(?<![0-9])2{1,3}(24 [Jj]am)", r"\1"),

    # titles
    (r"(\| RM150/Bulan), Penghantaran \d+(?:\s*-\s*\d+)? (?:[Jj]am|[Hh]ari)", r"\1, Tanpa Deposit"),
    (r"(\| RM150/Bulan), Setup Percuma", r"\1, Tanpa Deposit"),
    (r"\| Hantar Same-Day JB", "| Tanpa Deposit, Hantar Pantas"),

    # meta / JSON-LD descriptions
    (r"Penghantaran " + DT + r", tanpa deposit, (?:pemasangan|servis) percuma\.",
     lambda m: f"Tanpa deposit, bayar selepas katil dipasang. Penghantaran {seawal(m['dt'])} (disahkan bertulis)."),
    (r"Tanpa deposit, penghantaran " + DT + r", servis percuma\.",
     lambda m: f"Tanpa deposit, bayar selepas katil dipasang. Penghantaran {seawal(m['dt'])} (disahkan bertulis)."),
    (r"(dari RM150/bulan)\. Penghantaran " + DT + r"\.",
     lambda m: f"{m[1]}. Penghantaran {seawal(m['dt'])} (disahkan bertulis)."),
    (r"Penghantaran ke (?P<t>[^\"<]+?) dalam masa " + DT + r" selepas pengesahan order\.",
     lambda m: f"Penghantaran ke {m['t']} boleh {seawal(m['dt'])} selepas pengesahan order, tertakluk stok dan lokasi; masa sebenar disahkan secara bertulis."),

    # hero subtitle
    (r"Tanpa Deposit\. Penghantaran " + DT + r" ke Seluruh (?P<t>[^.<]+?)\. Pemasangan & Servis Percuma\.",
     lambda m: f"Tanpa Deposit. Penghantaran {seawal(m['dt'])} ke {m['t']} (disahkan bertulis). Bayar selepas katil dipasang."),

    # headings that are only a time promise
    (r"(<h[1-6][^>]*>\s*(?:<em>)?)Penghantaran \d+(?:\s*-\s*\d+)? (?:[Jj]am|[Hh]ari)((?:</em>)?\s*</h[1-6]>)",
     r"\1Penghantaran Pantas\2"),

    # feature card / why-us / area header / FAQ body / CTA
    (r"<p>Penghantaran pantas ke seluruh (?P<t>[^<]+?) dalam " + DT + r"</p>",
     lambda m: f"<p>{cap(seawal(m['dt']))} ke {m['t']} — masa sebenar disahkan secara bertulis</p>"),
    (r"untuk penghantaran <strong>dalam masa " + DT + r"</strong> ke rumah anda(?P<t> di [^.<]+?)?\.",
     lambda m: f"untuk penghantaran <strong>{seawal(m['dt'])}</strong> ke rumah anda{m['t'] or ''} (masa disahkan secara bertulis)."),
    (r"Penghantaran " + DT + r" ke semua kawasan berikut",
     lambda m: f"Penghantaran ke semua kawasan berikut — {seawal(m['dt'])}, masa disahkan secara bertulis"),
    (r"Untuk kawasan (?P<t>[^,<]+?), katil sampai dalam masa " + DT + r" selepas order",
     lambda m: f"Untuk kawasan {m['t']}, katil boleh sampai {seawal(m['dt'])} selepas order disahkan — masa sebenar disahkan secara bertulis"),
    (r"penghantaran dalam masa <strong>" + DT + r"</strong> selepas pengesahan order\. Untuk kawasan luar bandar mungkin ambil masa sedikit lebih lama\.",
     lambda m: f"penghantaran boleh <strong>{seawal(m['dt'])}</strong> selepas pengesahan order, tertakluk stok dan lokasi — masa sebenar disahkan secara bertulis untuk setiap tempahan. Kawasan luar bandar mungkin mengambil masa lebih lama."),
    (r"Penghantaran: (?:Same day|Hari yang sama)(?! \()", "Penghantaran: seawal hari yang sama (disahkan bertulis)"),
    (r"Penghantaran: (?P<dt>\d+(?:\s*-\s*\d+)?\s*(?:jam|hari))(?! \()",
     lambda m: f"Penghantaran: {seawal(m['dt'])} (disahkan bertulis)"),
    (r"(?:Kami Hantar|Katil Hospital Sampai) Hari Ini\.", "Semak Slot Penghantaran Hari Ini."),

    # setup / service / mattress / delivery "free" or "included"
    (r">\s*Pemasangan Percuma\s*<", ">Pemasangan &amp; Demo<"),
    (r"Pemasangan dan Latihan Percuma", "Pemasangan dan Latihan"),
    (r"Demonstrasi dan latihan penggunaan katil hospital secara percuma kepada pengguna dan penjaga",
     "Demonstrasi dan latihan penggunaan katil hospital kepada pengguna dan penjaga semasa pemasangan"),
    (r"<p>Pasang & ajar guna di rumah anda tanpa caj</p>",
     "<p>Pasukan kami pasang &amp; ajar guna di rumah anda — terma dalam sebut harga bertulis</p>"),
    (r"Kami tolong pasang dan ajar tanpa caj tambahan\.",
     "Kami tolong pasang dan ajar cara guna. Sebarang caj dinyatakan dalam sebut harga bertulis."),
    (r"Pasukan kami pasang dan ajar guna di rumah anda tanpa caj tambahan",
     "Pasukan kami pasang dan ajar guna di rumah anda — sebarang caj dinyatakan dalam sebut harga bertulis"),
    (r"<strong>PERCUMA:</strong> Setup & pemasangan", "<strong>Disediakan:</strong> Setup &amp; pemasangan (ikut sebut harga)"),
    (r"<strong>PERCUMA:</strong> Tunjuk ajar cara penggunaan", "<strong>Disediakan:</strong> Tunjuk ajar cara penggunaan"),
    (r"<strong>PERCUMA:</strong> Servis & repair", "<strong>Sokongan:</strong> Servis &amp; repair semasa sewa (ikut terma)"),
    (r"<strong>PERCUMA:</strong> Pemasangan & demo di rumah", "<strong>Disediakan:</strong> Pemasangan &amp; demo di rumah (ikut sebut harga)"),
    (r'alt="Pemasangan katil hospital percuma"', 'alt="Pemasangan katil hospital di rumah"'),
    (r'alt="Pemasangan percuma katil hospital di', 'alt="Pemasangan katil hospital di'),
    (r">\s*Servis Percuma\s*<", ">Servis Semasa Sewa<"),
    (r"Penyelenggaraan dan repair percuma sepanjang tempoh sewa",
     "Penyelenggaraan dan pembaikan semasa sewa mengikut terma sebut harga bertulis"),
    (r"untuk repair percuma sepanjang sewa", "untuk servis semasa sewa, mengikut terma sebut harga"),
    (r"Harga termasuk penghantaran, pemasangan dan tilam\.",
     "Tilam, penghantaran dan pemasangan hanya termasuk jika disenaraikan dalam sebut harga bertulis."),
    (r"Sewa termasuk: katil hospital, tilam, rel sisi, penghantaran, pemasangan, demonstrasi penggunaan, dan servis/repair percuma sepanjang tempoh sewa\.",
     "Harga sewa adalah untuk katil hospital yang dinamakan (termasuk rel sisi). Tilam, penghantaran, pemasangan dan aksesori lain hanya termasuk jika disenaraikan dalam sebut harga bertulis. Caj penghantaran sehala dalam Malaysia sehingga RM280, bergantung pada alamat."),
    (r"(?:Pasang percuma, tanpa deposit|Tanpa deposit, pasang percuma|Pemasangan percuma, tanpa deposit|Tanpa deposit, pemasangan percuma)\.",
     "Tanpa deposit, bayar selepas katil dipasang."),
    (r"Pemasangan percuma oleh pasukan kami", "Pemasangan oleh pasukan kami"),
    (r"secara percuma semasa (penghantaran|pemasangan)", r"semasa \1"),
    (r"Promosi Mac - Sewa katil hospital dari RM150/bulan, pemasangan PERCUMA \(percuma set IV drip dan meja makan\)!",
     "Sewa katil hospital dari RM150/bulan — tanpa deposit, bayar selepas katil dipasang."),
    (r"March Promo - Rent hospital bed from RM150/month, FREE installation \(free IV drip set and dining table\)!",
     "Rent a hospital bed from RM150/month — no deposit, pay after the bed is installed."),
    (r"三月促销 - 医院床出租从RM150/月起，免费安装（赠送IV支架和餐桌）！",
     "医院床出租每月RM150起——无需押金，床送达安装后才付款。"),
    (r"மார்ச் பிரமோஷன் - மருத்துவமனை கட்டில் வாடகை RM150/மாதம் முதல், இலவச நிறுவல் \(இலவச IV drip செட் மற்றும் சாப்பாட்டு மேசை\)!",
     "மருத்துவமனை கட்டில் வாடகை RM150/மாதம் முதல் — டெபாசிட் இல்லை, கட்டில் நிறுவிய பின் பணம் செலுத்துங்கள்."),

    (r"(<strong>)?Pemasangan PERCUMA(</strong>)? - Pasukan kami akan datang pasang katil di rumah anda tanpa sebarang caj tambahan\.",
     r"\1Pemasangan\2 - Pasukan kami akan datang pasang katil di rumah anda; sebarang caj dinyatakan dalam sebut harga bertulis."),
    (r"Pemasangan percuma, tanpa deposit sejak 2016\.", "Tanpa deposit, bayar selepas dipasang — sejak 2016."),
    (r"Semuanya termasuk dalam perkhidmatan pemasangan percuma\.", "Semuanya sebahagian daripada perkhidmatan pemasangan kami."),
    (r"dan pemasangan percuma, kami membantu", "dan pemasangan di rumah, kami membantu"),
    (r"\. Pemasangan percuma\. Penghantaran ke seluruh Malaysia\.", ". Tanpa deposit. Penghantaran ke seluruh Malaysia."),
    (r"Pemasangan percuma, penghantaran ke seluruh Malaysia", "Tanpa deposit, penghantaran ke seluruh Malaysia"),
    (r"Kami hantar & pasang PERCUMA di rumah anda", "Kami hantar &amp; pasang di rumah anda"),
    (r"\b([Pp]emasangan|[Pp]asang) (?:percuma|PERCUMA)\b", r"\1"),
    (r"Penghantaran: \d+ minit(?: dari gudang)?", "Penghantaran: seawal 3 jam (disahkan bertulis)"),
    (r'(<span class="google-rating-num"[^>]*>)4\.9(</span>)', r"\1\2"),
    (r'(<span class="google-ulasan"[^>]*>)500\+ ulasan(</span>)', r"\1Ulasan Google\2"),
    (r"KKM &(?:amp;)? MDA-licensed\.", "MDA-registered."),
    (r">\s*Lulus KKM\s*<", ">Berdaftar MDA<"),

    # prices
    (r"Katil 3 fungsi dari RM200/bulan", "Katil 3 fungsi dari RM250/bulan"),
    (r'"priceRange": "RM150 - RM350/bulan"', '"priceRange": "RM150 - RM450/bulan"'),
    (r'"priceRange": "RM150 - RM(?:5000|8000)"', '"priceRange": "RM150 - RM5500"'),
    (r"Price Range: (</strong>\s*)?RM150 - RM350/month", r"Price Range: \1RM150 - RM450/month"),

    # MDA / KKM wording (registration stays, "approved/certified by KKM" goes)
    (r"Diluluskan Oleh", "Berdaftar Dengan"),
    (r"Lulus KKM &(?:amp;)? MDA\.", "Berdaftar dengan MDA."),
    (r"LULUS KKM &(?:amp;)? PIHAK BERKUASA<br>PERANTI PERUBATAN", "BERDAFTAR DENGAN PIHAK BERKUASA<br>PERANTI PERUBATAN (MDA)"),
    (r"Berlesen MDA dan berdaftar KKM", "Berlesen &amp; berdaftar dengan MDA"),
    (r'"name": "Lulus KKM(?: \(Kementerian Kesihatan Malaysia\))?"', '"name": "Kelulusan Iklan MDA (MDAMD 0127/2025)"'),
    (r'"name": "Approved by KKM \(Ministry of Health Malaysia\)"', '"name": "MDA advertising approval (MDAMD 0127/2025)"'),
    (r'"name": "通过KKM认证（马来西亚卫生部）"', '"name": "MDA广告批准（MDAMD 0127/2025）"'),
    (r'"name": "KKM \(மலேசிய சுகாதார அமைச்சகம்\) அங்கீகரிக்கப்பட்டது"', '"name": "MDA விளம்பர ஒப்புதல் (MDAMD 0127/2025)"'),
    (r"Trusted Seller, Approved By", "Trusted Seller, Registered With"),
    (r">\s*Certified Products\s*<", ">MDA-Registered Products<"),
    (r">\s*认证产品\s*<", ">MDA注册产品<"),
    (r"信赖与认证", "信赖与注册"),
    (r"Trust &(?:amp;)? Certification", "Trust &amp; Registration"),
    (r"Kepercayaan &(?:amp;)? Pensijilan", "Kepercayaan &amp; Pendaftaran"),

    # unverified counts / ratings
    (r"(\])\s*,\s*\"award\": \"[^\"]*\"(\s*\})", r"\1\2"),
    (r'<div class="stat-number">500\+</div>(\s*)<div class="stat-label">[^<]*</div>',
     r'<div class="stat-number">2016</div>\1<div class="stat-label">STAT_FOUNDED</div>'),
    (r'<div class="stat-number">10\+</div>(\s*)<div class="stat-label">[^<]*</div>',
     r'<div class="stat-number">MDA</div>\1<div class="stat-label">STAT_MDA</div>'),
    (r'<div class="stat-number">4\.9★</div>(\s*)<div class="stat-label">[^<]*</div>',
     r'<div class="stat-number">RM0</div>\1<div class="stat-label">STAT_DEPOSIT</div>'),
    (r">\s*10\+ Tahun Pengalaman\s*<", ">Berkhidmat Sejak 2016<"),
    (r">\s*10\+ Years Experience\s*<", ">Serving Since 2016<"),
    (r">\s*10\+年经验\s*<", ">自2016年起服务<"),
    (r">\s*10\+ ஆண்டுகள் அனுபவம்\s*<", ">2016 முதல் சேவை<"),
    (r"\(80% pelanggan pilih ini\)", "(pilihan kebanyakan pelanggan)"),
    (r"80% pelanggan kami memilih katil 2 fungsi", "Kebanyakan pelanggan kami memilih katil 2 fungsi"),
    (r"\(80% of customers choose this\)", "(chosen by most customers)"),
    (r"（80%客户选择此款）", "（大多数客户的选择）"),

    # instalments: exist, signed after delivery; no published rate/term
    (r'("paymentAccepted": "[^"]*), (?:Ansuran 0%|0% Instalment|0%分期付款|0% தவணை)"',
     lambda m: m[1] + ", " + {"Ansuran 0%": "Ansuran", "0% Instalment": "Instalment", "0%分期付款": "分期付款", "0% தவணை": "தவணை"}[m[0].split(", ")[-1].rstrip('"')] + '"'),

    # schema delivery lead time (an unqualified promise in structured data)
    (r',\s*"deliveryLeadTime": \{[^}]*\}', ""),
]

STAT_LABELS = {  # per-language labels for the replaced trust stats
    "ms": {"STAT_FOUNDED": "Tahun Ditubuhkan", "STAT_MDA": "Katil Berdaftar", "STAT_DEPOSIT": "Deposit Sewa"},
    "en": {"STAT_FOUNDED": "Established", "STAT_MDA": "Registered Beds", "STAT_DEPOSIT": "Rental Deposit"},
    "zh": {"STAT_FOUNDED": "成立年份", "STAT_MDA": "注册病床", "STAT_DEPOSIT": "租赁押金"},
    "ta": {"STAT_FOUNDED": "நிறுவப்பட்டது", "STAT_MDA": "பதிவு செய்யப்பட்ட கட்டில்கள்", "STAT_DEPOSIT": "வாடகை டெபாசிட்"},
}

def lang_of(rel: str) -> str:
    return rel.split("/")[0] if rel.split("/")[0] in ("en", "zh", "ta") else "ms"

# ------------------------------------------------------- exact, per-file text
from fix_claims_exact import EXACT  # noqa: E402  (kept separate: long, per-language)


# ------------------------------------------- generic qualifier (long tail)
import audit_claims as A  # noqa: E402

QUALIFIER = {
    "ms": (" — masa sebenar disahkan secara bertulis", " (disahkan bertulis)"),
    "en": (" — actual time confirmed in writing", " (confirmed in writing)"),
    "zh": ("（实际时间以书面确认为准）", "（以书面确认为准）"),
    "ta": (" (உண்மையான நேரம் எழுத்துப்பூர்வமாக உறுதிப்படுத்தப்படும்)", " (எழுத்துப்பூர்வ உறுதிப்படுத்தலுடன்)"),
}
ENGLISH_FILES = ("en/", "blog/best-hospital-bed-rental-malaysia/")

def seg_lang(rel: str, seg: str) -> str:
    if re.search(r"[一-鿿]", seg):
        return "zh"
    if re.search(r"[஀-௿]", seg):
        return "ta"
    return "en" if rel.startswith(ENGLISH_FILES) else "ms"

def raw_pattern(seg: str) -> str:
    """Regex for a published-text segment inside raw HTML: tags and whitespace
    may sit between words, and "&" may be written as "&amp;"."""
    parts = ["(?:&|&amp;)".join(re.escape(x) for x in tok.split("&")) for tok in seg.split()]
    return r"(?:\s|<[^>]+>)*".join(parts)

def qualify_remaining(rel: str, html_src: str) -> str:
    """Append the written-confirmation qualifier to every remaining delivery-time
    promise the audit still flags (state pages and blog prose)."""
    text = A.published_text(html_src)
    for seg in dict.fromkeys(A.segments(text)):
        if not A.is_unqualified_delivery(seg) or seg.rstrip().endswith("?"):
            continue
        lang = seg_lang(rel, seg)
        with_dot, bare = QUALIFIER[lang]
        for m in reversed(list(re.finditer(raw_pattern(seg), html_src))):
            span = html_src[m.start():m.end()]
            if span.endswith((".", "。")):
                new = span[:-1] + with_dot + span[-1]
            else:
                new = span + bare
            html_src = html_src[:m.start()] + new + html_src[m.end():]
    return html_src

def main() -> int:
    files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    changed = 0
    missing = []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        src = f.read_text(encoding="utf-8")
        out = src
        for scope in (rel, "*"):
            for old, new in EXACT.get(scope, []):
                if old.startswith("re:"):
                    out, n = re.subn(old[3:], new, out)
                elif old in out:
                    out, n = out.replace(old, new), 1
                else:
                    n = 0
                if not n and scope != "*" and new not in out:
                    missing.append((rel, old[:90]))
        for pat, repl in R:
            out = re.sub(pat, repl, out)
        for k, v in STAT_LABELS[lang_of(rel)].items():
            out = out.replace(k, v)
        out = qualify_remaining(rel, out)
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, flags=re.S):
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                if json_ok(src, block):
                    print(f"JSON-LD broken by fix in {rel}: {e}")
                    return 2
        if out != src:
            f.write_text(out, encoding="utf-8")
            changed += 1
    print(f"{changed} files changed")
    for rel, old in missing:
        print(f"  exact string not found: {rel}: {old}")
    return 0

def json_ok(src: str, _block: str) -> bool:
    """True if every JSON-LD block in the original parsed (so a failure now is ours)."""
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, flags=re.S):
        try:
            json.loads(b)
        except json.JSONDecodeError:
            return False
    return True

if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    sys.exit(main())
