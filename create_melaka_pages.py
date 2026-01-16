#!/usr/bin/env python3
"""
Script to create Melaka location pages based on index.html
Run this script from the project root directory:
    python create_melaka_pages.py
"""

import os

# Locations for Melaka
locations = [
    ('melaka', 'Melaka'),
    ('melaka-tengah', 'Melaka Tengah'),
    ('alor-gajah', 'Alor Gajah'),
    ('jasin', 'Jasin'),
    ('ayer-keroh', 'Ayer Keroh'),
    ('masjid-tanah', 'Masjid Tanah'),
    ('bukit-katil', 'Bukit Katil'),
    ('krubong', 'Krubong'),
    ('bukit-rambai', 'Bukit Rambai'),
    ('tanjung-kling', 'Tanjung Kling'),
    ('bukit-baru', 'Bukit Baru'),
    ('klebang', 'Klebang'),
]

# Read original file
with open('index.html', 'r', encoding='utf-8') as f:
    original = f.read()

# Create locations folder if it doesn't exist
os.makedirs('locations', exist_ok=True)

for slug, name in locations:
    content = original

    # Change title
    content = content.replace(
        '<title>Sewa Mesin Oksigen Malaysia | Portable Oxygen Concentrator Rental & Sale</title>',
        f'<title>Sewa Mesin Oksigen {name} | Portable Oxygen Concentrator Rental & Sale</title>'
    )

    # Change meta title
    content = content.replace(
        '<meta name="title" content="Sewa Mesin Oksigen Malaysia | Portable Oxygen Concentrator Rental & Sale">',
        f'<meta name="title" content="Sewa Mesin Oksigen {name} | Portable Oxygen Concentrator Rental & Sale">'
    )

    # Change meta description
    content = content.replace(
        '<meta name="description" content="Sewa atau beli mesin oksigen mudah alih di Malaysia. Penghantaran percuma ke seluruh Semenanjung. Harga berpatutan mulai RM150/minggu. Hubungi 03-7890 1234.">',
        f'<meta name="description" content="Sewa atau beli mesin oksigen mudah alih di {name}. Penghantaran percuma, harga berpatutan mulai RM150/minggu. Hubungi 011-2868 6592.">'
    )

    # Change canonical URL
    content = content.replace(
        '<link rel="canonical" href="https://oxygencare.my/">',
        f'<link rel="canonical" href="https://oxygencare.my/locations/{slug}/">'
    )

    # Change H1 heading
    content = content.replace(
        'Sewa & Beli <span class="text-green">Mesin<br>Oksigen</span> perubatan<br>Malaysia',
        f'Sewa & Beli <span class="text-green">Mesin<br>Oksigen</span> perubatan<br>{name}'
    )

    # Write file
    filepath = f'locations/{slug}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Created: {filepath}')

print('\nDone! All Melaka location pages have been created.')
