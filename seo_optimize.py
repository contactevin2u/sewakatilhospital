#!/usr/bin/env python3
"""
Comprehensive SEO Optimization for Location Pages
- Title optimization (50-60 chars)
- Meta description (150-160 chars)
- H1-H6 structure
- Image alt tags
- Schema markup
- Keywords integration
"""

import os
import re
import json
import glob

# Target Keywords (15 keywords)
TARGET_KEYWORDS = [
    "sewa katil hospital",
    "beli katil hospital",
    "katil hospital",
    "hospital bed rental",
    "katil hospital murah",
    "katil hospital near me",
    "katil hospital 2 fungsi",
    "katil hospital 3 fungsi",
    "katil hospital elektrik",
    "penghantaran katil hospital",
    "katil hospital tanpa deposit",
    "sewa katil hospital harga",
    "katil hospital warga emas",
    "katil hospital pesakit",
    "rent hospital bed"
]

# Location data with SEO-optimized content
LOCATIONS_SEO = {
    # States
    "selangor.html": {
        "name": "Selangor",
        "title": "Sewa Katil Hospital Selangor | RM150/Bulan, Penghantaran 4 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di Selangor dari RM150/bulan. Penghantaran 4 jam ke Shah Alam, PJ, Subang, Klang. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Selangor",
        "keywords": "sewa katil hospital Selangor, beli katil hospital Selangor, katil hospital Shah Alam, katil hospital PJ, katil hospital murah Selangor, hospital bed rental Selangor",
        "areas": ["Shah Alam", "Petaling Jaya", "Subang Jaya", "Klang", "Kajang", "Bangi", "Puchong", "Ampang", "Rawang", "Cyberjaya"],
        "delivery": "4 jam"
    },
    "johor.html": {
        "name": "Johor",
        "title": "Sewa Katil Hospital Johor | RM150/Bulan, Penghantaran 24 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di Johor dari RM150/bulan. Penghantaran 24 jam ke JB, Batu Pahat, Muar, Kluang. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Johor",
        "keywords": "sewa katil hospital Johor, beli katil hospital Johor, katil hospital JB, katil hospital Johor Bahru, katil hospital murah Johor, hospital bed rental Johor",
        "areas": ["Johor Bahru", "Batu Pahat", "Muar", "Kluang", "Pontian", "Segamat", "Kota Tinggi", "Mersing", "Kulai", "Pasir Gudang"],
        "delivery": "24 jam"
    },
    "kuala-lumpur.html": {
        "name": "Kuala Lumpur",
        "title": "Sewa Katil Hospital KL | RM150/Bulan, Penghantaran 4 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di KL dari RM150/bulan. Penghantaran 4 jam ke Cheras, Kepong, Bangsar, Setapak. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Kuala Lumpur",
        "keywords": "sewa katil hospital KL, beli katil hospital Kuala Lumpur, katil hospital Cheras, katil hospital Kepong, katil hospital murah KL, hospital bed rental KL",
        "areas": ["Cheras", "Kepong", "Setapak", "Wangsa Maju", "Bangsar", "Mont Kiara", "Bukit Bintang", "Sentul", "Sri Petaling", "Batu"],
        "delivery": "4 jam"
    },
    "pulau-pinang.html": {
        "name": "Pulau Pinang",
        "title": "Sewa Katil Hospital Pulau Pinang | RM150/Bulan, Penghantaran 24 Jam",
        "meta_desc": "Sewa & beli katil hospital di Pulau Pinang dari RM150/bulan. Penghantaran 24 jam ke George Town, Butterworth, BM. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Pulau Pinang",
        "keywords": "sewa katil hospital Penang, beli katil hospital Pulau Pinang, katil hospital George Town, katil hospital Butterworth, hospital bed rental Penang",
        "areas": ["George Town", "Butterworth", "Bukit Mertajam", "Bayan Lepas", "Air Itam", "Jelutong", "Balik Pulau", "Seberang Perai"],
        "delivery": "24 jam"
    },
    "kedah.html": {
        "name": "Kedah",
        "title": "Sewa Katil Hospital Kedah | RM150/Bulan, Penghantaran 24 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di Kedah dari RM150/bulan. Penghantaran 24 jam ke Alor Setar, Sungai Petani, Kulim. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Kedah",
        "keywords": "sewa katil hospital Kedah, beli katil hospital Kedah, katil hospital Alor Setar, katil hospital Sungai Petani, hospital bed rental Kedah",
        "areas": ["Alor Setar", "Sungai Petani", "Kulim", "Langkawi", "Jitra", "Baling", "Pendang", "Yan", "Gurun"],
        "delivery": "24 jam"
    },
    "perak.html": {
        "name": "Perak",
        "title": "Sewa Katil Hospital Perak | RM150/Bulan, Penghantaran 24 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di Perak dari RM150/bulan. Penghantaran 24 jam ke Ipoh, Taiping, Teluk Intan. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Perak",
        "keywords": "sewa katil hospital Perak, beli katil hospital Perak, katil hospital Ipoh, katil hospital Taiping, hospital bed rental Perak",
        "areas": ["Ipoh", "Taiping", "Teluk Intan", "Sitiawan", "Manjung", "Kuala Kangsar", "Kampar", "Batu Gajah"],
        "delivery": "24 jam"
    },
    "negeri-sembilan.html": {
        "name": "Negeri Sembilan",
        "title": "Sewa Katil Hospital N. Sembilan | RM150/Bulan, Penghantaran 24 Jam",
        "meta_desc": "Sewa & beli katil hospital di N. Sembilan dari RM150/bulan. Penghantaran 24 jam ke Seremban, Nilai, Port Dickson. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Negeri Sembilan",
        "keywords": "sewa katil hospital Negeri Sembilan, beli katil hospital N9, katil hospital Seremban, katil hospital Nilai, hospital bed rental N9",
        "areas": ["Seremban", "Port Dickson", "Nilai", "Senawang", "Bahau", "Kuala Pilah", "Tampin", "Rembau"],
        "delivery": "24 jam"
    },
    "pahang.html": {
        "name": "Pahang",
        "title": "Sewa Katil Hospital Pahang | RM150/Bulan, Penghantaran 24 Jam (2026)",
        "meta_desc": "Sewa & beli katil hospital di Pahang dari RM150/bulan. Penghantaran 24 jam ke Kuantan, Temerloh, Bentong. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Pahang",
        "keywords": "sewa katil hospital Pahang, beli katil hospital Pahang, katil hospital Kuantan, katil hospital Temerloh, hospital bed rental Pahang",
        "areas": ["Kuantan", "Temerloh", "Bentong", "Raub", "Jerantut", "Pekan", "Maran", "Cameron Highlands"],
        "delivery": "24 jam"
    },
    "kelantan.html": {
        "name": "Kelantan",
        "title": "Sewa Katil Hospital Kelantan | RM150/Bulan, Penghantaran 24 Jam",
        "meta_desc": "Sewa & beli katil hospital di Kelantan dari RM150/bulan. Penghantaran 24 jam ke Kota Bharu, Pasir Mas, Tanah Merah. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Kelantan",
        "keywords": "sewa katil hospital Kelantan, beli katil hospital Kelantan, katil hospital Kota Bharu, katil hospital KB, hospital bed rental Kelantan",
        "areas": ["Kota Bharu", "Pasir Mas", "Tanah Merah", "Machang", "Kuala Krai", "Gua Musang", "Bachok", "Tumpat"],
        "delivery": "24 jam"
    },
    "terengganu.html": {
        "name": "Terengganu",
        "title": "Sewa Katil Hospital Terengganu | RM150/Bulan, Penghantaran 24 Jam",
        "meta_desc": "Sewa & beli katil hospital di Terengganu dari RM150/bulan. Penghantaran 24 jam ke Kuala Terengganu, Kemaman, Dungun. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Terengganu",
        "keywords": "sewa katil hospital Terengganu, beli katil hospital Terengganu, katil hospital Kuala Terengganu, hospital bed rental Terengganu",
        "areas": ["Kuala Terengganu", "Kemaman", "Dungun", "Besut", "Marang", "Hulu Terengganu", "Setiu", "Chukai"],
        "delivery": "24 jam"
    },
    "sabah.html": {
        "name": "Sabah",
        "title": "Sewa Katil Hospital Sabah | RM150/Bulan, Penghantaran 1-2 Hari",
        "meta_desc": "Sewa & beli katil hospital di Sabah dari RM150/bulan. Penghantaran 1-2 hari ke Kota Kinabalu, Sandakan, Tawau. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Sabah",
        "keywords": "sewa katil hospital Sabah, beli katil hospital Sabah, katil hospital Kota Kinabalu, katil hospital KK, hospital bed rental Sabah",
        "areas": ["Kota Kinabalu", "Sandakan", "Tawau", "Lahad Datu", "Keningau", "Semporna"],
        "delivery": "1-2 hari"
    },
    "sarawak.html": {
        "name": "Sarawak",
        "title": "Sewa Katil Hospital Sarawak | RM150/Bulan, Penghantaran 1-2 Hari",
        "meta_desc": "Sewa & beli katil hospital di Sarawak dari RM150/bulan. Penghantaran 1-2 hari ke Kuching, Miri, Sibu, Bintulu. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": "Katil Hospital #1 Sarawak",
        "keywords": "sewa katil hospital Sarawak, beli katil hospital Sarawak, katil hospital Kuching, katil hospital Miri, hospital bed rental Sarawak",
        "areas": ["Kuching", "Miri", "Sibu", "Bintulu", "Sri Aman", "Kapit"],
        "delivery": "1-2 hari"
    },
}

# Generate SEO data for cities based on parent state
def generate_city_seo(filename, city_name, parent_state, delivery_time):
    """Generate SEO data for a city"""
    return {
        "name": city_name,
        "title": f"Sewa Katil Hospital {city_name} | RM150/Bulan, Penghantaran {delivery_time.title()}",
        "meta_desc": f"Sewa & beli katil hospital di {city_name} dari RM150/bulan. Penghantaran {delivery_time}, tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "h1": f"Katil Hospital #1 {city_name}",
        "keywords": f"sewa katil hospital {city_name}, beli katil hospital {city_name}, katil hospital murah {city_name}, hospital bed rental {city_name}, katil hospital {parent_state}",
        "delivery": delivery_time
    }

def create_schema_markup(location_name, areas, delivery_time):
    """Create comprehensive schema markup"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "LocalBusiness",
                "@id": f"https://sewakatilhospital.my/locations/{location_name.lower().replace(' ', '-')}/#business",
                "name": f"Sewa Katil Hospital {location_name} - AA Alive Sdn Bhd",
                "description": f"Perkhidmatan sewa dan beli katil hospital di {location_name}. Penghantaran {delivery_time}, tanpa deposit, pemasangan percuma.",
                "url": f"https://sewakatilhospital.my/locations/{location_name.lower().replace(' ', '-')}/",
                "telephone": "+601128799609",
                "priceRange": "RM150 - RM350/bulan",
                "image": "https://sewakatilhospital.my/images/og-image.jpg",
                "address": {
                    "@type": "PostalAddress",
                    "addressRegion": location_name,
                    "addressCountry": "MY"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": "3.1390",
                    "longitude": "101.6869"
                },
                "areaServed": areas[:10],
                "openingHoursSpecification": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "00:00",
                    "closes": "23:59"
                },
                "sameAs": [
                    "https://www.facebook.com/katilhospitalmy",
                    "https://www.instagram.com/katilhospitalmy/"
                ]
            },
            {
                "@type": "Service",
                "serviceType": "Hospital Bed Rental",
                "name": f"Sewa Katil Hospital {location_name}",
                "description": f"Perkhidmatan sewa katil hospital di {location_name} dari RM150/bulan. Penghantaran {delivery_time}.",
                "provider": {
                    "@type": "LocalBusiness",
                    "name": "AA Alive Sdn Bhd"
                },
                "areaServed": {
                    "@type": "Place",
                    "name": location_name
                },
                "offers": {
                    "@type": "Offer",
                    "price": "150",
                    "priceCurrency": "MYR",
                    "priceValidUntil": "2026-12-31",
                    "availability": "https://schema.org/InStock"
                }
            },
            {
                "@type": "Product",
                "name": "Katil Hospital 2 Fungsi Manual",
                "description": "Katil hospital 2 fungsi dengan laras kepala dan kaki. Sesuai untuk pemulihan jangka pendek.",
                "brand": {
                    "@type": "Brand",
                    "name": "AA Alive"
                },
                "offers": {
                    "@type": "AggregateOffer",
                    "lowPrice": "150",
                    "highPrice": "799",
                    "priceCurrency": "MYR",
                    "offerCount": "2",
                    "offers": [
                        {
                            "@type": "Offer",
                            "name": "Sewa",
                            "price": "150",
                            "priceCurrency": "MYR",
                            "priceValidUntil": "2026-12-31"
                        },
                        {
                            "@type": "Offer",
                            "name": "Beli",
                            "price": "799",
                            "priceCurrency": "MYR",
                            "priceValidUntil": "2026-12-31"
                        }
                    ]
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Berapa harga sewa katil hospital di {location_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Harga sewa katil hospital di {location_name} bermula dari RM150/bulan untuk katil 2 fungsi manual. Katil 3 fungsi dari RM200/bulan."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Berapa lama penghantaran ke {location_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Penghantaran ke {location_name} dalam masa {delivery_time} selepas pengesahan order."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Ada deposit untuk sewa?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Tiada deposit diperlukan. Anda hanya perlu bayar sewa bulanan sahaja."
                        }
                    }
                ]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Utama",
                        "item": "https://sewakatilhospital.my/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Lokasi",
                        "item": "https://sewakatilhospital.my/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": location_name,
                        "item": f"https://sewakatilhospital.my/locations/{location_name.lower().replace(' ', '-')}/"
                    }
                ]
            }
        ]
    }
    return json.dumps(schema, indent=4, ensure_ascii=False)

def optimize_location_page(filepath, seo_data):
    """Apply SEO optimizations to a location page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        location_name = seo_data['name']

        # 1. Optimize Title (50-60 chars)
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{seo_data["title"]}</title>',
            content
        )

        # 2. Optimize meta title
        content = re.sub(
            r'<meta name="title" content="[^"]*">',
            f'<meta name="title" content="{seo_data["title"]}">',
            content
        )

        # 3. Optimize Meta Description (150-160 chars)
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{seo_data["meta_desc"]}">',
            content
        )

        # 4. Optimize Keywords
        content = re.sub(
            r'<meta name="keywords" content="[^"]*">',
            f'<meta name="keywords" content="{seo_data["keywords"]}">',
            content
        )

        # 5. Optimize H1 (only one H1 per page)
        content = re.sub(
            r'<h1 id="hero-heading">\s*.*?\s*</h1>',
            f'<h1 id="hero-heading">{seo_data["h1"]}</h1>',
            content,
            flags=re.DOTALL
        )

        # 6. Update OG title and description
        content = re.sub(
            r'<meta property="og:title" content="[^"]*">',
            f'<meta property="og:title" content="{seo_data["title"]}">',
            content
        )
        content = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            f'<meta property="og:description" content="{seo_data["meta_desc"]}">',
            content
        )

        # 7. Update image alt tags with keywords
        content = re.sub(
            r'alt="Katil Hospital [^"]*"',
            f'alt="Katil Hospital {location_name} - Sewa dari RM150/bulan"',
            content
        )
        content = re.sub(
            r'alt="Bukti penghantaran[^"]*"',
            f'alt="Bukti penghantaran katil hospital ke {location_name}"',
            content
        )

        # 8. Update Schema Markup
        areas = seo_data.get('areas', [location_name])
        delivery = seo_data.get('delivery', '24 jam')
        new_schema = create_schema_markup(location_name, areas, delivery)

        # Replace existing schema
        content = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            f'<script type="application/ld+json">\n    {new_schema}\n    </script>',
            content,
            count=1,
            flags=re.DOTALL
        )

        # 9. Add canonical URL if missing
        canonical = f'https://sewakatilhospital.my/locations/{location_name.lower().replace(" ", "-")}/'
        if '<link rel="canonical"' not in content:
            content = content.replace(
                '</head>',
                f'    <link rel="canonical" href="{canonical}">\n</head>'
            )

        # 10. Add sitemap link in footer if missing
        if '/sitemap/' not in content:
            content = content.replace(
                '/terms-conditions/',
                '/terms-conditions/"></a><a href="/sitemap/'
            )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error optimizing {filepath}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locations_dir = os.path.join(base_dir, 'locations')

    print("=" * 60)
    print("SEO Optimization for Location Pages")
    print("=" * 60)

    # Get all location files
    location_files = glob.glob(os.path.join(locations_dir, '*.html'))
    print(f"\nFound {len(location_files)} location files\n")

    optimized = 0
    for filepath in location_files:
        filename = os.path.basename(filepath)

        # Get SEO data
        if filename in LOCATIONS_SEO:
            seo_data = LOCATIONS_SEO[filename]
        else:
            # Generate SEO data for cities not in the main list
            city_name = filename.replace('.html', '').replace('-', ' ').title()
            # Determine parent state and delivery time based on filename patterns
            if any(x in filename for x in ['shah-alam', 'petaling', 'subang', 'klang', 'kajang', 'bangi', 'puchong', 'ampang', 'rawang', 'cyberjaya', 'serdang', 'gombak', 'sepang', 'banting', 'damansara', 'selayang', 'kuala-selangor', 'sabak-bernam']):
                parent = "Selangor"
                delivery = "4 jam"
            elif any(x in filename for x in ['cheras', 'kepong', 'setapak', 'wangsa', 'titiwangsa', 'bukit-bintang', 'bangsar', 'mont-kiara', 'segambut', 'sentul', 'sri-petaling', 'batu']):
                parent = "Kuala Lumpur"
                delivery = "4 jam"
            elif any(x in filename for x in ['johor-bahru', 'batu-pahat', 'muar', 'kluang', 'pontian', 'segamat', 'kota-tinggi', 'mersing', 'kulai', 'pasir-gudang', 'skudai', 'senai', 'iskandar', 'tangkak']):
                parent = "Johor"
                delivery = "24 jam"
            elif any(x in filename for x in ['kota-kinabalu', 'sandakan', 'tawau', 'lahad', 'keningau', 'semporna']):
                parent = "Sabah"
                delivery = "1-2 hari"
            elif any(x in filename for x in ['kuching', 'miri', 'sibu', 'bintulu', 'sri-aman', 'kapit']):
                parent = "Sarawak"
                delivery = "1-2 hari"
            else:
                parent = "Malaysia"
                delivery = "24 jam"

            seo_data = generate_city_seo(filename, city_name, parent, delivery)

        print(f"Optimizing: {filename}")
        if optimize_location_page(filepath, seo_data):
            optimized += 1

    print(f"\n{'=' * 60}")
    print(f"Optimized {optimized} location pages")
    print("=" * 60)

if __name__ == '__main__':
    main()
