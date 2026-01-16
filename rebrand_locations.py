#!/usr/bin/env python3
"""
Rebrand all location pages to match Selangor page structure.
Uses Selangor page as template and generates all other location pages.
"""

import os
import re
import glob

# Location data: filename -> (Display Name, Parent State, Areas Served, Delivery Time)
LOCATIONS = {
    # States
    "johor.html": ("Johor", None, ["Johor Bahru", "Batu Pahat", "Muar", "Kluang", "Pontian", "Segamat", "Kota Tinggi", "Mersing", "Kulai", "Pasir Gudang", "Skudai", "Senai"], "24 jam"),
    "kedah.html": ("Kedah", None, ["Alor Setar", "Sungai Petani", "Kulim", "Langkawi", "Jitra", "Baling", "Pendang", "Yan", "Gurun", "Changlun"], "24 jam"),
    "kelantan.html": ("Kelantan", None, ["Kota Bharu", "Pasir Mas", "Tanah Merah", "Machang", "Kuala Krai", "Gua Musang", "Bachok", "Tumpat", "Pasir Puteh", "Jeli"], "24 jam"),
    "pahang.html": ("Pahang", None, ["Kuantan", "Temerloh", "Bentong", "Raub", "Jerantut", "Pekan", "Maran", "Bera", "Lipis", "Cameron Highlands", "Mentakab", "Rompin"], "24 jam"),
    "perak.html": ("Perak", None, ["Ipoh", "Taiping", "Teluk Intan", "Sitiawan", "Manjung", "Kuala Kangsar", "Kampar", "Batu Gajah", "Seri Iskandar", "Tanjung Malim"], "24 jam"),
    "pulau-pinang.html": ("Pulau Pinang", None, ["George Town", "Butterworth", "Bukit Mertajam", "Bayan Lepas", "Air Itam", "Jelutong", "Balik Pulau", "Tanjung Bungah", "Seberang Perai", "Nibong Tebal", "Kepala Batas"], "24 jam"),
    "terengganu.html": ("Terengganu", None, ["Kuala Terengganu", "Kemaman", "Dungun", "Besut", "Marang", "Hulu Terengganu", "Setiu", "Kuala Nerus", "Chukai", "Paka"], "24 jam"),
    "negeri-sembilan.html": ("Negeri Sembilan", None, ["Seremban", "Port Dickson", "Nilai", "Senawang", "Bahau", "Kuala Pilah", "Tampin", "Rembau", "Jelebu", "Mantin", "Labu", "Gemas"], "24 jam"),
    "sabah.html": ("Sabah", None, ["Kota Kinabalu", "Sandakan", "Tawau", "Lahad Datu", "Keningau", "Semporna"], "1-2 hari"),
    "sarawak.html": ("Sarawak", None, ["Kuching", "Miri", "Sibu", "Bintulu", "Sri Aman", "Kapit"], "1-2 hari"),
    "kuala-lumpur.html": ("Kuala Lumpur", None, ["Cheras", "Kepong", "Setapak", "Wangsa Maju", "Titiwangsa", "Bukit Bintang", "Bangsar", "Mont Kiara", "Segambut", "Sentul", "Sri Petaling", "Batu", "Damansara"], "4 jam"),

    # Cities in Selangor (skip selangor.html itself)
    "shah-alam.html": ("Shah Alam", "Selangor", ["Seksyen 1-25", "Kota Kemuning", "Setia Alam", "Bukit Jelutong", "Alam Impian", "Glenmarie"], "4 jam"),
    "petaling-jaya.html": ("Petaling Jaya", "Selangor", ["SS2", "Damansara Utama", "Kelana Jaya", "Kota Damansara", "Bandar Utama", "Tropicana", "Mutiara Damansara"], "4 jam"),
    "subang-jaya.html": ("Subang Jaya", "Selangor", ["USJ", "Putra Heights", "Bandar Sunway", "SS12-19", "Subang Bestari", "Subang Perdana"], "4 jam"),
    "klang.html": ("Klang", "Selangor", ["Klang Utara", "Klang Selatan", "Pelabuhan Klang", "Bukit Tinggi", "Bandar Botanic", "Setia Alam"], "4 jam"),
    "kajang.html": ("Kajang", "Selangor", ["Bandar Kajang", "Sungai Chua", "Taman Prima Saujana", "Country Heights", "Bandar Baru Bangi", "Saujana Impian"], "4 jam"),
    "bangi.html": ("Bangi", "Selangor", ["Bandar Baru Bangi", "Kajang", "Semenyih", "Serdang", "UKM", "Bangi Gateway"], "4 jam"),
    "puchong.html": ("Puchong", "Selangor", ["Bandar Puteri", "Taman Puchong Utama", "Puchong Jaya", "Kinrara", "IOI Mall", "Setia Walk"], "4 jam"),
    "ampang.html": ("Ampang", "Selangor", ["Ampang Jaya", "Pandan Indah", "Taman TAR", "Bukit Antarabangsa", "Ampang Point", "Ampang Hilir"], "4 jam"),
    "rawang.html": ("Rawang", "Selangor", ["Rawang Town", "Templer Park", "Selayang", "Batu Caves", "Gombak", "Bukit Beruntung"], "4 jam"),
    "cyberjaya.html": ("Cyberjaya", "Selangor", ["Cyberjaya", "Putrajaya", "Dengkil", "Salak Tinggi", "Sepang"], "4 jam"),
    "serdang.html": ("Serdang", "Selangor", ["Seri Kembangan", "Serdang Raya", "UPM", "Mines", "Balakong", "Taman Equine"], "4 jam"),
    "gombak.html": ("Gombak", "Selangor", ["Gombak", "Batu Caves", "Selayang", "Rawang", "IIUM", "Zoo Negara"], "4 jam"),
    "sepang.html": ("Sepang", "Selangor", ["KLIA", "Salak Tinggi", "Dengkil", "Cyberjaya", "Sepang Town"], "4 jam"),
    "kuala-selangor.html": ("Kuala Selangor", "Selangor", ["Kuala Selangor Town", "Tanjung Karang", "Sekinchan", "Bukit Rotan", "Jeram"], "4 jam"),
    "sabak-bernam.html": ("Sabak Bernam", "Selangor", ["Sabak Bernam Town", "Sungai Besar", "Sekinchan"], "4 jam"),
    "selayang.html": ("Selayang", "Selangor", ["Selayang Jaya", "Batu Caves", "Kepong", "Rawang", "Gombak"], "4 jam"),
    "banting.html": ("Banting", "Selangor", ["Banting Town", "Jenjarom", "Morib", "Teluk Panglima Garang"], "4 jam"),
    "damansara.html": ("Damansara", "Selangor", ["Damansara Utama", "Damansara Jaya", "Damansara Heights", "TTDI", "Kota Damansara", "Mutiara Damansara"], "4 jam"),

    # Cities in Johor
    "johor-bahru.html": ("Johor Bahru", "Johor", ["JB Sentral", "Taman Molek", "Mount Austin", "Perling", "Skudai", "Tebrau", "Larkin", "Tampoi"], "24 jam"),
    "batu-pahat.html": ("Batu Pahat", "Johor", ["Batu Pahat Town", "Sri Gading", "Parit Raja", "Yong Peng"], "24 jam"),
    "muar.html": ("Muar", "Johor", ["Muar Town", "Tangkak", "Parit Jawa", "Bukit Bakri", "Pagoh"], "24 jam"),
    "kluang.html": ("Kluang", "Johor", ["Kluang Town", "Simpang Renggam", "Paloh", "Kahang"], "24 jam"),
    "pontian.html": ("Pontian", "Johor", ["Pontian Town", "Pekan Nanas", "Kukup", "Benut"], "24 jam"),
    "segamat.html": ("Segamat", "Johor", ["Segamat Town", "Labis", "Buloh Kasap", "Jementah"], "24 jam"),
    "kota-tinggi.html": ("Kota Tinggi", "Johor", ["Kota Tinggi Town", "Desaru", "Pengerang", "Teluk Ramunia"], "24 jam"),
    "mersing.html": ("Mersing", "Johor", ["Mersing Town", "Endau", "Air Papan", "Tioman Jetty"], "24 jam"),
    "kulai.html": ("Kulai", "Johor", ["Kulai Town", "Senai", "Saleng", "Seelong"], "24 jam"),
    "pasir-gudang.html": ("Pasir Gudang", "Johor", ["Pasir Gudang Town", "Masai", "Permas Jaya", "Plentong"], "24 jam"),
    "skudai.html": ("Skudai", "Johor", ["Skudai Town", "Taman Universiti", "Pulai", "Tun Aminah"], "24 jam"),
    "senai.html": ("Senai", "Johor", ["Senai Town", "Senai Airport", "Kulai"], "24 jam"),
    "iskandar-puteri.html": ("Iskandar Puteri", "Johor", ["Nusajaya", "Puteri Harbour", "Medini", "Gelang Patah", "Kota Iskandar"], "24 jam"),
    "tangkak.html": ("Tangkak", "Johor", ["Tangkak Town", "Ledang", "Sagil", "Kesang"], "24 jam"),

    # Cities in Kedah
    "alor-setar.html": ("Alor Setar", "Kedah", ["Alor Setar Town", "Anak Bukit", "Mergong", "Pekan Melayu", "Tanjung Bendahara"], "24 jam"),
    "sungai-petani.html": ("Sungai Petani", "Kedah", ["Sungai Petani Town", "Bandar Laguna Merbok", "Taman Ria", "Amanjaya"], "24 jam"),
    "kulim.html": ("Kulim", "Kedah", ["Kulim Town", "Kulim Hi-Tech Park", "Lunas", "Padang Serai"], "24 jam"),
    "langkawi.html": ("Langkawi", "Kedah", ["Kuah", "Pantai Cenang", "Padang Matsirat", "Ayer Hangat"], "1-2 hari"),
    "jitra.html": ("Jitra", "Kedah", ["Jitra Town", "Changlun", "Kodiang", "Bukit Kayu Hitam"], "24 jam"),
    "baling.html": ("Baling", "Kedah", ["Baling Town", "Kupang", "Siong"], "24 jam"),
    "pendang.html": ("Pendang", "Kedah", ["Pendang Town", "Bukit Selambau", "Padang Terap"], "24 jam"),
    "yan.html": ("Yan", "Kedah", ["Yan Town", "Guar Chempedak", "Jeniang"], "24 jam"),
    "gurun.html": ("Gurun", "Kedah", ["Gurun Town", "Jeniang", "Sik"], "24 jam"),
    "changlun.html": ("Changlun", "Kedah", ["Changlun Town", "Bukit Kayu Hitam", "Wang Kelian"], "24 jam"),
    "padang-serai.html": ("Padang Serai", "Kedah", ["Padang Serai Town", "Kulim", "Lunas"], "24 jam"),
    "sik.html": ("Sik", "Kedah", ["Sik Town", "Jeniang", "Gulau"], "24 jam"),
    "kuala-kedah.html": ("Kuala Kedah", "Kedah", ["Kuala Kedah Town", "Langkawi Ferry", "Alor Setar"], "24 jam"),

    # Cities in Kelantan
    "kota-bharu.html": ("Kota Bharu", "Kelantan", ["Kota Bharu Town", "Kubang Kerian", "Pengkalan Chepa", "Wakaf Bharu", "PCB"], "24 jam"),
    "pasir-mas.html": ("Pasir Mas", "Kelantan", ["Pasir Mas Town", "Rantau Panjang", "Tok Bali"], "24 jam"),
    "tanah-merah.html": ("Tanah Merah", "Kelantan", ["Tanah Merah Town", "Bukit Bunga", "Kusial"], "24 jam"),
    "machang.html": ("Machang", "Kelantan", ["Machang Town", "Temangan", "Pangkal Meleret"], "24 jam"),
    "kuala-krai.html": ("Kuala Krai", "Kelantan", ["Kuala Krai Town", "Dabong", "Manek Urai"], "24 jam"),
    "gua-musang.html": ("Gua Musang", "Kelantan", ["Gua Musang Town", "Chiku", "Lojing"], "24 jam"),
    "bachok.html": ("Bachok", "Kelantan", ["Bachok Town", "Pantai Irama", "Beris Lalang"], "24 jam"),
    "tumpat.html": ("Tumpat", "Kelantan", ["Tumpat Town", "Wakaf Bharu", "Pengkalan Kubor"], "24 jam"),
    "pasir-puteh.html": ("Pasir Puteh", "Kelantan", ["Pasir Puteh Town", "Selising", "Cherang Ruku"], "24 jam"),
    "jeli.html": ("Jeli", "Kelantan", ["Jeli Town", "Kuala Balah", "Batu Melintang"], "24 jam"),
    "rantau-panjang.html": ("Rantau Panjang", "Kelantan", ["Rantau Panjang Town", "Pasir Mas", "Wakaf Baharu"], "24 jam"),

    # Cities in Pahang
    "kuantan.html": ("Kuantan", "Pahang", ["Kuantan Town", "Indera Mahkota", "Teluk Cempedak", "Gambang", "Gebeng", "Beserah"], "24 jam"),
    "temerloh.html": ("Temerloh", "Pahang", ["Temerloh Town", "Mentakab", "Lanchang", "Kerdau"], "24 jam"),
    "bentong.html": ("Bentong", "Pahang", ["Bentong Town", "Karak", "Bukit Tinggi", "Chamang"], "24 jam"),
    "raub.html": ("Raub", "Pahang", ["Raub Town", "Sungai Ruan", "Dong", "Bukit Fraser"], "24 jam"),
    "jerantut.html": ("Jerantut", "Pahang", ["Jerantut Town", "Taman Negara", "Kuala Tahan", "Kuala Tembeling"], "24 jam"),
    "pekan.html": ("Pekan", "Pahang", ["Pekan Town", "Pekan Pahang", "Nenasi"], "24 jam"),
    "maran.html": ("Maran", "Pahang", ["Maran Town", "Jengka", "Chenor"], "24 jam"),
    "bera.html": ("Bera", "Pahang", ["Bera Town", "Triang", "Kerayong"], "24 jam"),
    "lipis.html": ("Lipis", "Pahang", ["Lipis Town", "Benta", "Padang Tengku"], "24 jam"),
    "cameron-highlands.html": ("Cameron Highlands", "Pahang", ["Tanah Rata", "Brinchang", "Ringlet", "Kampung Raja"], "24 jam"),
    "mentakab.html": ("Mentakab", "Pahang", ["Mentakab Town", "Temerloh", "Lanchang"], "24 jam"),
    "rompin.html": ("Rompin", "Pahang", ["Rompin Town", "Tioman Ferry", "Tanjung Gemok"], "24 jam"),

    # Cities in Pulau Pinang
    "george-town.html": ("George Town", "Pulau Pinang", ["George Town", "Komtar", "Gurney", "Tanjung Tokong", "Pulau Tikus"], "24 jam"),
    "butterworth.html": ("Butterworth", "Pulau Pinang", ["Butterworth Town", "Perai", "Prai", "Raja Uda"], "24 jam"),
    "bukit-mertajam.html": ("Bukit Mertajam", "Pulau Pinang", ["BM Town", "Alma", "Machang Bubuk", "Permatang Tinggi"], "24 jam"),
    "bayan-lepas.html": ("Bayan Lepas", "Pulau Pinang", ["Bayan Lepas Town", "FTZ", "Queensbay", "Sungai Ara"], "24 jam"),
    "air-itam.html": ("Air Itam", "Pulau Pinang", ["Air Itam Town", "Kek Lok Si", "Paya Terubong", "Farlim"], "24 jam"),
    "jelutong.html": ("Jelutong", "Pulau Pinang", ["Jelutong Town", "Gelugor", "Sungai Pinang", "Rifle Range"], "24 jam"),
    "balik-pulau.html": ("Balik Pulau", "Pulau Pinang", ["Balik Pulau Town", "Teluk Kumbar", "Gertak Sanggul", "Pantai Acheh"], "24 jam"),
    "tanjung-bungah.html": ("Tanjung Bungah", "Pulau Pinang", ["Tanjung Bungah", "Batu Ferringhi", "Teluk Bahang"], "24 jam"),
    "seberang-perai.html": ("Seberang Perai", "Pulau Pinang", ["Butterworth", "Bukit Mertajam", "Nibong Tebal", "Kepala Batas", "Simpang Ampat"], "24 jam"),
    "nibong-tebal.html": ("Nibong Tebal", "Pulau Pinang", ["Nibong Tebal Town", "Jawi", "Simpang Ampat"], "24 jam"),
    "kepala-batas.html": ("Kepala Batas", "Pulau Pinang", ["Kepala Batas Town", "Tasek Gelugor", "Penaga"], "24 jam"),
    "tasek-gelugor.html": ("Tasek Gelugor", "Pulau Pinang", ["Tasek Gelugor Town", "Kepala Batas", "Bertam"], "24 jam"),

    # Cities in Terengganu
    "kuala-terengganu.html": ("Kuala Terengganu", "Terengganu", ["Kuala Terengganu Town", "Gong Badak", "Kuala Ibai", "Manir", "Batu Rakit"], "24 jam"),
    "kemaman.html": ("Kemaman", "Terengganu", ["Kemaman Town", "Chukai", "Kerteh", "Kijal", "Paka"], "24 jam"),
    "dungun.html": ("Dungun", "Terengganu", ["Dungun Town", "Paka", "Kuala Abang", "Sura"], "24 jam"),
    "besut.html": ("Besut", "Terengganu", ["Besut Town", "Kuala Besut", "Jerteh", "Kampung Raja"], "24 jam"),
    "marang.html": ("Marang", "Terengganu", ["Marang Town", "Rusila", "Bandar Permaisuri"], "24 jam"),
    "hulu-terengganu.html": ("Hulu Terengganu", "Terengganu", ["Kuala Berang", "Ajil", "Bukit Besi"], "24 jam"),
    "setiu.html": ("Setiu", "Terengganu", ["Setiu Town", "Permaisuri", "Penarik"], "24 jam"),
    "kuala-nerus.html": ("Kuala Nerus", "Terengganu", ["Kuala Nerus Town", "Gong Badak", "Seberang Takir"], "24 jam"),
    "chukai.html": ("Chukai", "Terengganu", ["Chukai Town", "Kemaman", "Kerteh"], "24 jam"),
    "paka.html": ("Paka", "Terengganu", ["Paka Town", "Kerteh", "Dungun"], "24 jam"),

    # Cities in Negeri Sembilan
    "seremban.html": ("Seremban", "Negeri Sembilan", ["Seremban Town", "Seremban 2", "Senawang", "Rasah", "Ampangan", "Labu"], "24 jam"),
    "port-dickson.html": ("Port Dickson", "Negeri Sembilan", ["Port Dickson Town", "Teluk Kemang", "Si Rusa", "Lukut"], "24 jam"),
    "nilai.html": ("Nilai", "Negeri Sembilan", ["Nilai Town", "Nilai 3", "Bandar Baru Nilai", "Putra Nilai"], "24 jam"),
    "senawang.html": ("Senawang", "Negeri Sembilan", ["Senawang Town", "Seremban", "Labu"], "24 jam"),
    "bahau.html": ("Bahau", "Negeri Sembilan", ["Bahau Town", "Jempol", "Serting"], "24 jam"),
    "kuala-pilah.html": ("Kuala Pilah", "Negeri Sembilan", ["Kuala Pilah Town", "Juasseh", "Johol"], "24 jam"),
    "tampin.html": ("Tampin", "Negeri Sembilan", ["Tampin Town", "Gemas", "Gemencheh"], "24 jam"),
    "rembau.html": ("Rembau", "Negeri Sembilan", ["Rembau Town", "Pedas", "Chembong"], "24 jam"),
    "jelebu.html": ("Jelebu", "Negeri Sembilan", ["Jelebu Town", "Kuala Klawang", "Pertang"], "24 jam"),
    "mantin.html": ("Mantin", "Negeri Sembilan", ["Mantin Town", "Nilai", "Lenggeng"], "24 jam"),
    "labu.html": ("Labu", "Negeri Sembilan", ["Labu Town", "Senawang", "Nilai"], "24 jam"),
    "gemas.html": ("Gemas", "Negeri Sembilan", ["Gemas Town", "Tampin", "Gemencheh"], "24 jam"),

    # Cities in KL
    "cheras.html": ("Cheras", "Kuala Lumpur", ["Cheras Town", "Taman Midah", "Taman Connaught", "Taman Segar", "Bandar Tun Hussein Onn"], "4 jam"),
    "kepong.html": ("Kepong", "Kuala Lumpur", ["Kepong Town", "Menjalara", "Desa ParkCity", "Metro Prima", "Kepong Baru"], "4 jam"),
    "setapak.html": ("Setapak", "Kuala Lumpur", ["Setapak Town", "Wangsa Maju", "Gombak", "Taman Melati"], "4 jam"),
    "wangsa-maju.html": ("Wangsa Maju", "Kuala Lumpur", ["Wangsa Maju Town", "KLCC", "Setapak", "Sri Rampai"], "4 jam"),
    "titiwangsa.html": ("Titiwangsa", "Kuala Lumpur", ["Titiwangsa", "KLCC", "Kampung Baru", "Chow Kit"], "4 jam"),
    "bukit-bintang.html": ("Bukit Bintang", "Kuala Lumpur", ["Bukit Bintang", "KLCC", "Pavilion", "Lot 10", "Starhill"], "4 jam"),
    "bangsar.html": ("Bangsar", "Kuala Lumpur", ["Bangsar", "Bangsar South", "Pantai", "Mid Valley"], "4 jam"),
    "mont-kiara.html": ("Mont Kiara", "Kuala Lumpur", ["Mont Kiara", "Sri Hartamas", "Desa Sri Hartamas", "Segambut"], "4 jam"),
    "segambut.html": ("Segambut", "Kuala Lumpur", ["Segambut Town", "Kepong", "Mont Kiara", "Sentul"], "4 jam"),
    "sentul.html": ("Sentul", "Kuala Lumpur", ["Sentul Town", "Sentul East", "Sentul West", "Batu"], "4 jam"),
    "sri-petaling.html": ("Sri Petaling", "Kuala Lumpur", ["Sri Petaling", "Bukit Jalil", "Sungai Besi", "Kuchai Lama"], "4 jam"),
    "batu.html": ("Batu", "Kuala Lumpur", ["Batu", "Batu Caves", "Gombak", "Selayang"], "4 jam"),
    "putrajaya.html": ("Putrajaya", "Putrajaya", ["Presint 1-18", "Cyberjaya", "Dengkil"], "4 jam"),

    # Cities in Sabah
    "kota-kinabalu.html": ("Kota Kinabalu", "Sabah", ["KK Town", "Likas", "Luyang", "Kepayan", "Penampang", "Inanam"], "1-2 hari"),
    "sandakan.html": ("Sandakan", "Sabah", ["Sandakan Town", "Mile 4", "Bandar Kim Fung", "Tanah Merah"], "1-2 hari"),
    "tawau.html": ("Tawau", "Sabah", ["Tawau Town", "Fajar", "Bukit", "Sabindo"], "1-2 hari"),
    "lahad-datu.html": ("Lahad Datu", "Sabah", ["Lahad Datu Town", "Silam", "Tungku"], "1-2 hari"),
    "keningau.html": ("Keningau", "Sabah", ["Keningau Town", "Apin-Apin", "Tenom"], "1-2 hari"),
    "semporna.html": ("Semporna", "Sabah", ["Semporna Town", "Sipadan", "Mabul"], "1-2 hari"),

    # Cities in Sarawak
    "kuching.html": ("Kuching", "Sarawak", ["Kuching Town", "Kota Samarahan", "Padawan", "Bau", "Lundu"], "1-2 hari"),
    "miri.html": ("Miri", "Sarawak", ["Miri Town", "Senadin", "Lutong", "Tudan"], "1-2 hari"),
    "sibu.html": ("Sibu", "Sarawak", ["Sibu Town", "Lanang", "Rantau Panjang"], "1-2 hari"),
    "bintulu.html": ("Bintulu", "Sarawak", ["Bintulu Town", "Kidurong", "Tanjung Kidurong"], "1-2 hari"),
    "sri-aman.html": ("Sri Aman", "Sarawak", ["Sri Aman Town", "Betong", "Lubok Antu"], "1-2 hari"),
    "kapit.html": ("Kapit", "Sarawak", ["Kapit Town", "Song", "Belaga"], "1-2 hari"),
}

def read_template():
    """Read the Selangor page as template"""
    with open('locations/selangor.html', 'r', encoding='utf-8') as f:
        return f.read()

def generate_location_page(template, location_name, parent_state, areas, delivery_time):
    """Generate a location page from the template"""
    content = template

    # Replace Selangor with location name in various contexts
    content = content.replace('Selangor', location_name)
    content = content.replace('selangor', location_name.lower().replace(' ', '-'))

    # Update delivery time
    content = content.replace('4 jam', delivery_time)
    content = content.replace('4 Jam', delivery_time.title())

    # Replace Selangor-specific area names in meta descriptions
    content = content.replace('Shah Alam, PJ, Subang, Klang, Kajang', ', '.join(areas[:5]))
    content = content.replace('Shah Alam, PJ, Subang, Klang, Kajang, dll', ', '.join(areas[:5]) + ', dll')

    # Update keywords with location-specific areas
    old_keywords = 'katil hospital Shah Alam, sewa katil hospital PJ, katil hospital Subang Jaya, katil hospital Klang'
    new_keywords = ', '.join([f'katil hospital {areas[i]}' if i < len(areas) else '' for i in range(min(4, len(areas)))])
    content = content.replace(old_keywords, new_keywords)

    # Update areas served section
    areas_html = ""
    for area in areas[:12]:  # Limit to 12 areas
        areas_html += f'''                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); border-radius: 12px; padding: 20px; text-align: center;">
                        <span style="color: white; font-weight: 600; font-size: 1rem;">{area}</span>
                    </div>
'''

    # Replace the areas grid
    areas_pattern = r'(<div style="display: grid; grid-template-columns: repeat\(4, 1fr\); gap: 16px;">)(.*?)(</div>\s*</div>\s*</section>\s*<!-- FAQ Section -->)'
    areas_replacement = f'\\1\n{areas_html}                \\3'
    content = re.sub(areas_pattern, areas_replacement, content, flags=re.DOTALL)

    # Update Schema areaServed
    schema_areas = ', '.join([f'"{area}"' for area in areas[:10]])
    content = re.sub(
        r'"areaServed": \[.*?\]',
        f'"areaServed": [{schema_areas}]',
        content,
        flags=re.DOTALL
    )

    return content

def main():
    print("Reading Selangor template...")
    template = read_template()

    updated_count = 0
    for filename, data in LOCATIONS.items():
        filepath = f'locations/{filename}'

        if not os.path.exists(filepath):
            print(f"Skipping {filename} - file not found")
            continue

        location_name, parent_state, areas, delivery_time = data

        print(f"Generating: {filename} ({location_name})")
        new_content = generate_location_page(template, location_name, parent_state, areas, delivery_time)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        updated_count += 1

    print(f"\nTotal files updated: {updated_count}")

if __name__ == '__main__':
    main()
