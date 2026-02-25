"""
Quick fix script: Remove (2026) from all location page titles to keep under 60 chars.
Run with: python fix-titles.py
"""
import glob, re, os

files = glob.glob('katil-hospital-*.html')
print(f'Found {len(files)} location files')

fixed = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    original = content

    # Fix title tags - remove (2026) suffix
    content = re.sub(r'(<title>[^<]*?) \(2026\)(</title>)', r'\1\2', content)
    content = re.sub(r'(<meta name="title" content="[^"]*?) \(2026\)(")', r'\1\2', content)

    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        fixed += 1
        # Show new title
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            t = title_match.group(1)
            print(f'  Fixed: {os.path.basename(f)} -> "{t}" ({len(t)} chars)')

print(f'\nDone! Fixed {fixed} of {len(files)} files.')
