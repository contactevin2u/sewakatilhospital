"""
Remove all delivery cost (kos penghantaran) mentions from all location pages.
Handles both state pages (16) and city pages (176).
"""
import re
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cleanup_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Remove visible FAQ about delivery cost
    # Pattern: <details class="faq-item">...<h3>Berapa kos penghantaran...</h3>...</details>
    pattern_faq = r'\s*<details class="faq-item">\s*<summary>\s*<h3>Berapa kos penghantaran[^<]*</h3>\s*</summary>\s*<div class="faq-answer">.*?</div>\s*</details>'
    if re.search(pattern_faq, html, re.DOTALL):
        html = re.sub(pattern_faq, '', html, flags=re.DOTALL)
        changes.append("removed delivery cost FAQ")

    # 2. Remove delivery cost FAQ from schema JSON-LD
    # Match the Question object about kos penghantaran (with leading comma if present)
    pattern_schema_faq = r',?\s*\{\s*"@type":\s*"Question",\s*"name":\s*"Berapa kos penghantaran[^"]*"[^}]*"acceptedAnswer":\s*\{[^}]*\}\s*\}'
    if re.search(pattern_schema_faq, html, re.DOTALL):
        html = re.sub(pattern_schema_faq, '', html, flags=re.DOTALL)
        changes.append("removed delivery cost from FAQ schema")

    # 3. Remove "Kos Penghantaran" info card from map section
    # Pattern: the entire div block containing "Kos Penghantaran"
    pattern_kos_card = r'\s*<div style="background: white; padding: 20px; border-radius: 12px;">\s*<div style="display: flex; align-items: center; gap: 12px;">\s*<div style="width: 40px; height: 40px; background: #fef3c7;[^>]*>.*?</svg>\s*</div>\s*<div>\s*<p[^>]*>Kos Penghantaran</p>\s*<p[^>]*>[^<]*</p>\s*</div>\s*</div>\s*</div>'
    if re.search(pattern_kos_card, html, re.DOTALL):
        html = re.sub(pattern_kos_card, '', html, flags=re.DOTALL)
        changes.append("removed Kos Penghantaran from map")

    # 4. Clean delivery cost from pricing FAQ answers
    # Pattern: "dan kos penghantaran (RM... text...)"  or "Kos penghantaran ke ... RM..."
    # Handle: "Harga belum termasuk tilam (RM50/bulan) dan kos penghantaran (RM50 dalam KL)."
    #      -> "Harga belum termasuk tilam (RM50/bulan)."
    pattern_dan_kos = r'\s*dan kos penghantaran \([^)]+\)'
    if re.search(pattern_dan_kos, html):
        html = re.sub(pattern_dan_kos, '', html)
        changes.append("removed 'dan kos penghantaran' from pricing")

    # Handle: "Kos penghantaran ke Johor antara RM80-120." as standalone sentence
    pattern_kos_sentence = r'\s*Kos penghantaran ke [^.]+\.'
    if re.search(pattern_kos_sentence, html):
        html = re.sub(pattern_kos_sentence, '', html)
        changes.append("removed 'Kos penghantaran ke...' sentences")

    # Handle: "Harga termasuk penghantaran, pemasangan dan tilam" -> keep but check for cost amounts
    # Handle: "kos penghantaran yang kompetitif bermula dari RM50" in intro paragraphs
    pattern_kos_kompetitif = r'[^.]*kos penghantaran yang kompetitif[^.]*\.'
    if re.search(pattern_kos_kompetitif, html, re.IGNORECASE):
        html = re.sub(pattern_kos_kompetitif, '', html, flags=re.IGNORECASE)
        changes.append("removed 'kos penghantaran yang kompetitif' from intro")

    # Handle: "Kos penghantaran ke Putrajaya hanya RM50, sama seperti kawasan KL dan Selangor."
    pattern_kos_hanya = r'[^.]*[Kk]os penghantaran ke [^.]+hanya RM\d+[^.]*\.'
    if re.search(pattern_kos_hanya, html):
        html = re.sub(pattern_kos_hanya, '', html)
        changes.append("removed specific delivery cost from intro")

    # Handle schema text with delivery cost: "Kos penghantaran ke..." in schema Answer text
    pattern_schema_kos = r'\s*Kos penghantaran ke [^"]*'
    # Only apply in schema context - be careful not to over-match
    # Actually the FAQ removal above should have caught the schema entry already

    # Handle: "Harga belum termasuk tilam dan kos penghantaran." (without specific amounts)
    pattern_dan_kos_generic = r' dan kos penghantaran'
    if ' dan kos penghantaran' in html:
        html = html.replace(' dan kos penghantaran', '')
        changes.append("removed generic 'dan kos penghantaran'")

    # 5. Clean up FAQ about Langkawi delivery cost mention
    pattern_langkawi_kos = r'Kos penghantaran ke Langkawi sekitar RM\d+-\d+\.\s*'
    if re.search(pattern_langkawi_kos, html):
        html = re.sub(pattern_langkawi_kos, '', html)
        changes.append("removed Langkawi delivery cost")

    # 6. Remove "Tiada caj tersembunyi." only if it follows delivery cost removal (standalone after removal)
    # Don't remove this generally - it's a good trust signal even without delivery cost context

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return changes
    return []


# Process all location pages
files = glob.glob(os.path.join(BASE_DIR, 'katil-hospital-*.html'))
ok = 0
changed = 0
for f in sorted(files):
    name = os.path.basename(f)
    result = cleanup_page(f)
    if result:
        print(f"UPDATED: {name} - {', '.join(result)}")
        changed += 1
    else:
        ok += 1

print(f"\n=== Done: {changed} updated, {ok} unchanged (total {changed + ok} files) ===")
