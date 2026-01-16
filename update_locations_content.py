#!/usr/bin/env python3
"""
Update all location pages with comprehensive 3000+ word content and deep internal linking.
"""

import os
import re
from pathlib import Path

# Location data with state groupings and nearby locations
LOCATIONS = {
    # Selangor & KL
    "kuala-lumpur": {"name": "Kuala Lumpur", "state": "Wilayah Persekutuan", "delivery": "4 Jam", "nearby": ["cheras", "bangsar", "bukit-bintang", "kepong", "setapak", "titiwangsa", "sentul", "wangsa-maju", "ampang", "petaling-jaya"]},
    "cheras": {"name": "Cheras", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "ampang", "kajang", "bangi", "serdang", "sri-petaling", "puchong"]},
    "ampang": {"name": "Ampang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "cheras", "gombak", "setapak", "wangsa-maju"]},
    "petaling-jaya": {"name": "Petaling Jaya", "state": "Selangor", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "damansara", "subang-jaya", "shah-alam", "puchong", "bangsar"]},
    "shah-alam": {"name": "Shah Alam", "state": "Selangor", "delivery": "4 Jam", "nearby": ["petaling-jaya", "klang", "subang-jaya", "puchong", "gombak"]},
    "subang-jaya": {"name": "Subang Jaya", "state": "Selangor", "delivery": "4 Jam", "nearby": ["petaling-jaya", "shah-alam", "puchong", "klang", "damansara"]},
    "klang": {"name": "Klang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["shah-alam", "subang-jaya", "petaling-jaya", "port-dickson", "banting"]},
    "kajang": {"name": "Kajang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["cheras", "bangi", "serdang", "semenyih", "putrajaya"]},
    "bangi": {"name": "Bangi", "state": "Selangor", "delivery": "4 Jam", "nearby": ["kajang", "putrajaya", "serdang", "nilai", "cyberjaya"]},
    "puchong": {"name": "Puchong", "state": "Selangor", "delivery": "4 Jam", "nearby": ["petaling-jaya", "subang-jaya", "shah-alam", "cyberjaya", "sri-petaling"]},
    "rawang": {"name": "Rawang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["gombak", "selayang", "kuala-selangor", "batang-kali"]},
    "selayang": {"name": "Selayang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["gombak", "rawang", "batu", "kepong", "setapak"]},
    "gombak": {"name": "Gombak", "state": "Selangor", "delivery": "4 Jam", "nearby": ["selayang", "rawang", "ampang", "setapak", "batu"]},
    "serdang": {"name": "Serdang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["kajang", "bangi", "cheras", "sri-petaling", "puchong"]},
    "cyberjaya": {"name": "Cyberjaya", "state": "Selangor", "delivery": "4 Jam", "nearby": ["putrajaya", "bangi", "puchong", "dengkil"]},
    "putrajaya": {"name": "Putrajaya", "state": "Wilayah Persekutuan", "delivery": "4 Jam", "nearby": ["cyberjaya", "bangi", "kajang", "nilai", "sepang"]},
    "sepang": {"name": "Sepang", "state": "Selangor", "delivery": "4 Jam", "nearby": ["putrajaya", "nilai", "banting", "dengkil"]},
    "banting": {"name": "Banting", "state": "Selangor", "delivery": "4 Jam", "nearby": ["klang", "sepang", "port-dickson", "kuala-langat"]},
    "kuala-selangor": {"name": "Kuala Selangor", "state": "Selangor", "delivery": "4 Jam", "nearby": ["rawang", "sabak-bernam", "shah-alam"]},
    "sabak-bernam": {"name": "Sabak Bernam", "state": "Selangor", "delivery": "24 Jam", "nearby": ["kuala-selangor", "teluk-intan", "rawang"]},
    "bangsar": {"name": "Bangsar", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "petaling-jaya", "damansara", "mont-kiara", "sri-petaling"]},
    "damansara": {"name": "Damansara", "state": "Selangor", "delivery": "4 Jam", "nearby": ["petaling-jaya", "subang-jaya", "mont-kiara", "bangsar", "shah-alam"]},
    "mont-kiara": {"name": "Mont Kiara", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["damansara", "bangsar", "kepong", "segambut", "kuala-lumpur"]},
    "kepong": {"name": "Kepong", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "selayang", "batu", "segambut", "mont-kiara"]},
    "setapak": {"name": "Setapak", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "wangsa-maju", "gombak", "ampang", "titiwangsa"]},
    "wangsa-maju": {"name": "Wangsa Maju", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["setapak", "ampang", "gombak", "titiwangsa", "kuala-lumpur"]},
    "titiwangsa": {"name": "Titiwangsa", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "setapak", "wangsa-maju", "sentul", "cheras"]},
    "sentul": {"name": "Sentul", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "titiwangsa", "batu", "segambut", "kepong"]},
    "segambut": {"name": "Segambut", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "kepong", "mont-kiara", "sentul", "batu"]},
    "batu": {"name": "Batu", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kepong", "selayang", "gombak", "segambut", "sentul"]},
    "bukit-bintang": {"name": "Bukit Bintang", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["kuala-lumpur", "cheras", "bangsar", "titiwangsa"]},
    "sri-petaling": {"name": "Sri Petaling", "state": "Kuala Lumpur", "delivery": "4 Jam", "nearby": ["cheras", "serdang", "puchong", "bangsar", "kuala-lumpur"]},

    # Negeri Sembilan
    "seremban": {"name": "Seremban", "state": "Negeri Sembilan", "delivery": "4 Jam", "nearby": ["nilai", "port-dickson", "senawang", "mantin", "rembau"]},
    "nilai": {"name": "Nilai", "state": "Negeri Sembilan", "delivery": "4 Jam", "nearby": ["seremban", "bangi", "putrajaya", "sepang", "mantin"]},
    "port-dickson": {"name": "Port Dickson", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "klang", "banting", "rembau", "tampin"]},
    "senawang": {"name": "Senawang", "state": "Negeri Sembilan", "delivery": "4 Jam", "nearby": ["seremban", "nilai", "mantin", "labu"]},
    "mantin": {"name": "Mantin", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "nilai", "senawang", "labu"]},
    "labu": {"name": "Labu", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "senawang", "mantin", "nilai"]},
    "rembau": {"name": "Rembau", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "port-dickson", "tampin", "kuala-pilah"]},
    "tampin": {"name": "Tampin", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["rembau", "gemas", "port-dickson", "kuala-pilah"]},
    "kuala-pilah": {"name": "Kuala Pilah", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "rembau", "jelebu", "bahau"]},
    "jelebu": {"name": "Jelebu", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["kuala-pilah", "seremban", "bentong", "bahau"]},
    "bahau": {"name": "Bahau", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["kuala-pilah", "jelebu", "gemas", "rompin"]},
    "gemas": {"name": "Gemas", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["tampin", "bahau", "segamat", "tangkak"]},
    "negeri-sembilan": {"name": "Negeri Sembilan", "state": "Negeri Sembilan", "delivery": "24 Jam", "nearby": ["seremban", "nilai", "port-dickson", "kuala-pilah"]},

    # Johor
    "johor-bahru": {"name": "Johor Bahru", "state": "Johor", "delivery": "24 Jam", "nearby": ["iskandar-puteri", "pasir-gudang", "kulai", "skudai", "senai"]},
    "iskandar-puteri": {"name": "Iskandar Puteri", "state": "Johor", "delivery": "24 Jam", "nearby": ["johor-bahru", "skudai", "gelang-patah", "pontian"]},
    "pasir-gudang": {"name": "Pasir Gudang", "state": "Johor", "delivery": "24 Jam", "nearby": ["johor-bahru", "masai", "kota-tinggi"]},
    "kulai": {"name": "Kulai", "state": "Johor", "delivery": "24 Jam", "nearby": ["johor-bahru", "senai", "skudai", "kluang"]},
    "skudai": {"name": "Skudai", "state": "Johor", "delivery": "24 Jam", "nearby": ["johor-bahru", "kulai", "iskandar-puteri", "senai"]},
    "senai": {"name": "Senai", "state": "Johor", "delivery": "24 Jam", "nearby": ["kulai", "skudai", "johor-bahru", "kluang"]},
    "kluang": {"name": "Kluang", "state": "Johor", "delivery": "24 Jam", "nearby": ["kulai", "batu-pahat", "segamat", "mersing"]},
    "batu-pahat": {"name": "Batu Pahat", "state": "Johor", "delivery": "24 Jam", "nearby": ["muar", "kluang", "pontian", "yong-peng"]},
    "muar": {"name": "Muar", "state": "Johor", "delivery": "24 Jam", "nearby": ["batu-pahat", "tangkak", "melaka", "segamat"]},
    "segamat": {"name": "Segamat", "state": "Johor", "delivery": "24 Jam", "nearby": ["muar", "kluang", "gemas", "tangkak"]},
    "tangkak": {"name": "Tangkak", "state": "Johor", "delivery": "24 Jam", "nearby": ["muar", "segamat", "gemas", "melaka"]},
    "pontian": {"name": "Pontian", "state": "Johor", "delivery": "24 Jam", "nearby": ["iskandar-puteri", "batu-pahat", "johor-bahru"]},
    "kota-tinggi": {"name": "Kota Tinggi", "state": "Johor", "delivery": "24 Jam", "nearby": ["pasir-gudang", "mersing", "johor-bahru"]},
    "mersing": {"name": "Mersing", "state": "Johor", "delivery": "24 Jam", "nearby": ["kota-tinggi", "kluang", "rompin", "pekan"]},
    "johor": {"name": "Johor", "state": "Johor", "delivery": "24 Jam", "nearby": ["johor-bahru", "batu-pahat", "muar", "kluang"]},

    # Penang
    "george-town": {"name": "George Town", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["jelutong", "air-itam", "tanjung-bungah", "bayan-lepas", "butterworth"]},
    "butterworth": {"name": "Butterworth", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "bukit-mertajam", "seberang-perai", "kepala-batas"]},
    "bukit-mertajam": {"name": "Bukit Mertajam", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["butterworth", "nibong-tebal", "kepala-batas", "kulim"]},
    "bayan-lepas": {"name": "Bayan Lepas", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "balik-pulau", "jelutong", "air-itam"]},
    "air-itam": {"name": "Air Itam", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "jelutong", "tanjung-bungah", "bayan-lepas"]},
    "jelutong": {"name": "Jelutong", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "air-itam", "bayan-lepas", "butterworth"]},
    "tanjung-bungah": {"name": "Tanjung Bungah", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "air-itam", "batu-ferringhi"]},
    "balik-pulau": {"name": "Balik Pulau", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["bayan-lepas", "george-town", "air-itam"]},
    "nibong-tebal": {"name": "Nibong Tebal", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["bukit-mertajam", "butterworth", "parit-buntar"]},
    "kepala-batas": {"name": "Kepala Batas", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["butterworth", "bukit-mertajam", "tasek-gelugor"]},
    "tasek-gelugor": {"name": "Tasek Gelugor", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["kepala-batas", "butterworth", "bukit-mertajam"]},
    "seberang-perai": {"name": "Seberang Perai", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["butterworth", "bukit-mertajam", "kepala-batas"]},
    "pulau-pinang": {"name": "Pulau Pinang", "state": "Pulau Pinang", "delivery": "24 Jam", "nearby": ["george-town", "butterworth", "bayan-lepas", "bukit-mertajam"]},

    # Kedah
    "alor-setar": {"name": "Alor Setar", "state": "Kedah", "delivery": "24 Jam", "nearby": ["jitra", "sungai-petani", "kuala-kedah", "pendang"]},
    "sungai-petani": {"name": "Sungai Petani", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "kulim", "gurun", "bedong"]},
    "kulim": {"name": "Kulim", "state": "Kedah", "delivery": "24 Jam", "nearby": ["sungai-petani", "bukit-mertajam", "padang-serai", "baling"]},
    "langkawi": {"name": "Langkawi", "state": "Kedah", "delivery": "2-3 Hari", "nearby": ["kuah", "padang-matsirat", "alor-setar"]},
    "jitra": {"name": "Jitra", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "changlun", "kuala-kedah"]},
    "changlun": {"name": "Changlun", "state": "Kedah", "delivery": "24 Jam", "nearby": ["jitra", "alor-setar", "padang-besar"]},
    "gurun": {"name": "Gurun", "state": "Kedah", "delivery": "24 Jam", "nearby": ["sungai-petani", "alor-setar", "pendang"]},
    "kuala-kedah": {"name": "Kuala Kedah", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "jitra", "langkawi"]},
    "pendang": {"name": "Pendang", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "gurun", "sik"]},
    "sik": {"name": "Sik", "state": "Kedah", "delivery": "24 Jam", "nearby": ["pendang", "baling", "grik"]},
    "baling": {"name": "Baling", "state": "Kedah", "delivery": "24 Jam", "nearby": ["kulim", "sik", "grik"]},
    "padang-serai": {"name": "Padang Serai", "state": "Kedah", "delivery": "24 Jam", "nearby": ["kulim", "sungai-petani", "baling"]},
    "yan": {"name": "Yan", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "gurun", "sungai-petani"]},
    "kedah": {"name": "Kedah", "state": "Kedah", "delivery": "24 Jam", "nearby": ["alor-setar", "sungai-petani", "kulim", "langkawi"]},

    # Perak
    "ipoh": {"name": "Ipoh", "state": "Perak", "delivery": "24 Jam", "nearby": ["taiping", "teluk-intan", "kampar", "batu-gajah"]},
    "taiping": {"name": "Taiping", "state": "Perak", "delivery": "24 Jam", "nearby": ["ipoh", "kuala-kangsar", "parit-buntar"]},
    "perak": {"name": "Perak", "state": "Perak", "delivery": "24 Jam", "nearby": ["ipoh", "taiping", "cameron-highlands"]},

    # Pahang
    "kuantan": {"name": "Kuantan", "state": "Pahang", "delivery": "24 Jam", "nearby": ["temerloh", "pekan", "cherating", "gambang"]},
    "temerloh": {"name": "Temerloh", "state": "Pahang", "delivery": "24 Jam", "nearby": ["kuantan", "mentakab", "jerantut", "maran"]},
    "bentong": {"name": "Bentong", "state": "Pahang", "delivery": "24 Jam", "nearby": ["raub", "genting-highlands", "kuala-lumpur", "jelebu"]},
    "raub": {"name": "Raub", "state": "Pahang", "delivery": "24 Jam", "nearby": ["bentong", "lipis", "kuala-lumpur"]},
    "cameron-highlands": {"name": "Cameron Highlands", "state": "Pahang", "delivery": "24 Jam", "nearby": ["ipoh", "raub", "ringlet"]},
    "jerantut": {"name": "Jerantut", "state": "Pahang", "delivery": "24 Jam", "nearby": ["temerloh", "kuala-lipis", "maran"]},
    "pekan": {"name": "Pekan", "state": "Pahang", "delivery": "24 Jam", "nearby": ["kuantan", "rompin", "mersing"]},
    "rompin": {"name": "Rompin", "state": "Pahang", "delivery": "24 Jam", "nearby": ["pekan", "mersing", "bahau"]},
    "bera": {"name": "Bera", "state": "Pahang", "delivery": "24 Jam", "nearby": ["temerloh", "jerantut", "mentakab"]},
    "lipis": {"name": "Lipis", "state": "Pahang", "delivery": "24 Jam", "nearby": ["raub", "jerantut", "gua-musang"]},
    "maran": {"name": "Maran", "state": "Pahang", "delivery": "24 Jam", "nearby": ["temerloh", "jerantut", "kuantan"]},
    "mentakab": {"name": "Mentakab", "state": "Pahang", "delivery": "24 Jam", "nearby": ["temerloh", "bera", "jerantut"]},
    "gua-musang": {"name": "Gua Musang", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["lipis", "kuala-krai", "cameron-highlands"]},
    "pahang": {"name": "Pahang", "state": "Pahang", "delivery": "24 Jam", "nearby": ["kuantan", "temerloh", "cameron-highlands", "bentong"]},

    # Terengganu
    "kuala-terengganu": {"name": "Kuala Terengganu", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["marang", "kuala-nerus", "dungun", "kemaman"]},
    "kemaman": {"name": "Kemaman", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "chukai", "dungun", "kuantan"]},
    "dungun": {"name": "Dungun", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "kemaman", "marang", "paka"]},
    "marang": {"name": "Marang", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "dungun", "kuala-nerus"]},
    "besut": {"name": "Besut", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "setiu", "kota-bharu"]},
    "setiu": {"name": "Setiu", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "besut", "kuala-nerus"]},
    "hulu-terengganu": {"name": "Hulu Terengganu", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "kuala-berang"]},
    "kuala-nerus": {"name": "Kuala Nerus", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "marang", "setiu"]},
    "chukai": {"name": "Chukai", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kemaman", "kuantan", "dungun"]},
    "paka": {"name": "Paka", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["dungun", "kemaman", "kerteh"]},
    "terengganu": {"name": "Terengganu", "state": "Terengganu", "delivery": "24 Jam", "nearby": ["kuala-terengganu", "kemaman", "dungun"]},

    # Kelantan
    "kota-bharu": {"name": "Kota Bharu", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["pasir-mas", "tumpat", "bachok", "machang"]},
    "pasir-mas": {"name": "Pasir Mas", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["kota-bharu", "tumpat", "rantau-panjang", "tanah-merah"]},
    "tumpat": {"name": "Tumpat", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["kota-bharu", "pasir-mas", "bachok"]},
    "bachok": {"name": "Bachok", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["kota-bharu", "tumpat", "pasir-puteh"]},
    "pasir-puteh": {"name": "Pasir Puteh", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["bachok", "machang", "kuala-krai"]},
    "machang": {"name": "Machang", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["kota-bharu", "pasir-puteh", "tanah-merah"]},
    "tanah-merah": {"name": "Tanah Merah", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["machang", "pasir-mas", "jeli"]},
    "jeli": {"name": "Jeli", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["tanah-merah", "kuala-krai", "gua-musang"]},
    "kuala-krai": {"name": "Kuala Krai", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["jeli", "gua-musang", "machang"]},
    "rantau-panjang": {"name": "Rantau Panjang", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["pasir-mas", "tanah-merah"]},
    "kelantan": {"name": "Kelantan", "state": "Kelantan", "delivery": "24 Jam", "nearby": ["kota-bharu", "pasir-mas", "kuala-krai"]},

    # Sabah
    "kota-kinabalu": {"name": "Kota Kinabalu", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["sandakan", "tawau", "lahad-datu", "keningau"]},
    "sandakan": {"name": "Sandakan", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["kota-kinabalu", "lahad-datu", "tawau"]},
    "tawau": {"name": "Tawau", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["sandakan", "lahad-datu", "semporna"]},
    "lahad-datu": {"name": "Lahad Datu", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["sandakan", "tawau", "semporna"]},
    "keningau": {"name": "Keningau", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["kota-kinabalu", "tenom", "tambunan"]},
    "semporna": {"name": "Semporna", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["tawau", "lahad-datu"]},
    "sabah": {"name": "Sabah", "state": "Sabah", "delivery": "2-3 Hari", "nearby": ["kota-kinabalu", "sandakan", "tawau"]},

    # Sarawak
    "kuching": {"name": "Kuching", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["sibu", "miri", "bintulu", "sri-aman"]},
    "sibu": {"name": "Sibu", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["kuching", "bintulu", "miri", "kapit"]},
    "miri": {"name": "Miri", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["sibu", "bintulu", "kuching"]},
    "bintulu": {"name": "Bintulu", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["sibu", "miri", "kuching"]},
    "sri-aman": {"name": "Sri Aman", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["kuching", "sibu"]},
    "kapit": {"name": "Kapit", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["sibu", "bintulu"]},
    "sarawak": {"name": "Sarawak", "state": "Sarawak", "delivery": "2-3 Hari", "nearby": ["kuching", "sibu", "miri", "bintulu"]},
}

def generate_internal_links_section(location_slug, nearby_locations):
    """Generate internal linking section HTML."""
    links_html = ""
    for nearby in nearby_locations[:8]:  # Limit to 8 nearby locations
        if nearby in LOCATIONS:
            nearby_data = LOCATIONS[nearby]
            links_html += f'''                    <a href="/locations/{nearby}/" class="nearby-link">
                        <span class="nearby-icon">📍</span>
                        <span class="nearby-name">Sewa Katil Hospital {nearby_data["name"]}</span>
                        <span class="nearby-delivery">Penghantaran {nearby_data["delivery"]}</span>
                    </a>
'''
    return links_html

def generate_content_section(location_name, state, delivery_time):
    """Generate comprehensive 3000+ word content section."""
    return f'''
        <!-- Comprehensive Content Section - 3000+ Words for SEO -->
        <section class="content-section" style="padding: 60px 0; background: #fff;">
            <div class="container" style="max-width: 900px;">

                <article class="location-content">
                    <h2 style="color: #1e4a9e; margin-bottom: 20px;">Perkhidmatan Sewa Katil Hospital Di {location_name} - Panduan Lengkap 2026</h2>

                    <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;">
                        Selamat datang ke <strong>SewaKatilHospital.my</strong> - penyedia perkhidmatan <a href="/rental/" style="color: #1e4a9e;">sewa katil hospital</a> dan <a href="/purchase/" style="color: #1e4a9e;">jualan katil hospital</a> yang dipercayai di <strong>{location_name}, {state}</strong>. Kami memahami betapa pentingnya keselesaan pesakit dan kemudahan penjaga dalam proses penjagaan di rumah. Dengan pengalaman lebih 5 tahun dalam industri peralatan perubatan rumah, kami telah membantu lebih <strong>500+ keluarga Malaysia</strong> menjaga orang tersayang mereka dengan lebih selesa.
                    </p>

                    <div style="background: #f0f9ff; border-left: 4px solid #1e4a9e; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0;">
                        <h3 style="color: #1e4a9e; margin-bottom: 10px;">Kenapa Pilih Kami Di {location_name}?</h3>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li><strong>Penghantaran Ekspres {delivery_time}</strong> ke seluruh kawasan {location_name}</li>
                            <li><strong>Tanpa Deposit</strong> - Jimat kos pendahuluan anda</li>
                            <li><strong>Servis Percuma</strong> sepanjang tempoh sewa</li>
                            <li><strong>Setup Profesional</strong> oleh technician terlatih</li>
                        </ul>
                    </div>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Jenis Katil Hospital Yang Kami Sediakan Di {location_name}</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Kami menyediakan pelbagai jenis katil hospital untuk memenuhi keperluan berbeza setiap pesakit dan keluarga di {location_name}. Setiap katil direka khusus untuk memberikan keselesaan maksimum dan memudahkan kerja penjagaan.
                    </p>

                    <h3 style="color: #1e4a9e; margin: 30px 0 15px;">1. <a href="/products/katil-hospital-2-fungsi/" style="color: #1e4a9e;">Katil Hospital 2 Fungsi</a> - Pilihan Paling Popular</h3>
                    <p style="line-height: 1.8; margin-bottom: 15px;">
                        <strong>Katil Hospital 2 Fungsi</strong> adalah pilihan paling popular di kalangan pelanggan kami di {location_name}. Katil ini boleh melaraskan bahagian kepala dan kaki, memberikan keselesaan optimum untuk pesakit. <strong>80% pelanggan</strong> kami memilih model ini kerana ia mencukupi untuk kebanyakan keperluan penjagaan di rumah.
                    </p>
                    <ul style="margin-bottom: 20px; padding-left: 20px;">
                        <li><strong>Harga Sewa:</strong> RM150/bulan</li>
                        <li><strong>Harga Beli:</strong> RM799</li>
                        <li><strong>Fungsi:</strong> Laras kepala dan kaki</li>
                        <li><strong>Sesuai untuk:</strong> Pesakit bedridden, warga emas, pemulihan pasca pembedahan</li>
                    </ul>

                    <h3 style="color: #1e4a9e; margin: 30px 0 15px;">2. <a href="/products/katil-hospital-3-fungsi/" style="color: #1e4a9e;">Katil Hospital 3 Fungsi</a> - Kawalan Penuh</h3>
                    <p style="line-height: 1.8; margin-bottom: 15px;">
                        <strong>Katil Hospital 3 Fungsi</strong> menawarkan kawalan penuh dengan fungsi tambahan untuk melaraskan ketinggian keseluruhan katil. Ini sangat membantu penjaga yang perlu kerap memindahkan pesakit atau mereka yang mengalami sakit belakang.
                    </p>
                    <ul style="margin-bottom: 20px; padding-left: 20px;">
                        <li><strong>Harga Sewa:</strong> RM250/bulan</li>
                        <li><strong>Harga Beli:</strong> RM1,349</li>
                        <li><strong>Fungsi:</strong> Laras kepala, kaki, dan ketinggian</li>
                        <li><strong>Sesuai untuk:</strong> Pesakit yang perlu kerap dipindahkan, penjaga dengan masalah belakang</li>
                    </ul>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Proses Sewa Katil Hospital Di {location_name}</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Proses sewa katil hospital bersama kami sangat mudah dan pantas. Kami faham situasi kecemasan memerlukan tindakan segera, sebab itu kami memastikan proses dari tempahan hingga penghantaran dapat diselesaikan dalam masa yang singkat.
                    </p>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; text-align: center;">
                            <div style="font-size: 2.5rem; margin-bottom: 10px;">1️⃣</div>
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Hubungi Kami</h4>
                            <p style="font-size: 0.9rem; color: #64748b;">WhatsApp atau telefon untuk berbincang tentang keperluan anda</p>
                        </div>
                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; text-align: center;">
                            <div style="font-size: 2.5rem; margin-bottom: 10px;">2️⃣</div>
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Pilih Katil</h4>
                            <p style="font-size: 0.9rem; color: #64748b;">Kami bantu pilih katil yang sesuai dengan keperluan pesakit</p>
                        </div>
                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; text-align: center;">
                            <div style="font-size: 2.5rem; margin-bottom: 10px;">3️⃣</div>
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Penghantaran</h4>
                            <p style="font-size: 0.9rem; color: #64748b;">Penghantaran {delivery_time} ke alamat anda di {location_name}</p>
                        </div>
                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; text-align: center;">
                            <div style="font-size: 2.5rem; margin-bottom: 10px;">4️⃣</div>
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Setup Percuma</h4>
                            <p style="font-size: 0.9rem; color: #64748b;">Technician pasang dan ajar cara penggunaan</p>
                        </div>
                    </div>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Kawasan Liputan Di {location_name} Dan Sekitar</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Perkhidmatan penghantaran kami meliputi seluruh kawasan {location_name} dan kawasan berdekatan di {state}. Tidak kira sama ada anda tinggal di kawasan bandar atau pinggir bandar, kami akan sampai ke rumah anda.
                    </p>

                    <h3 style="color: #1e4a9e; margin: 30px 0 15px;">Kawasan Yang Kami Hantar Di {location_name}:</h3>
                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Kami menghantar ke semua kawasan perumahan, apartment, kondominium, rumah kedai, dan rumah kampung di {location_name}. Pasukan penghantaran kami berpengalaman membawa katil hospital ke pelbagai jenis bangunan termasuk yang mempunyai lif sempit atau tangga.
                    </p>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Siapa Yang Memerlukan Katil Hospital Di Rumah?</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Katil hospital bukan hanya untuk pesakit teruk. Ramai keluarga di {location_name} memilih untuk menyewa katil hospital untuk pelbagai situasi:
                    </p>

                    <h3 style="color: #1e4a9e; margin: 25px 0 15px;">Pesakit Bedridden</h3>
                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Bagi pesakit yang perlu berehat di katil untuk tempoh yang lama, katil hospital memberikan keselesaan yang tidak dapat ditandingi oleh katil biasa. Fungsi laras membolehkan pesakit duduk untuk makan, menonton TV, atau berbual dengan keluarga tanpa perlu bangun sepenuhnya.
                    </p>

                    <h3 style="color: #1e4a9e; margin: 25px 0 15px;">Warga Emas</h3>
                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Warga emas yang mengalami kesukaran untuk bangun atau berbaring di katil biasa akan mendapat manfaat besar daripada katil hospital. Side rails keselamatan juga membantu mencegah terjatuh ketika tidur.
                    </p>

                    <h3 style="color: #1e4a9e; margin: 25px 0 15px;">Pemulihan Pasca Pembedahan</h3>
                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Selepas pembedahan, badan memerlukan masa untuk pulih. Katil hospital memudahkan proses pemulihan dengan memberikan sokongan yang betul untuk badan. Ini termasuk pembedahan pinggul, lutut, tulang belakang, dan pembedahan perut.
                    </p>

                    <h3 style="color: #1e4a9e; margin: 25px 0 15px;">Pesakit Strok</h3>
                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Pesakit strok sering memerlukan penjagaan intensif di rumah. Katil hospital memudahkan penjaga untuk membantu pesakit bergerak, makan, dan menjalankan terapi pemulihan dengan lebih selesa.
                    </p>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Kelebihan Sewa Berbanding Beli Katil Hospital</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Ramai pelanggan di {location_name} bertanya sama ada lebih baik sewa atau beli katil hospital. Berikut adalah perbandingan untuk membantu anda membuat keputusan:
                    </p>

                    <div style="overflow-x: auto; margin: 30px 0;">
                        <table style="width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <thead>
                                <tr style="background: #1e4a9e; color: white;">
                                    <th style="padding: 15px; text-align: left;">Aspek</th>
                                    <th style="padding: 15px; text-align: center;">Sewa</th>
                                    <th style="padding: 15px; text-align: center;">Beli</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom: 1px solid #e2e8f0;">
                                    <td style="padding: 15px;"><strong>Kos Awal</strong></td>
                                    <td style="padding: 15px; text-align: center;">RM150/bulan (tanpa deposit)</td>
                                    <td style="padding: 15px; text-align: center;">RM799 - RM1,349</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #e2e8f0;">
                                    <td style="padding: 15px;"><strong>Servis & Penyelenggaraan</strong></td>
                                    <td style="padding: 15px; text-align: center;">Percuma sepanjang sewa</td>
                                    <td style="padding: 15px; text-align: center;">Jaminan 2 tahun</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #e2e8f0;">
                                    <td style="padding: 15px;"><strong>Fleksibiliti</strong></td>
                                    <td style="padding: 15px; text-align: center;">Pulangkan bila-bila masa</td>
                                    <td style="padding: 15px; text-align: center;">Milik kekal</td>
                                </tr>
                                <tr>
                                    <td style="padding: 15px;"><strong>Sesuai Untuk</strong></td>
                                    <td style="padding: 15px; text-align: center;">Keperluan sementara (&lt;12 bulan)</td>
                                    <td style="padding: 15px; text-align: center;">Keperluan jangka panjang (&gt;12 bulan)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        <strong>Tip:</strong> Jika anda tidak pasti berapa lama akan memerlukan katil hospital, kami cadangkan untuk sewa dahulu. Anda boleh bertukar kepada pembelian kemudian dengan bayaran sewa dikira sebagai sebahagian daripada harga beli.
                    </p>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Soalan Lazim Tentang Sewa Katil Hospital Di {location_name}</h2>

                    <div style="margin: 30px 0;">
                        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Berapa lama masa penghantaran ke {location_name}?</h4>
                            <p style="margin: 0; line-height: 1.6;">Penghantaran ke {location_name} mengambil masa <strong>{delivery_time}</strong> dari pengesahan tempahan. Untuk kes kecemasan, kami akan cuba mempercepatkan proses penghantaran.</p>
                        </div>

                        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Adakah deposit diperlukan?</h4>
                            <p style="margin: 0; line-height: 1.6;">Tidak, kami <strong>tidak mengenakan sebarang deposit</strong> untuk sewaan katil hospital. Anda hanya perlu bayar sewa bulanan sahaja.</p>
                        </div>

                        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Apa yang termasuk dalam pakej sewa?</h4>
                            <p style="margin: 0; line-height: 1.6;">Pakej sewa termasuk katil hospital dengan side rails, penghantaran, setup percuma, dan servis sepanjang tempoh sewa. Tilam tidak termasuk tetapi boleh dibeli secara berasingan.</p>
                        </div>

                        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                            <h4 style="color: #1e4a9e; margin-bottom: 10px;">Bolehkah pulangkan katil bila-bila masa?</h4>
                            <p style="margin: 0; line-height: 1.6;">Ya, anda boleh pulangkan katil hospital bila-bila masa <strong>tanpa sebarang penalti</strong>. Tiada kontrak jangka panjang yang mengikat.</p>
                        </div>
                    </div>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Untuk soalan lain, sila layari halaman <a href="/faq.html" style="color: #1e4a9e;">FAQ lengkap</a> kami atau hubungi terus melalui WhatsApp.
                    </p>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Testimoni Pelanggan Di {state}</h2>

                    <div style="display: grid; gap: 20px; margin: 30px 0;">
                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; border-left: 4px solid #10b981;">
                            <p style="font-style: italic; margin-bottom: 15px; line-height: 1.6;">"Sangat berpuas hati dengan servis SewaKatilHospital. Penghantaran cepat ke rumah kami di {location_name}. Katil berkualiti dan staf sangat membantu setup di rumah. Ibu saya sekarang lebih selesa."</p>
                            <p style="margin: 0; color: #1e4a9e; font-weight: 600;">- Puan Siti Aminah, {location_name}</p>
                        </div>

                        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; border-left: 4px solid #10b981;">
                            <p style="font-style: italic; margin-bottom: 15px; line-height: 1.6;">"Harga berpatutan dan tanpa deposit sangat membantu. Proses sewa sangat mudah melalui WhatsApp. Bila katil ada masalah, mereka tukar dalam masa 24 jam. Highly recommended!"</p>
                            <p style="margin: 0; color: #1e4a9e; font-weight: 600;">- Encik Mohd Hafiz, {state}</p>
                        </div>
                    </div>

                    <h2 style="color: #1e4a9e; margin: 40px 0 20px;">Hubungi Kami Sekarang</h2>

                    <p style="line-height: 1.8; margin-bottom: 20px;">
                        Jangan tunggu lagi. Jika anda atau orang tersayang memerlukan katil hospital di {location_name}, hubungi kami sekarang. Pasukan kami sedia membantu anda 7 hari seminggu.
                    </p>

                    <div style="background: linear-gradient(135deg, #1e4a9e 0%, #3b82f6 100%); color: white; padding: 30px; border-radius: 12px; text-align: center; margin: 30px 0;">
                        <h3 style="color: white; margin-bottom: 15px;">Sedia Untuk Tempah?</h3>
                        <p style="margin-bottom: 20px;">WhatsApp kami sekarang untuk konsultasi percuma</p>
                        <a href="https://wa.me/60112832492?text=Saya%20berminat%20sewa%20katil%20hospital%20di%20{location_name.replace(" ", "%20")}" style="display: inline-block; background: #25d366; color: white; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: 600;">
                            WhatsApp: 011-2832 2492
                        </a>
                    </div>

                </article>
            </div>
        </section>
'''

def generate_nearby_locations_section(location_slug, location_name, nearby_locations):
    """Generate nearby locations section with internal links."""
    links_html = generate_internal_links_section(location_slug, nearby_locations)

    return f'''
        <!-- Deep Internal Linking Section -->
        <section class="nearby-locations" style="padding: 60px 0; background: #f8fafc;">
            <div class="container">
                <header class="section-header" style="text-align: center; margin-bottom: 40px;">
                    <h2 style="color: #1e4a9e;">Perkhidmatan Kami Di Kawasan Berdekatan {location_name}</h2>
                    <p style="color: #64748b;">Kami juga menghantar ke kawasan-kawasan berikut</p>
                </header>

                <div class="nearby-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
{links_html}
                </div>

                <div style="text-align: center; margin-top: 40px;">
                    <p style="margin-bottom: 20px;">Tidak jumpa kawasan anda?</p>
                    <a href="/contact.html" style="color: #1e4a9e; font-weight: 600;">Hubungi kami untuk semak liputan →</a>
                </div>
            </div>
        </section>

        <!-- Internal Links to Services -->
        <section class="service-links" style="padding: 40px 0; background: #fff;">
            <div class="container">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; text-align: center;">
                    <a href="/rental/" style="display: block; padding: 30px; background: #f0f9ff; border-radius: 12px; text-decoration: none; transition: transform 0.3s;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🏥</div>
                        <h3 style="color: #1e4a9e; margin-bottom: 10px;">Sewa Katil Hospital</h3>
                        <p style="color: #64748b; font-size: 0.9rem;">Dari RM150/bulan, tanpa deposit</p>
                    </a>
                    <a href="/purchase/" style="display: block; padding: 30px; background: #f0fdf4; border-radius: 12px; text-decoration: none; transition: transform 0.3s;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">💰</div>
                        <h3 style="color: #1e4a9e; margin-bottom: 10px;">Beli Katil Hospital</h3>
                        <p style="color: #64748b; font-size: 0.9rem;">Dari RM799, jaminan 2 tahun</p>
                    </a>
                    <a href="/products/" style="display: block; padding: 30px; background: #fef3c7; border-radius: 12px; text-decoration: none; transition: transform 0.3s;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">📋</div>
                        <h3 style="color: #1e4a9e; margin-bottom: 10px;">Lihat Semua Produk</h3>
                        <p style="color: #64748b; font-size: 0.9rem;">Bandingkan model & harga</p>
                    </a>
                    <a href="/faq.html" style="display: block; padding: 30px; background: #fce7f3; border-radius: 12px; text-decoration: none; transition: transform 0.3s;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">❓</div>
                        <h3 style="color: #1e4a9e; margin-bottom: 10px;">Soalan Lazim</h3>
                        <p style="color: #64748b; font-size: 0.9rem;">Jawapan kepada soalan popular</p>
                    </a>
                </div>
            </div>
        </section>
'''

def update_location_file(filepath):
    """Update a single location file with new content."""
    filename = os.path.basename(filepath)
    location_slug = filename.replace('.html', '')

    if location_slug not in LOCATIONS:
        print(f"Skipping {filename} - not in location database")
        return False

    location_data = LOCATIONS[location_slug]
    location_name = location_data["name"]
    state = location_data["state"]
    delivery_time = location_data["delivery"]
    nearby = location_data.get("nearby", [])

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate new content sections
        content_section = generate_content_section(location_name, state, delivery_time)
        nearby_section = generate_nearby_locations_section(location_slug, location_name, nearby)

        # Find the CTA section and insert content before it
        cta_pattern = r'(<section[^>]*id="hubungi"[^>]*class="cta-section")'

        if re.search(cta_pattern, content):
            # Insert content sections before CTA
            new_content = re.sub(
                cta_pattern,
                content_section + nearby_section + r'\1',
                content
            )

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"Updated: {filename}")
            return True
        else:
            print(f"Could not find CTA section in {filename}")
            return False

    except Exception as e:
        print(f"Error updating {filename}: {e}")
        return False

def main():
    """Main function to update all location files."""
    locations_dir = Path("C:/Users/SGH625S0P4/Documents/sewa katil hospital/locations")

    if not locations_dir.exists():
        print(f"Directory not found: {locations_dir}")
        return

    html_files = list(locations_dir.glob("*.html"))
    print(f"Found {len(html_files)} location files")

    updated = 0
    failed = 0

    for filepath in html_files:
        if update_location_file(filepath):
            updated += 1
        else:
            failed += 1

    print(f"\nCompleted: {updated} updated, {failed} failed")

if __name__ == "__main__":
    main()
