#!/usr/bin/env python3
"""
Script to update all location pages with new SEO-optimized meta tags
for hospital bed rental branding.
"""

import os
import re
from pathlib import Path

# Define the locations folder
LOCATIONS_DIR = Path(__file__).parent / "locations"

# KL/Selangor areas - 4 Jam delivery
KL_SELANGOR_AREAS = {
    'ampang', 'bangi', 'bangsar', 'banting', 'batu', 'bukit-bintang', 'cheras',
    'cyberjaya', 'damansara', 'gombak', 'kajang', 'kepong', 'klang', 'kuala-lumpur',
    'kuala-selangor', 'mont-kiara', 'petaling-jaya', 'puchong', 'putrajaya', 'rawang',
    'sabak-bernam', 'segambut', 'selangor', 'selayang', 'sentul', 'sepang', 'serdang',
    'setapak', 'shah-alam', 'sri-petaling', 'subang-jaya', 'titiwangsa', 'wangsa-maju'
}

# East Malaysia (Sabah/Sarawak) - 2-3 Hari delivery
EAST_MALAYSIA_AREAS = {
    'sabah', 'sarawak', 'kota-kinabalu', 'kuching', 'miri', 'sibu', 'bintulu',
    'sandakan', 'tawau', 'lahad-datu', 'keningau', 'semporna', 'sri-aman', 'kapit'
}

def get_delivery_time(location_slug):
    """Determine delivery time based on location."""
    if location_slug in KL_SELANGOR_AREAS:
        return "4 Jam"
    elif location_slug in EAST_MALAYSIA_AREAS:
        return "2-3 Hari"
    else:
        return "24 Jam"

def format_location_name(slug):
    """Convert slug to proper location name."""
    # Handle special cases
    special_names = {
        'george-town': 'George Town',
        'kota-kinabalu': 'Kota Kinabalu',
        'kota-bharu': 'Kota Bharu',
        'kota-tinggi': 'Kota Tinggi',
        'kuala-lumpur': 'Kuala Lumpur',
        'kuala-terengganu': 'Kuala Terengganu',
        'kuala-selangor': 'Kuala Selangor',
        'kuala-kedah': 'Kuala Kedah',
        'kuala-pilah': 'Kuala Pilah',
        'kuala-krai': 'Kuala Krai',
        'kuala-nerus': 'Kuala Nerus',
        'johor-bahru': 'Johor Bahru',
        'shah-alam': 'Shah Alam',
        'petaling-jaya': 'Petaling Jaya',
        'subang-jaya': 'Subang Jaya',
        'iskandar-puteri': 'Iskandar Puteri',
        'pasir-gudang': 'Pasir Gudang',
        'pasir-mas': 'Pasir Mas',
        'pasir-puteh': 'Pasir Puteh',
        'batu-pahat': 'Batu Pahat',
        'port-dickson': 'Port Dickson',
        'bukit-bintang': 'Bukit Bintang',
        'bukit-mertajam': 'Bukit Mertajam',
        'mont-kiara': 'Mont Kiara',
        'air-itam': 'Air Itam',
        'bayan-lepas': 'Bayan Lepas',
        'nibong-tebal': 'Nibong Tebal',
        'kepala-batas': 'Kepala Batas',
        'balik-pulau': 'Balik Pulau',
        'tanjung-bungah': 'Tanjung Bungah',
        'tasek-gelugor': 'Tasek Gelugor',
        'seberang-perai': 'Seberang Perai',
        'sungai-petani': 'Sungai Petani',
        'padang-serai': 'Padang Serai',
        'lahad-datu': 'Lahad Datu',
        'sri-aman': 'Sri Aman',
        'sri-petaling': 'Sri Petaling',
        'cameron-highlands': 'Cameron Highlands',
        'gua-musang': 'Gua Musang',
        'tanah-merah': 'Tanah Merah',
        'rantau-panjang': 'Rantau Panjang',
        'negeri-sembilan': 'Negeri Sembilan',
        'pulau-pinang': 'Pulau Pinang',
        'hulu-terengganu': 'Hulu Terengganu',
        'wangsa-maju': 'Wangsa Maju',
        'alor-setar': 'Alor Setar',
        'sabak-bernam': 'Sabak Bernam',
    }

    if slug in special_names:
        return special_names[slug]

    # Default: capitalize each word
    return ' '.join(word.capitalize() for word in slug.split('-'))

def update_location_page(file_path):
    """Update a single location page with new SEO meta tags."""
    # Get location slug from filename
    slug = file_path.stem
    location_name = format_location_name(slug)
    delivery_time = get_delivery_time(slug)

    # New SEO content
    new_title = f"Sewa Katil Hospital {location_name} | Penghantaran {delivery_time}, Tanpa Deposit (2026)"
    new_description = f"Jaga pesakit di rumah di {location_name} jadi lebih mudah. Sewa katil hospital dari RM150/bulan. Penghantaran {delivery_time}, tanpa deposit, servis percuma. Hubungi 011-2868 6592."

    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Update <title> tag
    content = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{new_title}</title>',
        content
    )

    # Update <meta name="title"> tag
    content = re.sub(
        r'<meta name="title" content="[^"]+">',
        f'<meta name="title" content="{new_title}">',
        content
    )

    # Update <meta name="description"> tag
    content = re.sub(
        r'<meta name="description" content="[^"]+">',
        f'<meta name="description" content="{new_description}">',
        content
    )

    # Update all oxygencare.my URLs to sewakatilhospital.my
    content = re.sub(
        r'https://oxygencare\.my',
        'https://sewakatilhospital.my',
        content
    )

    # Update email addresses from oxygencare.my to sewakatilhospital.my
    content = re.sub(
        r'info@oxygencare\.my',
        'info@sewakatilhospital.my',
        content
    )

    # Update any remaining oxygencare.my references
    content = re.sub(
        r'oxygencare\.my',
        'sewakatilhospital.my',
        content
    )

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return original_content != content

def main():
    """Process all location pages."""
    if not LOCATIONS_DIR.exists():
        print(f"Error: Locations directory not found: {LOCATIONS_DIR}")
        return

    html_files = list(LOCATIONS_DIR.glob("*.html"))
    print(f"Found {len(html_files)} location pages to update")

    updated_count = 0
    for file_path in sorted(html_files):
        try:
            if update_location_page(file_path):
                updated_count += 1
                print(f"Updated: {file_path.name}")
            else:
                print(f"No changes: {file_path.name}")
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    print(f"\nCompleted! Updated {updated_count} of {len(html_files)} files.")

if __name__ == "__main__":
    main()
