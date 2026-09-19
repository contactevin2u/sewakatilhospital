#!/usr/bin/env python3
"""2026-09-19 follow-up to fix_claims_2026_09_19.py (idempotent).

1. The "KKM & MDA Icon" image shows the Jata Negara beside the MDA logo, which
   reads as government endorsement. Replace it with a text badge that states the
   actual fact (device registration GA9817222-107721) and links to the MDA record.
2. "Free Installation.webp" was an AI-generated picture with a visible Gemini
   watermark and a filename that advertises free installation. Point every card
   at a real delivery photo instead.
3. Rent-to-own is partial and case by case (owner, 2026-09-19): no page may
   promise that rental payments come off the purchase price in full.

    python scripts/fix_workstream_a_2026_09_19.py
"""
from __future__ import annotations
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

MDA_URL = "https://mdar.mda.gov.my/frontend/web/index.php?id=68014&amp;r=carian%2Fview"
BADGE_TEXT = {
    "ms": "Berdaftar dengan MDA · GA9817222-107721",
    "en": "MDA-registered · GA9817222-107721",
    "zh": "已在 MDA 注册 · GA9817222-107721",
    "ta": "MDA-இல் பதிவுசெய்யப்பட்டது · GA9817222-107721",
}
BADGE_STYLE = ("display:inline-block;padding:6px 10px;border:1px solid #cbd5e1;border-radius:8px;"
               "background:#fff;color:#0f172a;font-size:12px;font-weight:600;line-height:1.3;"
               "text-decoration:none;white-space:nowrap")
EMBLEM_IMG = re.compile(r'<img\s+src="/?images/KKM (?:&|&amp;) MDA Icon\.webp"[^>]*>')

PHOTO = "/images/pemasangan-katil-hospital-rumah.webp"
PHOTO_IMG = re.compile(r'(<img\s+src=")/?images/Free Installation\.webp("[^>]*>)')

RENT_TO_OWN = {
    # homepage FAQ JSON-LD, one per language
    "Kami juga ada plan sewa-beli di mana bayaran sewa boleh ditolak dari harga belian jika anda decide untuk beli kemudian.":
        "Boleh bincang tolak sebahagian bayaran sewa jika beli kemudian — ikut sebut harga bertulis.",
    "We also have a rent-to-own plan where rental payments can be deducted from the purchase price if you decide to buy later.":
        "If you buy later, we can discuss deducting part of the rental already paid — case by case, as set out in a written quotation.",
    "我们还有先租后买计划，如果您后来决定购买，租金可从购买价中扣除。":
        "如果您之后决定购买，可商讨从购买价中扣除部分已付租金——视个案而定，以书面报价为准。",
    "வாடகை-கொள்முதல் திட்டமும் உள்ளது - பின்னர் வாங்க முடிவுசெய்தால் வாடகை கொடுப்பனவை கொள்முதல் விலையிலிருந்து கழிக்கலாம்.":
        "பின்னர் வாங்க முடிவுசெய்தால், செலுத்திய வாடகையின் ஒரு பகுதியைக் கழிப்பது குறித்துப் பேசலாம் — ஒவ்வொரு வழக்கிற்கும் ஏற்ப, எழுத்துப்பூர்வ விலைப்பட்டியலின்படி.",
    # en homepage "why us" card: the body is about instalments, not rental credit
    "Flexible Rent-to-Own Plans": "Flexible Rent or Buy Plans",
    # blog/sewa-vs-beli-katil-hospital: the worked example assumed every ringgit of rent is credited
    "<li><strong>Bila decide untuk beli</strong> - bayaran sewa boleh ditolak dari harga beli</li>":
        "<li><strong>Bila decide untuk beli</strong> - boleh bincang tolak sebahagian bayaran sewa, kes demi kes</li>",
    "<li><strong>Contoh:</strong> Sewa 3 bulan (RM450), kemudian beli = RM799 - RM450 = <strong>RM349 sahaja</strong></li>":
        "<li><strong>Jumlah sebenar</strong> - dinyatakan dalam sebut harga bertulis sebelum anda setuju</li>",
    # blog/best-hospital-bed-rental-malaysia
    "<li>Rent-to-own option available</li>":
        "<li>Part of the rental paid can be discussed towards a purchase (case by case, per written quotation)</li>",
    "some providers like RentHospitalBed.my offer rent-to-own programs where your rental payments go toward the purchase price.":
        "some providers like RentHospitalBed.my can discuss deducting part of the rental already paid if you buy later — case by case, per a written quotation.",
}


def lang_of(html: str) -> str:
    m = re.search(r'<html[^>]*\blang="([a-zA-Z]+)', html)
    code = (m.group(1).lower() if m else "ms")
    return code if code in BADGE_TEXT else "ms"


def badge(lang: str) -> str:
    return (f'<a href="{MDA_URL}" target="_blank" rel="noopener" style="{BADGE_STYLE}">'
            f'{BADGE_TEXT[lang]}</a>')


def fix_photo(m: re.Match) -> str:
    tag = m.group(1) + PHOTO + m.group(2)
    return (tag.replace(" transform: scale(1.5);", "")
               .replace("object-position: center 0%;", "object-position: center 55%;"))


def main() -> None:
    counts = {"emblem": 0, "photo": 0, "rent_to_own": 0, "files": 0}
    for f in sorted(ROOT.rglob("*.html")):
        if ".git" in f.parts:
            continue
        src = f.read_text(encoding="utf-8")
        out, n = EMBLEM_IMG.subn(badge(lang_of(src)), src)
        counts["emblem"] += n
        out, n = PHOTO_IMG.subn(fix_photo, out)
        counts["photo"] += n
        for old, new in RENT_TO_OWN.items():
            if old in out:
                counts["rent_to_own"] += out.count(old)
                out = out.replace(old, new)
        if out != src:
            f.write_text(out, encoding="utf-8", newline="")
            counts["files"] += 1
    print(counts)


if __name__ == "__main__":
    main()
