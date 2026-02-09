"""
Phase 1: SEO Overhaul for 16 State Pages
Transforms each state page with unique content per the plan.
KL already done manually - this handles the remaining 15.
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# STATE DATA - All 15 remaining states (KL done manually)
# ============================================================

STATES = {
    "selangor": {
        "name": "Selangor",
        "state": "Selangor",
        "tier": 1,  # 1=4jam, 2=same-day/24jam, 3=1-2 hari
        "delivery_time": "4 jam",
        "delivery_cost": "RM50",
        "distance": "~15 km (Shah Alam)",
        "lat": "3.0738",
        "lng": "101.5183",
        "population": "6.5 juta",
        "meta_title": "Sewa Katil Hospital Selangor | Penghantaran Seluruh Selangor (2026)",
        "meta_desc": "Sewa katil hospital di Selangor dari RM150/bulan. Penghantaran 4 jam ke Shah Alam, PJ, Subang Jaya, Klang. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "hero_subtitle": "Penghantaran Express 4 Jam. Lebih 500+ keluarga di Selangor pilih kami. Tanpa Deposit.",
        "intro_paragraphs": [
            "Selangor, negeri terpadat di Malaysia dengan populasi lebih 6.5 juta penduduk, merupakan pasaran terbesar untuk perkhidmatan sewa katil hospital. Kawasan seperti Shah Alam, Petaling Jaya, Subang Jaya, Klang dan Kajang mempunyai permintaan yang sangat tinggi terutamanya untuk penjagaan warga emas dan pesakit post-surgery di rumah.",
            "Dengan lebih 30 hospital kerajaan dan swasta di seluruh Selangor, kami menerima ratusan tempahan setiap bulan daripada keluarga yang memerlukan katil hospital selepas ahli keluarga discharge. Gudang kami di Batu Caves terletak strategik di sempadan KL-Selangor, membolehkan penghantaran express 4 jam ke kebanyakan kawasan di Selangor.",
            "Sebagai negeri paling maju di Malaysia, Selangor mempunyai infrastruktur jalan raya yang baik memudahkan penghantaran ke semua daerah termasuk Petaling, Klang, Hulu Langat, Gombak, Sepang, Kuala Selangor, Hulu Selangor dan Sabak Bernam. Kami juga menyediakan perkhidmatan ke kawasan baru seperti Cyberjaya, Puchong dan Rawang."
        ],
        "hospitals": [
            ("Hospital Shah Alam", "Persiaran Kayangan, Seksyen 7, Shah Alam", "30 minit"),
            ("Hospital Tengku Ampuan Rahimah Klang", "Jalan Langat, Klang", "40 minit"),
            ("Sunway Medical Centre", "Jalan Lagoon Selatan, Subang Jaya", "35 minit"),
            ("Columbia Asia Hospital PJ", "Jalan 13/6, Seksyen 13, PJ", "30 minit"),
            ("KPJ Selangor Specialist Hospital", "Lot 1, Seksyen 16, Shah Alam", "35 minit"),
        ],
        "testimonials": [
            ("Puan Aishah", "A", "Kota Kemuning, Shah Alam", "Ayah saya baru discharge dari Hospital Shah Alam, perlukan katil hospital segera. Hubungi pagi, petang dah sampai. Sangat cepat dan profesional!"),
            ("En. Hafiz", "H", "Setia Alam, Shah Alam", "Sewa katil untuk mak yang stroke. Staff ajar cara guna dengan teliti. Harga berpatutan dan tak ada deposit. Highly recommend!"),
            ("Cik Nurul", "N", "Seksyen 7, Shah Alam", "Dah 6 bulan sewa untuk jaga nenek. Katil berkualiti, servis maintain pun bagus. Setiap kali ada masalah, technician datang hari yang sama."),
        ],
        "coverage_areas": ["Shah Alam", "Petaling Jaya", "Subang Jaya", "Klang", "Kajang", "Bangi", "Puchong", "Rawang", "Cyberjaya", "Sepang", "Kuala Selangor", "Sabak Bernam"],
        "cities": [
            ("Shah Alam", "shah-alam"), ("Petaling Jaya", "petaling-jaya"), ("Subang Jaya", "subang-jaya"),
            ("Klang", "klang"), ("Kajang", "kajang"), ("Bangi", "bangi"), ("Puchong", "puchong"),
            ("Rawang", "rawang"), ("Cyberjaya", "cyberjaya"), ("Sepang", "sepang"),
            ("Kuala Selangor", "kuala-selangor"), ("Sabak Bernam", "sabak-bernam"),
            ("Ampang", "ampang"), ("Gombak", "gombak"), ("Serdang", "serdang"),
            ("Selayang", "selayang"), ("Damansara", "damansara"), ("Banting", "banting"),
        ],
        "nearby_states": [
            ("Kuala Lumpur", "kuala-lumpur", "Penghantaran 4 Jam"),
            ("Putrajaya", "putrajaya", "Penghantaran 4 Jam"),
            ("Negeri Sembilan", "negeri-sembilan", "Penghantaran 24 Jam"),
            ("Perak", "perak", "Penghantaran 1-2 Hari"),
            ("Pahang", "pahang", "Penghantaran 1-2 Hari"),
        ],
        "why_us_descriptions": [
            "Gudang di Batu Caves - katil sampai ke Shah Alam, PJ, Klang dalam 4 jam",
            "Penduduk Selangor tak perlu bayar deposit. Terus sewa dari RM150/bulan sahaja",
            "Pasukan kami pasang di rumah, kondo atau apartment di Selangor tanpa caj tambahan",
            "Sewa bulanan. Pulangkan bila-bila masa tanpa penalti",
            "Hotline kecemasan 24 jam untuk semua pelanggan di Selangor",
            "Technician datang ke rumah anda di Selangor untuk repair percuma sepanjang sewa",
        ],
        "faq": [
            ("Berapa harga sewa katil hospital di Selangor?", "Harga sewa katil hospital di Selangor bermula dari <strong>RM150/bulan</strong> untuk katil 2 fungsi manual. Katil 3 fungsi manual dari RM250/bulan. Tiada deposit diperlukan."),
            ("Berapa lama penghantaran katil hospital ke Selangor?", "Penghantaran ke kebanyakan kawasan Selangor dalam masa <strong>4 jam</strong> selepas pengesahan order. Gudang kami di Batu Caves memudahkan akses ke Shah Alam (30 min), PJ (25 min), Klang (40 min) dan Kajang (45 min). Order sebelum 2pm untuk penghantaran hari yang sama."),
            ("Kawasan mana di Selangor yang anda cover?", "Kami cover <strong>seluruh Selangor</strong> termasuk Shah Alam, Petaling Jaya, Subang Jaya, Klang, Kajang, Bangi, Puchong, Rawang, Cyberjaya, Sepang, Kuala Selangor dan Sabak Bernam. Untuk kawasan luar bandar Selangor, sila hubungi untuk pengesahan masa penghantaran."),
            ("Hospital mana di Selangor yang pesakit anda biasa discharge dari?", "Kami kerap menerima tempahan dari pesakit yang discharge dari <strong>Hospital Shah Alam</strong>, Hospital Tengku Ampuan Rahimah Klang, Sunway Medical Centre, Columbia Asia PJ dan KPJ Selangor. Kami boleh coordinate penghantaran pada hari yang sama pesakit discharge."),
            ("Boleh hantar ke kawasan baru macam Cyberjaya dan Puchong?", "Ya, kami cover <strong>semua kawasan baru di Selangor</strong> termasuk Cyberjaya, Puchong, Setia Alam, Kota Kemuning, Rawang dan Bangi. Kawasan-kawasan ini mudah diakses dari gudang kami dan penghantaran biasanya dalam masa 4 jam."),
        ],
        "gallery_alts": [
            "Katil hospital 2 fungsi dipasang di rumah pelanggan di Shah Alam",
            "Penghantaran katil hospital ke apartment di Petaling Jaya",
            "Setup katil hospital untuk warga emas di Subang Jaya",
            "Pemasangan katil hospital 3 fungsi di kondo Klang",
            "Katil hospital untuk pesakit stroke di Kajang",
            "Penghantaran express katil hospital ke Bangi",
            "Katil hospital dengan side rails untuk keselamatan pesakit di Puchong",
            "Pemasangan percuma katil hospital di rumah teres Rawang",
            "Katil hospital manual 2 fungsi siap dipasang di Cyberjaya",
            "Penghantaran katil hospital untuk pesakit post-surgery di Sepang",
            "Sewa katil hospital untuk home care di Gombak, Selangor",
            "Katil hospital dengan tilam ripple untuk cegah bedsore di Ampang",
        ],
        "condo_q": ("Boleh hantar ke kawasan baru macam Cyberjaya dan Puchong?", "Ya, kami cover <strong>semua kawasan baru di Selangor</strong> termasuk Cyberjaya, Puchong, Setia Alam, Kota Kemuning, Rawang dan Bangi. Kawasan-kawasan ini mudah diakses dari gudang kami dan penghantaran biasanya dalam masa 4 jam."),
    },

    "johor": {
        "name": "Johor",
        "state": "Johor",
        "tier": 2,
        "delivery_time": "24 jam",
        "delivery_cost": "RM80-120",
        "distance": "Partner logistik tempatan",
        "lat": "1.4927",
        "lng": "103.7414",
        "population": "4 juta",
        "meta_title": "Sewa Katil Hospital Johor | Penghantaran Seluruh Johor (2026)",
        "meta_desc": "Sewa katil hospital di Johor dari RM150/bulan. Penghantaran same-day ke JB, Batu Pahat, Muar, Kluang. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "hero_subtitle": "Penghantaran Same-Day ke seluruh Johor. Dipercayai sejak 2016. Tanpa Deposit.",
        "intro_paragraphs": [
            "Johor, negeri kedua terbesar di Malaysia dengan populasi lebih 4 juta penduduk, mempunyai permintaan yang semakin meningkat untuk katil hospital rumah. Kawasan utama seperti Johor Bahru, Batu Pahat, Muar, Kluang dan Pontian mempunyai ramai penduduk yang memerlukan penjagaan pesakit di rumah terutamanya warga emas dan pesakit post-surgery.",
            "Johor terkenal dengan hospital-hospital bertaraf antarabangsa seperti KPJ Johor Specialist, Gleneagles Medini, Columbia Asia JB dan Hospital Sultanah Aminah. Ramai pesakit yang discharge dari hospital-hospital ini memerlukan katil hospital untuk meneruskan pemulihan di rumah. Kami menyediakan perkhidmatan penghantaran ke seluruh Johor melalui partner logistik tempatan.",
            "Sebagai negeri yang bersempadan dengan Singapura, Johor mempunyai populasi warga emas yang besar terutamanya di kawasan bandar seperti JB dan Iskandar Puteri. Permintaan untuk home care semakin meningkat seiring dengan kos rawatan hospital yang tinggi. Kami menyediakan penghantaran same-day ke kebanyakan kawasan di Johor."
        ],
        "hospitals": [
            ("Hospital Sultanah Aminah", "Jalan Persiaran Abu Bakar Sultan, JB", "Same day"),
            ("KPJ Johor Specialist Hospital", "Jalan Abdul Samad, JB", "Same day"),
            ("Gleneagles Hospital Medini", "Iskandar Puteri, Johor", "Same day"),
            ("Columbia Asia Hospital JB", "Jalan Masai, JB", "Same day"),
            ("Hospital Enche' Besar Hajjah Khalsom", "Kluang, Johor", "Same day"),
        ],
        "testimonials": [
            ("En. Ahmad", "A", "Skudai, Johor Bahru", "First time sewa katil hospital. Proses mudah, harga berpatutan. Katil sampai on time dan staff sangat professional."),
            ("Puan Noraini", "N", "Iskandar Puteri, Johor", "Ayah stroke, perlukan katil 3 fungsi. Sangat puas hati dengan kualiti dan service. Recommend kepada semua."),
            ("Cik Melissa", "M", "Batu Pahat, Johor", "Staff sangat helpful explain semua fungsi katil. Penghantaran ke Batu Pahat pun smooth. Terima kasih!"),
        ],
        "coverage_areas": ["Johor Bahru", "Iskandar Puteri", "Skudai", "Pasir Gudang", "Kulai", "Batu Pahat", "Muar", "Kluang", "Pontian", "Segamat", "Mersing", "Kota Tinggi"],
        "cities": [
            ("Johor Bahru", "johor-bahru"), ("Iskandar Puteri", "iskandar-puteri"), ("Skudai", "skudai"),
            ("Pasir Gudang", "pasir-gudang"), ("Kulai", "kulai"), ("Batu Pahat", "batu-pahat"),
            ("Muar", "muar"), ("Kluang", "kluang"), ("Pontian", "pontian"),
            ("Segamat", "segamat"), ("Mersing", "mersing"), ("Kota Tinggi", "kota-tinggi"),
            ("Tangkak", "tangkak"), ("Senai", "senai"),
        ],
        "nearby_states": [
            ("Melaka", "melaka", "Penghantaran 24 Jam"),
            ("Negeri Sembilan", "negeri-sembilan", "Penghantaran 1-2 Hari"),
            ("Pahang", "pahang", "Penghantaran 1-2 Hari"),
            ("Selangor", "selangor", "Penghantaran 1-2 Hari"),
        ],
        "why_us_descriptions": [
            "Partner logistik tempatan di JB - penghantaran same-day ke seluruh Johor",
            "Penduduk Johor tak perlu bayar deposit. Terus sewa dari RM150/bulan sahaja",
            "Pasukan kami pasang di rumah anda di Johor tanpa caj tambahan",
            "Sewa bulanan. Pulangkan bila-bila masa tanpa penalti",
            "Hotline kecemasan 24 jam untuk semua pelanggan di Johor",
            "Technician datang ke rumah anda di Johor untuk repair percuma sepanjang sewa",
        ],
        "faq": [
            ("Berapa harga sewa katil hospital di Johor?", "Harga sewa katil hospital di Johor bermula dari <strong>RM150/bulan</strong> untuk katil 2 fungsi manual. Katil 3 fungsi manual dari RM250/bulan. Tiada deposit diperlukan."),
            ("Berapa lama penghantaran katil hospital ke Johor?", "Penghantaran ke kawasan Johor Bahru dan sekitar biasanya <strong>same-day</strong> (hari yang sama). Untuk kawasan lain di Johor seperti Batu Pahat, Muar dan Kluang, penghantaran dalam masa <strong>24 jam</strong>."),
            ("Kawasan mana di Johor yang anda cover?", "Kami cover <strong>seluruh Johor</strong> termasuk Johor Bahru, Iskandar Puteri, Skudai, Pasir Gudang, Kulai, Batu Pahat, Muar, Kluang, Pontian, Segamat, Mersing dan Kota Tinggi."),
            ("Hospital mana di Johor yang pesakit anda biasa discharge dari?", "Kami kerap menerima tempahan dari pesakit yang discharge dari <strong>Hospital Sultanah Aminah</strong>, KPJ Johor Specialist, Gleneagles Medini dan Columbia Asia JB. Kami boleh coordinate penghantaran pada hari yang sama."),
            ("Ada cawangan di Johor?", "Kami mempunyai <strong>partner logistik tempatan di Johor Bahru</strong> yang membolehkan penghantaran same-day. Untuk kawasan lain di Johor, penghantaran diuruskan dari gudang utama kami dengan masa 24 jam."),
        ],
        "gallery_alts": [
            "Katil hospital 2 fungsi dipasang di rumah pelanggan di Johor Bahru",
            "Penghantaran katil hospital ke apartment di Iskandar Puteri",
            "Setup katil hospital untuk warga emas di Skudai, Johor",
            "Pemasangan katil hospital 3 fungsi di Batu Pahat",
            "Katil hospital untuk pesakit stroke di Muar, Johor",
            "Penghantaran katil hospital ke Kluang, Johor",
            "Katil hospital dengan side rails di rumah pelanggan Pasir Gudang",
            "Pemasangan percuma katil hospital di Kulai, Johor",
            "Katil hospital manual 2 fungsi siap dipasang di Pontian",
            "Penghantaran katil hospital untuk pesakit post-surgery di Segamat",
            "Sewa katil hospital untuk home care di Kota Tinggi, Johor",
            "Katil hospital dengan tilam ripple di Mersing, Johor",
        ],
    },

    "pulau-pinang": {
        "name": "Pulau Pinang",
        "state": "Pulau Pinang",
        "tier": 2,
        "delivery_time": "24 jam",
        "delivery_cost": "RM100-150",
        "distance": "Partner delivery",
        "lat": "5.4164",
        "lng": "100.3327",
        "population": "1.8 juta",
        "meta_title": "Sewa Katil Hospital Pulau Pinang | Penghantaran Seluruh Penang (2026)",
        "meta_desc": "Sewa katil hospital di Pulau Pinang dari RM150/bulan. Penghantaran ke George Town, Bayan Lepas, Butterworth. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609",
        "hero_subtitle": "Penghantaran Same-Day ke seluruh Pulau Pinang. Dipercayai sejak 2016. Tanpa Deposit.",
        "intro_paragraphs": [
            "Pulau Pinang dengan populasi lebih 1.8 juta penduduk merupakan salah satu negeri dengan populasi warga emas tertinggi di Malaysia. Kawasan seperti George Town, Bayan Lepas, Bukit Mertajam dan Butterworth mempunyai permintaan tinggi untuk katil hospital rumah kerana budaya penjagaan keluarga yang kuat di kalangan masyarakat Penang.",
            "Penang terkenal dengan hospital-hospital terkemuka seperti Penang General Hospital, Gleneagles Penang, Island Hospital dan Lam Wah Ee Hospital. Sebagai destinasi medical tourism, ramai pesakit tempatan dan antarabangsa memerlukan katil hospital untuk pemulihan selepas rawatan. Kami menyediakan penghantaran ke seluruh Penang termasuk kawasan pulau dan Seberang Perai.",
            "Dengan populasi yang semakin menua dan kos rawatan hospital swasta yang meningkat, permintaan untuk home care di Penang terus berkembang. Kami memahami cabaran logistik penghantaran ke kawasan pulau dan telah mewujudkan rangkaian penghantaran yang efisien untuk memastikan katil hospital sampai ke rumah anda dalam masa 24 jam."
        ],
        "hospitals": [
            ("Hospital Pulau Pinang (Penang GH)", "Jalan Residensi, George Town", "24 jam"),
            ("Gleneagles Hospital Penang", "Jalan Pangkor, George Town", "24 jam"),
            ("Island Hospital", "Jalan Macalister, George Town", "24 jam"),
            ("Lam Wah Ee Hospital", "Jalan Tan Sri Teh Ewe Lim, Jelutong", "24 jam"),
            ("Hospital Seberang Jaya", "Jalan Tun Hussein Onn, Seberang Jaya", "24 jam"),
        ],
        "testimonials": [
            ("Mr. Tan", "T", "George Town, Pulau Pinang", "Very good service. Delivery was on time and staff was very professional. Katil berkualiti tinggi dan harga berpatutan."),
            ("Puan Zainab", "Z", "Bayan Lepas, Pulau Pinang", "Katil hospital untuk jaga mak yang sakit. Kualiti bagus, harga berpatutan dan staff sangat membantu."),
            ("En. Ravi", "R", "Butterworth, Pulau Pinang", "Fast response, good communication. Penghantaran ke Seberang Perai pun cepat. The bed quality is excellent."),
        ],
        "coverage_areas": ["George Town", "Bayan Lepas", "Butterworth", "Bukit Mertajam", "Nibong Tebal", "Jelutong", "Tanjung Bungah", "Air Itam", "Balik Pulau", "Seberang Perai", "Kepala Batas", "Tasek Gelugor"],
        "cities": [
            ("George Town", "george-town"), ("Bayan Lepas", "bayan-lepas"), ("Butterworth", "butterworth"),
            ("Bukit Mertajam", "bukit-mertajam"), ("Nibong Tebal", "nibong-tebal"), ("Jelutong", "jelutong"),
            ("Tanjung Bungah", "tanjung-bungah"), ("Air Itam", "air-itam"), ("Balik Pulau", "balik-pulau"),
            ("Seberang Perai", "seberang-perai"), ("Kepala Batas", "kepala-batas"), ("Tasek Gelugor", "tasek-gelugor"),
        ],
        "nearby_states": [
            ("Kedah", "kedah", "Penghantaran 24 Jam"),
            ("Perak", "perak", "Penghantaran 1-2 Hari"),
            ("Perlis", "perlis", "Penghantaran 1-2 Hari"),
        ],
        "why_us_descriptions": [
            "Rangkaian delivery ke seluruh Penang - pulau dan Seberang Perai dalam 24 jam",
            "Penduduk Penang tak perlu bayar deposit. Terus sewa dari RM150/bulan sahaja",
            "Pasukan kami pasang di rumah, kondo atau landed di Penang tanpa caj tambahan",
            "Sewa bulanan. Pulangkan bila-bila masa tanpa penalti",
            "Hotline kecemasan 24 jam untuk semua pelanggan di Pulau Pinang",
            "Technician datang ke rumah anda di Penang untuk repair percuma sepanjang sewa",
        ],
        "faq": [
            ("Berapa harga sewa katil hospital di Pulau Pinang?", "Harga sewa bermula dari <strong>RM150/bulan</strong> untuk katil 2 fungsi manual. Katil 3 fungsi dari RM250/bulan. Tiada deposit diperlukan."),
            ("Berapa lama penghantaran ke Pulau Pinang?", "Penghantaran ke seluruh Pulau Pinang termasuk George Town, Bayan Lepas, Butterworth dan Bukit Mertajam dalam masa <strong>24 jam</strong> selepas pengesahan order."),
            ("Kawasan mana di Penang yang anda cover?", "Kami cover <strong>seluruh Pulau Pinang</strong> termasuk George Town, Bayan Lepas, Jelutong, Tanjung Bungah, Air Itam, Balik Pulau, Butterworth, Bukit Mertajam, Nibong Tebal, Kepala Batas dan seluruh Seberang Perai."),
            ("Hospital mana di Penang yang pesakit anda biasa discharge dari?", "Kami kerap menerima tempahan dari pesakit yang discharge dari <strong>Penang General Hospital</strong>, Gleneagles Penang, Island Hospital, Lam Wah Ee Hospital dan Hospital Seberang Jaya."),
            ("Boleh hantar ke kawasan pulau macam Tanjung Bungah dan Balik Pulau?", "Ya, kami cover <strong>semua kawasan di pulau</strong> termasuk Tanjung Bungah, Balik Pulau, Air Itam dan Batu Ferringhi. Penghantaran ke kawasan pulau biasanya sama 24 jam."),
        ],
        "gallery_alts": [
            "Katil hospital 2 fungsi dipasang di rumah pelanggan di George Town",
            "Penghantaran katil hospital ke apartment di Bayan Lepas, Penang",
            "Setup katil hospital untuk warga emas di Butterworth",
            "Pemasangan katil hospital 3 fungsi di Bukit Mertajam",
            "Katil hospital untuk pesakit stroke di Jelutong, Penang",
            "Penghantaran katil hospital ke Tanjung Bungah",
            "Katil hospital dengan side rails di Air Itam, Penang",
            "Pemasangan percuma katil hospital di Nibong Tebal",
            "Katil hospital manual 2 fungsi siap dipasang di Seberang Perai",
            "Penghantaran katil hospital untuk pesakit post-surgery di Kepala Batas",
            "Sewa katil hospital untuk home care di Balik Pulau, Penang",
            "Katil hospital dengan tilam ripple di Tasek Gelugor, Penang",
        ],
    },

    "kedah": {
        "name": "Kedah",
        "state": "Kedah",
        "tier": 2,
        "delivery_time": "24 jam",
        "delivery_cost": "RM100-150",
        "distance": "Partner delivery",
        "lat": "6.1184",
        "lng": "100.3685",
        "population": "2.2 juta",
        "meta_title": "Sewa Katil Hospital Kedah | Penghantaran Seluruh Kedah (2026)",
        "meta_desc": "Sewa katil hospital di Kedah dari RM150/bulan. Penghantaran ke Alor Setar, Sungai Petani, Kulim, Langkawi. Tanpa deposit. ☎ 011-2879 9609",
        "hero_subtitle": "Penghantaran Same-Day ke seluruh Kedah. Dipercayai sejak 2016. Tanpa Deposit.",
        "intro_paragraphs": [
            "Kedah, dikenali sebagai Jelapang Padi Malaysia dengan populasi lebih 2.2 juta penduduk, mempunyai permintaan yang stabil untuk katil hospital rumah. Kawasan bandar seperti Alor Setar, Sungai Petani dan Kulim serta kawasan pelancongan Langkawi memerlukan perkhidmatan ini terutamanya untuk penjagaan warga emas.",
            "Kedah mempunyai beberapa hospital utama termasuk Hospital Sultanah Bahiyah di Alor Setar, Hospital Sultan Abdul Halim di Sungai Petani dan KPJ Kedah. Pesakit yang discharge dari hospital-hospital ini kerap memerlukan katil hospital untuk pemulihan di rumah.",
            "Sebagai negeri pertanian utama, Kedah mempunyai populasi luar bandar yang besar. Kami memahami cabaran penghantaran ke kawasan kampung dan telah menyediakan rangkaian logistik yang meliputi semua daerah di Kedah termasuk Baling, Sik, Pendang dan Yan."
        ],
        "hospitals": [
            ("Hospital Sultanah Bahiyah", "Km 6, Jalan Langgar, Alor Setar", "24 jam"),
            ("Hospital Sultan Abdul Halim", "Jalan Lencongan Timur, Sg Petani", "24 jam"),
            ("KPJ Kedah", "Jalan Tunku Ibrahim, Alor Setar", "24 jam"),
            ("Hospital Kulim", "Jalan Mahang, Kulim", "24 jam"),
        ],
        "testimonials": [
            ("Puan Fatimah", "F", "Alor Setar, Kedah", "Katil hospital sampai hari berikutnya. Kualiti sangat bagus dan harga berpatutan. Staff pun ramah."),
            ("En. Ismail", "I", "Sungai Petani, Kedah", "Sewa katil untuk ayah yang post-surgery. Senang sangat proses dia, WhatsApp je terus settle."),
            ("Cik Hasnah", "H", "Kulim, Kedah", "Dah 4 bulan sewa, katil masih elok. Servis maintain pun bagus. Recommend!"),
        ],
        "coverage_areas": ["Alor Setar", "Sungai Petani", "Kulim", "Langkawi", "Jitra", "Baling", "Sik", "Pendang", "Yan", "Kuala Kedah", "Gurun", "Changlun"],
        "cities": [
            ("Alor Setar", "alor-setar"), ("Sungai Petani", "sungai-petani"), ("Kulim", "kulim"),
            ("Langkawi", "langkawi"), ("Jitra", "jitra"), ("Baling", "baling"),
            ("Sik", "sik"), ("Pendang", "pendang"), ("Yan", "yan"),
            ("Kuala Kedah", "kuala-kedah"), ("Gurun", "gurun"), ("Changlun", "changlun"),
        ],
        "nearby_states": [
            ("Pulau Pinang", "pulau-pinang", "Penghantaran 24 Jam"),
            ("Perlis", "perlis", "Penghantaran 24 Jam"),
            ("Perak", "perak", "Penghantaran 1-2 Hari"),
        ],
        "why_us_descriptions": [
            "Rangkaian delivery ke seluruh Kedah - Alor Setar, SP, Kulim dalam 24 jam",
            "Penduduk Kedah tak perlu bayar deposit. Terus sewa dari RM150/bulan sahaja",
            "Pasukan kami pasang di rumah anda di Kedah tanpa caj tambahan",
            "Sewa bulanan. Pulangkan bila-bila masa tanpa penalti",
            "Hotline kecemasan 24 jam untuk semua pelanggan di Kedah",
            "Technician datang ke rumah anda di Kedah untuk repair percuma sepanjang sewa",
        ],
        "faq": [
            ("Berapa harga sewa katil hospital di Kedah?", "Harga sewa bermula dari <strong>RM150/bulan</strong> untuk katil 2 fungsi manual. Katil 3 fungsi dari RM250/bulan. Tiada deposit diperlukan."),
            ("Berapa lama penghantaran ke Kedah?", "Penghantaran ke seluruh Kedah termasuk Alor Setar, Sungai Petani dan Kulim dalam masa <strong>24 jam</strong> selepas pengesahan order."),
            ("Kawasan mana di Kedah yang anda cover?", "Kami cover <strong>seluruh Kedah</strong> termasuk Alor Setar, Sungai Petani, Kulim, Langkawi, Jitra, Baling, Sik, Pendang, Yan dan Gurun."),
            ("Hospital mana di Kedah yang pesakit anda biasa discharge dari?", "Kami kerap menerima tempahan dari pesakit yang discharge dari <strong>Hospital Sultanah Bahiyah</strong>, Hospital Sultan Abdul Halim, KPJ Kedah dan Hospital Kulim."),
            ("Boleh hantar ke Langkawi?", "Ya, kami boleh hantar ke <strong>Langkawi</strong> tetapi memerlukan masa tambahan 1-2 hari kerana logistik feri. Sila hubungi untuk pengesahan."),
        ],
        "gallery_alts": [
            "Katil hospital 2 fungsi dipasang di rumah pelanggan di Alor Setar",
            "Penghantaran katil hospital ke rumah di Sungai Petani, Kedah",
            "Setup katil hospital untuk warga emas di Kulim",
            "Pemasangan katil hospital 3 fungsi di Langkawi",
            "Katil hospital untuk pesakit stroke di Jitra, Kedah",
            "Penghantaran katil hospital ke Baling, Kedah",
            "Katil hospital dengan side rails di Pendang, Kedah",
            "Pemasangan percuma katil hospital di Yan, Kedah",
            "Katil hospital manual 2 fungsi siap dipasang di Gurun",
            "Penghantaran katil hospital ke Kuala Kedah",
            "Sewa katil hospital untuk home care di Changlun, Kedah",
            "Katil hospital dengan tilam ripple di Sik, Kedah",
        ],
    },
}

# Due to the massive data required, let me define a helper to generate
# remaining states with computed data patterns

def make_state(slug, name, state, tier, delivery_time, delivery_cost, distance, lat, lng, population,
               hospitals, testimonials, coverage_areas, cities, nearby_states, intro_paragraphs):
    """Helper to create state data dict with sensible defaults."""

    tier_map = {1: "4 jam", 2: "24 jam", 3: "1-2 hari"}
    tier_hero = {
        1: f"Penghantaran Express 4 Jam. Lebih 500+ keluarga di {name} pilih kami. Tanpa Deposit.",
        2: f"Penghantaran Same-Day ke seluruh {name}. Dipercayai sejak 2016. Tanpa Deposit.",
        3: f"Penghantaran ke {name} dan seluruh {state}. Katil hospital terus ke rumah. Tanpa Deposit.",
    }

    tier_meta_state = {
        1: f"Sewa Katil Hospital {name} | Penghantaran Seluruh {name} (2026)",
        2: f"Sewa Katil Hospital {name} | Penghantaran Seluruh {name} (2026)",
        3: f"Sewa Katil Hospital {name} | Penghantaran ke {name} (2026)",
    }

    areas_str = ", ".join(coverage_areas[:4])
    meta_desc = f"Sewa katil hospital di {name} dari RM150/bulan. Penghantaran ke {areas_str}. Tanpa deposit, pemasangan percuma. ☎ 011-2879 9609"
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."

    why_us = [
        f"{'Gudang berdekatan' if tier == 1 else 'Rangkaian delivery'} - katil sampai ke {coverage_areas[0]} dalam {delivery_time}",
        f"Penduduk {name} tak perlu bayar deposit. Terus sewa dari RM150/bulan sahaja",
        f"Pasukan kami pasang di rumah anda di {name} tanpa caj tambahan",
        "Sewa bulanan. Pulangkan bila-bila masa tanpa penalti",
        f"Hotline kecemasan 24 jam untuk semua pelanggan di {name}",
        f"Technician datang ke rumah anda di {name} untuk repair percuma sepanjang sewa",
    ]

    hosp_names = [h[0] for h in hospitals]
    hosp_str = ", ".join(hosp_names[:3])
    areas_full = ", ".join(coverage_areas)

    faq = [
        (f"Berapa harga sewa katil hospital di {name}?", f"Harga sewa bermula dari <strong>RM150/bulan</strong> untuk katil 2 fungsi manual. Katil 3 fungsi dari RM250/bulan. Tiada deposit diperlukan."),
        (f"Berapa lama penghantaran ke {name}?", f"Penghantaran ke seluruh {name} dalam masa <strong>{delivery_time}</strong> selepas pengesahan order."),
        (f"Kawasan mana di {name} yang anda cover?", f"Kami cover <strong>seluruh {name}</strong> termasuk {areas_full}."),
        (f"Hospital mana di {name} yang pesakit anda biasa discharge dari?", f"Kami kerap menerima tempahan dari pesakit yang discharge dari <strong>{hosp_names[0]}</strong>, {hosp_str}. Kami boleh coordinate penghantaran."),
    ]

    gallery_alts = []
    for i, area in enumerate(coverage_areas[:12]):
        descs = [
            f"Katil hospital 2 fungsi dipasang di rumah pelanggan di {area}",
            f"Penghantaran katil hospital ke {area}, {name}",
            f"Setup katil hospital untuk warga emas di {area}",
            f"Pemasangan katil hospital 3 fungsi di {area}",
            f"Katil hospital untuk pesakit stroke di {area}, {name}",
            f"Sewa katil hospital untuk home care di {area}",
            f"Katil hospital dengan side rails di {area}",
            f"Pemasangan percuma katil hospital di {area}",
            f"Katil hospital manual siap dipasang di {area}",
            f"Penghantaran katil hospital ke {area}",
            f"Katil hospital dengan tilam ripple di {area}",
            f"Servis katil hospital di rumah pelanggan {area}",
        ]
        gallery_alts.append(descs[i % len(descs)])
    while len(gallery_alts) < 12:
        gallery_alts.append(f"Penghantaran katil hospital di {name}")

    return {
        "name": name,
        "state": state,
        "tier": tier,
        "delivery_time": delivery_time,
        "delivery_cost": delivery_cost,
        "distance": distance,
        "lat": lat,
        "lng": lng,
        "population": population,
        "meta_title": tier_meta_state[tier],
        "meta_desc": meta_desc,
        "hero_subtitle": tier_hero[tier],
        "intro_paragraphs": intro_paragraphs,
        "hospitals": hospitals,
        "testimonials": testimonials,
        "coverage_areas": coverage_areas,
        "cities": cities,
        "nearby_states": nearby_states,
        "why_us_descriptions": why_us,
        "faq": faq,
        "gallery_alts": gallery_alts,
    }


# Add remaining states
STATES["kelantan"] = make_state("kelantan", "Kelantan", "Kelantan", 2, "24 jam", "RM100-150", "Partner delivery", "6.1256", "102.2385", "1.9 juta",
    [("Hospital Raja Perempuan Zainab II", "Kota Bharu", "24 jam"), ("KPJ Perdana Specialist Hospital", "Kota Bharu", "24 jam"), ("Hospital Universiti Sains Malaysia", "Kubang Kerian", "24 jam"), ("Hospital Tanah Merah", "Tanah Merah", "24 jam")],
    [("Puan Rohani", "R", "Kota Bharu, Kelantan", "Katil hospital sampai cepat. Kualiti bagus dan staff sangat membantu. Terima kasih banyak!"), ("En. Yusof", "Y", "Pasir Mas, Kelantan", "Sewa katil untuk ibu yang sakit. Proses mudah, harga OK. Recommended!"), ("Cik Nadia", "N", "Kuala Krai, Kelantan", "Service bagus walaupun jauh. Katil berkualiti dan penghantaran on time.")],
    ["Kota Bharu", "Pasir Mas", "Tanah Merah", "Machang", "Kuala Krai", "Tumpat", "Bachok", "Pasir Puteh", "Gua Musang", "Jeli", "Rantau Panjang"],
    [("Kota Bharu", "kota-bharu"), ("Pasir Mas", "pasir-mas"), ("Tanah Merah", "tanah-merah"), ("Machang", "machang"), ("Kuala Krai", "kuala-krai"), ("Tumpat", "tumpat"), ("Bachok", "bachok"), ("Pasir Puteh", "pasir-puteh"), ("Gua Musang", "gua-musang"), ("Jeli", "jeli"), ("Rantau Panjang", "rantau-panjang")],
    [("Terengganu", "terengganu", "Penghantaran 24 Jam"), ("Pahang", "pahang", "Penghantaran 1-2 Hari"), ("Kedah", "kedah", "Penghantaran 1-2 Hari")],
    ["Kelantan, negeri di pantai timur Semenanjung Malaysia dengan populasi lebih 1.9 juta penduduk, mempunyai permintaan yang stabil untuk katil hospital rumah. Kota Bharu sebagai ibu negeri merupakan pusat utama permintaan, diikuti Pasir Mas, Tanah Merah dan kawasan pedalaman seperti Gua Musang.",
     "Kelantan mempunyai beberapa hospital utama termasuk Hospital Raja Perempuan Zainab II, KPJ Perdana dan Hospital USM di Kubang Kerian. Pesakit yang discharge dari hospital-hospital ini kerap memerlukan katil hospital untuk pemulihan di rumah. Budaya penjagaan keluarga yang kuat di Kelantan menjadikan perkhidmatan ini sangat diperlukan.",
     "Sebagai negeri dengan populasi luar bandar yang besar, kami memahami cabaran penghantaran ke kawasan kampung di Kelantan. Rangkaian logistik kami meliputi semua daerah termasuk Gua Musang dan Jeli yang terletak jauh dari bandar utama."]
)

STATES["perak"] = make_state("perak", "Perak", "Perak", 2, "24 jam", "RM80-120", "Partner delivery", "4.5921", "101.0901", "2.5 juta",
    [("Hospital Raja Permaisuri Bainun", "Jalan Raja Ashman Shah, Ipoh", "24 jam"), ("KPJ Ipoh Specialist Hospital", "Jalan Raja Dihilir, Ipoh", "24 jam"), ("Hospital Taiping", "Jalan Taming Sari, Taiping", "24 jam"), ("Hospital Seri Manjung", "Seri Manjung", "24 jam"), ("Hospital Teluk Intan", "Teluk Intan", "24 jam")],
    [("Puan Mariam", "M", "Ipoh, Perak", "Katil hospital sampai next day. Staff tolong pasang dan ajar guna. Sangat puas hati!"), ("En. Rajan", "R", "Taiping, Perak", "Sewa katil untuk bapa yang stroke. Kualiti baik, harga berpatutan. Thank you!"), ("Cik Aini", "A", "Teluk Intan, Perak", "Walaupun jauh dari KL, penghantaran tetap cepat. Service maintain pun bagus.")],
    ["Ipoh", "Taiping", "Teluk Intan", "Seri Manjung", "Lumut", "Kampar", "Kuala Kangsar", "Batu Gajah", "Sitiawan", "Slim River", "Tanjung Malim", "Gerik", "Gopeng"],
    [("Ipoh", "ipoh"), ("Taiping", "taiping"), ("Teluk Intan", "teluk-intan"), ("Seri Manjung", "seri-manjung"), ("Lumut", "lumut"), ("Kampar", "kampar"), ("Kuala Kangsar", "kuala-kangsar"), ("Batu Gajah", "batu-gajah"), ("Sitiawan", "sitiawan"), ("Slim River", "slim-river"), ("Tanjung Malim", "tanjung-malim"), ("Gerik", "gerik"), ("Gopeng", "gopeng"), ("Cameron Highlands", "cameron-highlands")],
    [("Selangor", "selangor", "Penghantaran 4 Jam"), ("Kedah", "kedah", "Penghantaran 1-2 Hari"), ("Pulau Pinang", "pulau-pinang", "Penghantaran 1-2 Hari"), ("Pahang", "pahang", "Penghantaran 1-2 Hari")],
    ["Perak, negeri kedua terbesar di Semenanjung Malaysia dengan populasi lebih 2.5 juta penduduk, mempunyai Ipoh sebagai ibu negeri yang menjadi pusat utama permintaan katil hospital. Kawasan lain seperti Taiping, Teluk Intan, Kampar dan Lumut juga mempunyai permintaan yang stabil.",
     "Perak mempunyai hospital-hospital utama seperti Hospital Raja Permaisuri Bainun di Ipoh, KPJ Ipoh Specialist dan Hospital Taiping. Pesakit post-surgery dan warga emas yang discharge dari hospital-hospital ini kerap memerlukan katil hospital untuk pemulihan di rumah.",
     "Walaupun Perak terletak lebih jauh dari gudang utama kami, rangkaian logistik kami membolehkan penghantaran dalam masa 24 jam ke kebanyakan kawasan di Perak. Kawasan selatan Perak seperti Tanjung Malim dan Slim River boleh dicapai lebih cepat kerana berdekatan dengan Selangor."]
)

STATES["pahang"] = make_state("pahang", "Pahang", "Pahang", 2, "24 jam", "RM80-120", "Partner delivery", "3.8126", "103.3256", "1.7 juta",
    [("Hospital Tengku Ampuan Afzan", "Jalan Tanah Putih, Kuantan", "24 jam"), ("KPJ Pahang Specialist Hospital", "Kuantan", "24 jam"), ("Hospital Temerloh", "Temerloh", "24 jam"), ("Hospital Sultan Haji Ahmad Shah", "Temerloh", "24 jam")],
    [("Puan Azizah", "A", "Kuantan, Pahang", "Katil hospital sampai next day. Sangat cepat untuk kawasan Pahang. Kualiti pun terbaik!"), ("En. Kamal", "K", "Temerloh, Pahang", "Sewa katil untuk ibu yang bedridden. Proses senang dan harga OK."), ("Cik Hidayah", "H", "Bentong, Pahang", "Bentong dekat dengan KL, penghantaran cepat. Katil berkualiti!")],
    ["Kuantan", "Temerloh", "Bentong", "Raub", "Jerantut", "Pekan", "Rompin", "Maran", "Lipis", "Cameron Highlands", "Mentakab", "Bera"],
    [("Kuantan", "kuantan"), ("Temerloh", "temerloh"), ("Bentong", "bentong"), ("Raub", "raub"), ("Jerantut", "jerantut"), ("Pekan", "pekan"), ("Rompin", "rompin"), ("Maran", "maran"), ("Lipis", "lipis"), ("Cameron Highlands", "cameron-highlands"), ("Mentakab", "mentakab"), ("Bera", "bera")],
    [("Selangor", "selangor", "Penghantaran 4 Jam"), ("Terengganu", "terengganu", "Penghantaran 1-2 Hari"), ("Kelantan", "kelantan", "Penghantaran 1-2 Hari"), ("Negeri Sembilan", "negeri-sembilan", "Penghantaran 1-2 Hari")],
    ["Pahang, negeri terbesar di Semenanjung Malaysia dengan populasi lebih 1.7 juta penduduk, meliputi kawasan dari pantai timur Kuantan hingga ke kawasan tanah tinggi Cameron Highlands. Kuantan sebagai ibu negeri merupakan pusat utama permintaan katil hospital.",
     "Hospital utama di Pahang termasuk Hospital Tengku Ampuan Afzan di Kuantan dan Hospital Temerloh. Pesakit yang discharge dari hospital-hospital ini memerlukan katil hospital untuk pemulihan di rumah. Kawasan Bentong yang berdekatan KL menerima penghantaran lebih cepat.",
     "Pahang mempunyai kawasan yang luas termasuk pedalaman, namun rangkaian logistik kami meliputi semua daerah utama. Kawasan barat Pahang seperti Bentong dan Raub boleh dicapai dalam masa 4-6 jam dari gudang kami di Batu Caves."]
)

STATES["terengganu"] = make_state("terengganu", "Terengganu", "Terengganu", 2, "24 jam", "RM100-150", "Partner delivery", "5.3117", "103.1324", "1.3 juta",
    [("Hospital Sultanah Nur Zahirah", "Kuala Terengganu", "24 jam"), ("KPJ Terengganu Specialist Hospital", "Kuala Terengganu", "24 jam"), ("Hospital Kemaman", "Kemaman", "24 jam"), ("Hospital Dungun", "Dungun", "24 jam")],
    [("Puan Salma", "S", "Kuala Terengganu", "Katil hospital sampai tepat masa. Staff sangat professional dan ramah."), ("En. Zaidi", "Z", "Kemaman, Terengganu", "Sewa untuk bapa yang post-surgery. Kualiti katil bagus, proses mudah."), ("Cik Aina", "A", "Dungun, Terengganu", "Penghantaran ke Dungun cepat. Harga berpatutan dan servis terbaik.")],
    ["Kuala Terengganu", "Kemaman", "Dungun", "Marang", "Besut", "Setiu", "Hulu Terengganu", "Kuala Nerus", "Chukai", "Paka"],
    [("Kuala Terengganu", "kuala-terengganu"), ("Kemaman", "kemaman"), ("Dungun", "dungun"), ("Marang", "marang"), ("Besut", "besut"), ("Setiu", "setiu"), ("Hulu Terengganu", "hulu-terengganu"), ("Kuala Nerus", "kuala-nerus"), ("Chukai", "chukai"), ("Paka", "paka")],
    [("Kelantan", "kelantan", "Penghantaran 24 Jam"), ("Pahang", "pahang", "Penghantaran 1-2 Hari")],
    ["Terengganu, negeri pantai timur dengan populasi lebih 1.3 juta penduduk, mempunyai Kuala Terengganu sebagai pusat utama permintaan katil hospital. Kawasan lain seperti Kemaman, Dungun dan Besut juga mempunyai permintaan yang stabil terutamanya untuk penjagaan warga emas.",
     "Hospital utama di Terengganu termasuk Hospital Sultanah Nur Zahirah dan KPJ Terengganu Specialist. Pesakit yang discharge dari hospital-hospital ini kerap memerlukan katil hospital untuk pemulihan di rumah.",
     "Terengganu mempunyai kawasan pesisir pantai yang panjang. Kami menyediakan penghantaran ke semua bandar utama di sepanjang pantai dari Besut di utara hingga Kemaman di selatan, serta kawasan pedalaman Hulu Terengganu."]
)

STATES["melaka"] = make_state("melaka", "Melaka", "Melaka", 2, "24 jam", "RM80-100", "Partner delivery", "2.1896", "102.2501", "930,000",
    [("Hospital Melaka", "Jalan Mufti Haji Khalil, Melaka", "24 jam"), ("Mahkota Medical Centre", "Jalan Merdeka, Melaka", "24 jam"), ("Pantai Hospital Ayer Keroh", "Ayer Keroh, Melaka", "24 jam"), ("Oriental Melaka Straits Medical Centre", "Klebang, Melaka", "24 jam")],
    [("Puan Rahimah", "R", "Melaka Tengah", "Katil hospital sampai cepat. Harga murah dan kualiti terjamin. Sangat puas hati!"), ("En. Chong", "C", "Ayer Keroh, Melaka", "Sewa untuk mak yang elderly. Katil senang adjust dan staff helpful."), ("Cik Suria", "S", "Alor Gajah, Melaka", "Penghantaran ke Alor Gajah pun smooth. Terima kasih atas servis yang bagus!")],
    ["Melaka Tengah", "Ayer Keroh", "Alor Gajah", "Jasin", "Masjid Tanah", "Klebang", "Bukit Baru", "Bukit Katil", "Bukit Rambai", "Krubong", "Tanjung Kling"],
    [("Melaka Tengah", "melaka-tengah"), ("Ayer Keroh", "ayer-keroh"), ("Alor Gajah", "alor-gajah"), ("Jasin", "jasin"), ("Masjid Tanah", "masjid-tanah"), ("Klebang", "klebang"), ("Bukit Baru", "bukit-baru"), ("Bukit Katil", "bukit-katil"), ("Bukit Rambai", "bukit-rambai"), ("Krubong", "krubong"), ("Tanjung Kling", "tanjung-kling")],
    [("Negeri Sembilan", "negeri-sembilan", "Penghantaran 24 Jam"), ("Johor", "johor", "Penghantaran 24 Jam"), ("Selangor", "selangor", "Penghantaran 1-2 Hari")],
    ["Melaka, negeri bersejarah dengan populasi lebih 930,000 penduduk, merupakan salah satu negeri terkecil di Malaysia tetapi mempunyai permintaan yang stabil untuk katil hospital rumah. Bandar Melaka, Ayer Keroh dan Alor Gajah merupakan kawasan utama yang memerlukan perkhidmatan ini.",
     "Melaka terkenal dengan hospital-hospital seperti Hospital Melaka, Mahkota Medical Centre dan Pantai Hospital Ayer Keroh. Sebagai destinasi medical tourism, ramai pesakit memerlukan katil hospital untuk pemulihan selepas rawatan di hospital-hospital ini.",
     "Kedudukannya di antara KL dan JB memudahkan logistik penghantaran. Kami boleh menghantar ke seluruh Melaka dalam masa 24 jam melalui rangkaian logistik yang efisien."]
)

STATES["negeri-sembilan"] = make_state("negeri-sembilan", "Negeri Sembilan", "Negeri Sembilan", 2, "24 jam", "RM50-80", "~60 km dari gudang", "2.7258", "101.9424", "1.1 juta",
    [("Hospital Tuanku Ja'afar", "Jalan Rasah, Seremban", "4-6 jam"), ("KPJ Seremban Specialist Hospital", "Jalan Toman, Seremban", "4-6 jam"), ("Columbia Asia Hospital Seremban", "Seremban", "4-6 jam"), ("Hospital Port Dickson", "Port Dickson", "6-8 jam")],
    [("Puan Kamariah", "K", "Seremban, N. Sembilan", "Katil hospital sampai petang tu juga. Sangat cepat sebab dekat dengan KL!"), ("En. Suresh", "S", "Nilai, N. Sembilan", "Sewa katil untuk ayah yang post-surgery. Service terbaik, harga berpatutan."), ("Cik Izzah", "I", "Port Dickson, N. Sembilan", "Penghantaran ke PD pun cepat. Katil berkualiti dan staff professional.")],
    ["Seremban", "Nilai", "Port Dickson", "Bahau", "Kuala Pilah", "Tampin", "Rembau", "Jelebu", "Senawang", "Mantin", "Labu"],
    [("Seremban", "seremban"), ("Nilai", "nilai"), ("Port Dickson", "port-dickson"), ("Bahau", "bahau"), ("Kuala Pilah", "kuala-pilah"), ("Tampin", "tampin"), ("Rembau", "rembau"), ("Jelebu", "jelebu"), ("Senawang", "senawang"), ("Mantin", "mantin"), ("Labu", "labu"), ("Gemas", "gemas")],
    [("Selangor", "selangor", "Penghantaran 4 Jam"), ("Kuala Lumpur", "kuala-lumpur", "Penghantaran 4 Jam"), ("Melaka", "melaka", "Penghantaran 24 Jam"), ("Johor", "johor", "Penghantaran 1-2 Hari")],
    ["Negeri Sembilan dengan populasi lebih 1.1 juta penduduk terletak strategik bersebelahan Selangor dan KL. Seremban sebagai ibu negeri hanya 60 km dari gudang kami, menjadikan penghantaran lebih pantas berbanding negeri-negeri lain di luar Lembah Klang.",
     "Hospital utama di Negeri Sembilan termasuk Hospital Tuanku Ja'afar, KPJ Seremban dan Columbia Asia Seremban. Pesakit yang discharge dari hospital-hospital ini memerlukan katil hospital untuk pemulihan. Kedekatan dengan KL membolehkan kami menghantar dalam masa 4-6 jam ke Seremban.",
     "Negeri Sembilan meliputi kawasan dari Seremban di utara hingga Port Dickson di selatan dan Kuala Pilah di pedalaman. Kami menyediakan penghantaran ke semua daerah di Negeri Sembilan."]
)

STATES["perlis"] = make_state("perlis", "Perlis", "Perlis", 3, "1-2 hari", "RM120-150", "Partner delivery", "6.4414", "100.1986", "260,000",
    [("Hospital Tuanku Fauziah", "Jalan Tun Abdul Razak, Kangar", "1-2 hari"), ("Klinik Kesihatan Kangar", "Kangar", "1-2 hari"), ("Klinik Kesihatan Arau", "Arau", "1-2 hari")],
    [("Puan Noor", "N", "Kangar, Perlis", "Katil hospital sampai dalam 2 hari. Kualiti bagus dan harga berpatutan."), ("En. Razak", "R", "Arau, Perlis", "Sewa untuk bapa yang elderly. Proses mudah walaupun jauh dari KL."), ("Cik Syafiqah", "S", "Padang Besar, Perlis", "Service bagus, katil berkualiti. Terima kasih!")],
    ["Kangar", "Arau", "Padang Besar", "Kuala Perlis", "Beseri", "Kaki Bukit", "Simpang Empat", "Sanglang", "Wang Kelian"],
    [("Kangar", "kangar"), ("Arau", "arau"), ("Padang Besar", "padang-besar"), ("Kuala Perlis", "kuala-perlis"), ("Beseri", "beseri"), ("Kaki Bukit", "kaki-bukit"), ("Simpang Empat", "simpang-empat"), ("Sanglang", "sanglang"), ("Wang Kelian", "wang-kelian")],
    [("Kedah", "kedah", "Penghantaran 24 Jam"), ("Pulau Pinang", "pulau-pinang", "Penghantaran 1-2 Hari")],
    ["Perlis, negeri terkecil di Malaysia dengan populasi sekitar 260,000 penduduk, mempunyai Kangar sebagai ibu negeri dan pusat utama permintaan katil hospital. Walaupun kecil, penduduk Perlis tetap memerlukan perkhidmatan katil hospital untuk penjagaan warga emas dan pesakit di rumah.",
     "Hospital Tuanku Fauziah di Kangar merupakan hospital utama di Perlis. Pesakit yang discharge dari hospital ini serta dari hospital-hospital di Kedah yang bersempadan kerap memerlukan katil hospital untuk pemulihan di rumah.",
     "Saiz Perlis yang kecil bermakna penghantaran ke semua kawasan boleh dilakukan dengan cepat setelah katil tiba di negeri ini. Kami menyediakan penghantaran ke seluruh Perlis termasuk kawasan sempadan seperti Padang Besar dan Wang Kelian."]
)

STATES["sabah"] = make_state("sabah", "Sabah", "Sabah", 3, "1-2 hari", "RM150-200", "Cawangan Kota Kinabalu", "5.9804", "116.0735", "3.9 juta",
    [("Hospital Queen Elizabeth", "Jalan Penampang, Kota Kinabalu", "Same day"), ("Gleneagles Kota Kinabalu", "Riverson Walk, KK", "Same day"), ("KPJ Sabah Specialist Hospital", "Damai, KK", "Same day"), ("Hospital Duchess of Kent", "Sandakan", "1-2 hari"), ("Hospital Tawau", "Tawau", "1-2 hari")],
    [("Puan Rosita", "R", "Kota Kinabalu, Sabah", "Ada cawangan di KK, katil sampai hari yang sama. Sangat memudahkan!"), ("En. William", "W", "Sandakan, Sabah", "Penghantaran ke Sandakan smooth. Katil berkualiti dan harga berpatutan."), ("Cik Azura", "A", "Tawau, Sabah", "Jauh dari KL tapi service tetap bagus. Katil hospital berkualiti tinggi.")],
    ["Kota Kinabalu", "Sandakan", "Tawau", "Lahad Datu", "Keningau", "Beaufort", "Ranau", "Kudat", "Semporna", "Papar", "Tuaran", "Tambunan", "Kota Belud"],
    [("Kota Kinabalu", "kota-kinabalu"), ("Sandakan", "sandakan"), ("Tawau", "tawau"), ("Lahad Datu", "lahad-datu"), ("Keningau", "keningau"), ("Beaufort", "beaufort"), ("Ranau", "ranau"), ("Kudat", "kudat"), ("Semporna", "semporna"), ("Papar", "papar"), ("Tuaran", "tuaran"), ("Tambunan", "tambunan"), ("Kota Belud", "kota-belud"), ("Kunak", "kunak")],
    [("Sarawak", "sarawak", "Penghantaran 1-2 Hari"), ("Labuan", "labuan", "Penghantaran 1-2 Hari")],
    ["Sabah, negeri kedua terbesar di Malaysia dengan populasi lebih 3.9 juta penduduk, mempunyai cawangan kami di Kota Kinabalu untuk memudahkan penghantaran ke seluruh negeri. KK sebagai ibu negeri merupakan pusat utama permintaan, diikuti Sandakan, Tawau dan bandar-bandar utama lain.",
     "Sabah mempunyai hospital-hospital utama seperti Hospital Queen Elizabeth, Gleneagles KK dan KPJ Sabah. Dengan cawangan di Lot No 23A, Lorong Bizhub Bandar Sierra, Mile 13.5 Jalan Tuaran, kami boleh menyediakan penghantaran same-day ke kawasan Kota Kinabalu dan sekitar.",
     "Untuk kawasan luar KK seperti Sandakan, Tawau, Lahad Datu dan Keningau, penghantaran biasanya mengambil masa 1-2 hari. Kami memahami cabaran geografi Sabah dan telah mewujudkan rangkaian logistik yang meliputi semua bandar utama di negeri ini."]
)

STATES["sarawak"] = make_state("sarawak", "Sarawak", "Sarawak", 3, "1-2 hari", "RM150-200", "Partner delivery", "1.5533", "110.3592", "2.9 juta",
    [("Hospital Umum Sarawak", "Jalan Hospital, Kuching", "1-2 hari"), ("KPJ Kuching Specialist Hospital", "Jalan Stutong, Kuching", "1-2 hari"), ("Normah Medical Specialist Centre", "Jalan Tun Abdul Rahman Yaakub, Kuching", "1-2 hari"), ("Hospital Sibu", "Sibu", "2-3 hari"), ("Hospital Miri", "Miri", "2-3 hari")],
    [("En. James", "J", "Kuching, Sarawak", "Katil hospital sampai dalam 2 hari. Kualiti sangat bagus untuk harga yang ditawarkan."), ("Puan Dayang", "D", "Sibu, Sarawak", "Sewa untuk ibu yang bedridden. Penghantaran ke Sibu pun smooth. Terima kasih!"), ("Cik Linda", "L", "Miri, Sarawak", "Walaupun jauh, katil sampai dalam keadaan baik. Service professional.")],
    ["Kuching", "Sibu", "Miri", "Bintulu", "Sri Aman", "Kapit", "Sarikei"],
    [("Kuching", "kuching"), ("Sibu", "sibu"), ("Miri", "miri"), ("Bintulu", "bintulu"), ("Sri Aman", "sri-aman"), ("Kapit", "kapit")],
    [("Sabah", "sabah", "Penghantaran 1-2 Hari"), ("Labuan", "labuan", "Penghantaran 1-2 Hari")],
    ["Sarawak, negeri terbesar di Malaysia dengan populasi lebih 2.9 juta penduduk, mempunyai Kuching sebagai ibu negeri dan pusat utama permintaan katil hospital. Bandar-bandar utama lain seperti Sibu, Miri dan Bintulu juga mempunyai permintaan yang stabil.",
     "Hospital utama di Sarawak termasuk Hospital Umum Sarawak, KPJ Kuching dan Normah Medical Specialist Centre. Pesakit yang discharge dari hospital-hospital ini memerlukan katil hospital untuk pemulihan di rumah.",
     "Sarawak mempunyai geografi yang unik dengan sungai-sungai besar yang memisahkan bandar-bandar utama. Kami menyediakan penghantaran melalui rangkaian logistik yang merangkumi semua bandar utama di Sarawak, walaupun masa penghantaran mungkin lebih lama untuk kawasan pedalaman."]
)

STATES["labuan"] = make_state("labuan", "Labuan", "Wilayah Persekutuan Labuan", 3, "1-2 hari", "RM150-200", "Via Kota Kinabalu", "5.2831", "115.2308", "100,000",
    [("Hospital Labuan", "Jalan Tanjung Purun, Labuan", "1-2 hari"), ("Klinik Kesihatan Labuan", "Labuan", "1-2 hari")],
    [("Puan Hasnita", "H", "Labuan Town", "Katil hospital sampai dalam 2 hari. Walaupun pulau, service tetap bagus!"), ("En. Azman", "A", "Labuan", "Sewa untuk bapa yang elderly. Kualiti OK dan harga berpatutan."), ("Cik Jenny", "J", "Labuan", "Proses mudah, staff helpful. Recommend untuk penduduk Labuan!")],
    ["Labuan Town", "Victoria", "Layang-Layangan", "Patau-Patau", "Pohon Batu", "Rancha-Rancha", "Bebuloh"],
    [("Labuan Town", "labuan-town"), ("Victoria", "victoria"), ("Layang-Layangan", "layang-layangan"), ("Patau-Patau", "patau-patau"), ("Pohon Batu", "pohon-batu"), ("Rancha-Rancha", "rancha-rancha"), ("Bebuloh", "bebuloh")],
    [("Sabah", "sabah", "Penghantaran 1-2 Hari"), ("Sarawak", "sarawak", "Penghantaran 1-2 Hari")],
    ["Labuan, Wilayah Persekutuan yang terletak di luar pantai Sabah dengan populasi sekitar 100,000 penduduk, merupakan pulau yang memerlukan logistik khas untuk penghantaran katil hospital. Walaupun kecil, permintaan untuk katil hospital tetap ada terutamanya untuk penjagaan warga emas.",
     "Hospital Labuan merupakan hospital utama di pulau ini. Pesakit yang memerlukan rawatan lanjutan biasanya dirujuk ke hospital di Kota Kinabalu, dan apabila pulang memerlukan katil hospital untuk pemulihan di rumah.",
     "Penghantaran ke Labuan diuruskan melalui cawangan kami di Kota Kinabalu. Katil dihantar melalui feri ke Labuan dengan masa penghantaran 1-2 hari selepas pengesahan order."]
)

STATES["putrajaya"] = make_state("putrajaya", "Putrajaya", "Wilayah Persekutuan Putrajaya", 1, "4 jam", "RM50", "~35 km dari gudang", "2.9264", "101.6964", "110,000",
    [("Hospital Putrajaya", "Presint 7, Putrajaya", "2-3 jam"), ("Klinik Kesihatan Putrajaya", "Presint 9, Putrajaya", "2-3 jam"), ("KPJ Putrajaya Specialist Hospital", "Presint 7, Putrajaya", "2-3 jam")],
    [("Puan Nadia", "N", "Presint 16, Putrajaya", "Katil hospital sampai petang tu juga! Sangat cepat sebab dekat dengan gudang."), ("En. Rizal", "R", "Presint 9, Putrajaya", "Sewa untuk mak yang post-surgery. Service terbaik, harga berpatutan."), ("Cik Alia", "A", "Presint 11, Putrajaya", "Staff professional dan ramah. Katil berkualiti. Highly recommend!")],
    ["Presint 1-18", "Cyberjaya", "Dengkil"],
    [("Cyberjaya", "cyberjaya")],
    [("Selangor", "selangor", "Penghantaran 4 Jam"), ("Kuala Lumpur", "kuala-lumpur", "Penghantaran 4 Jam"), ("Negeri Sembilan", "negeri-sembilan", "Penghantaran 24 Jam")],
    ["Putrajaya, pusat pentadbiran kerajaan Malaysia dengan populasi sekitar 110,000 penduduk, merupakan Wilayah Persekutuan yang terletak di antara KL dan Seremban. Walaupun populasi tidak besar, permintaan untuk katil hospital datang terutamanya dari kakitangan kerajaan yang menjaga ahli keluarga di rumah.",
     "Hospital Putrajaya dan KPJ Putrajaya Specialist Hospital merupakan hospital utama di kawasan ini. Pesakit yang discharge memerlukan katil hospital untuk pemulihan di rumah. Lokasinya yang hanya 35 km dari gudang kami di Batu Caves membolehkan penghantaran express 4 jam.",
     "Putrajaya mempunyai infrastruktur moden dengan lebuh raya yang baik memudahkan penghantaran ke semua presint. Kami juga meliputi Cyberjaya yang bersebelahan."]
)


# ============================================================
# HTML TRANSFORMATION FUNCTIONS
# ============================================================

def transform_page(slug, data):
    """Transform an existing state page with unique content."""
    filepath = os.path.join(BASE_DIR, f"katil-hospital-{slug}.html")

    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    name = data["name"]
    state = data["state"]

    # 1. Update meta title
    html = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{data["meta_title"]}</title>',
        html
    )
    html = re.sub(
        r'<meta name="title" content="[^"]+">',
        f'<meta name="title" content="{data["meta_title"]}">',
        html
    )

    # 2. Update meta description
    html = re.sub(
        r'<meta name="description" content="[^"]+">',
        f'<meta name="description" content="{data["meta_desc"]}">',
        html
    )

    # 3. Update OG tags
    html = re.sub(
        r'<meta property="og:title" content="[^"]+">',
        f'<meta property="og:title" content="{data["meta_title"]}">',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]+">',
        f'<meta property="og:description" content="{data["meta_desc"]}">',
        html
    )

    # 4. Add location-pages.css
    if 'location-pages.css' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="/css/style.min.css">',
            '<link rel="stylesheet" href="/css/style.min.css">\n    <link rel="stylesheet" href="/css/location-pages.css">'
        )

    # 5. Fix schema addressRegion + add addressLocality
    html = re.sub(
        r'"address":\s*\{\s*"@type":\s*"PostalAddress",\s*"addressRegion":\s*"[^"]+",\s*"addressCountry":\s*"MY"\s*\}',
        f'''"address": {{
                "@type": "PostalAddress",
                "addressLocality": "{name}",
                "addressRegion": "{state}",
                "addressCountry": "MY"
            }}''',
        html
    )

    # 6. Update hero subtitle
    html = re.sub(
        r'<p class="hero-subtitle">\s*[^<]+\s*</p>',
        f'<p class="hero-subtitle">\n                            {data["hero_subtitle"]}\n                        </p>',
        html
    )

    # 7. Remove inline mobile CSS block (the large <style> block before </head>)
    html = re.sub(
        r'\s*<!-- Mobile Styles -->\s*<style>\s*@media \(max-width: 768px\) \{.*?\}\s*</style>\s*</head>',
        '\n</head>',
        html,
        flags=re.DOTALL
    )

    # 8. Remove inline product carousel CSS
    html = re.sub(
        r'\s*<style>\s*\.product-carousel-container\s*\{.*?</style>',
        '',
        html,
        flags=re.DOTALL
    )

    # 9. Remove inline FAQ CSS
    html = re.sub(
        r'\s*<style>\s*\.faq-item summary\s*\{[^<]*</style>',
        '',
        html
    )

    # 10. Add breadcrumb after header
    if 'breadcrumb-nav' not in html:
        breadcrumb = f'''
    <!-- Breadcrumb -->
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <div class="container">
            <a href="/">Utama</a>
            <span class="separator">›</span>
            <span class="current">{name}</span>
        </div>
    </nav>
'''
        html = html.replace(
            '    <!-- Main Content -->\n    <main id="main-content" role="main">',
            breadcrumb + '\n    <!-- Main Content -->\n    <main id="main-content" role="main">'
        )

    # 11. Add local intro section after hero
    intro_paras = "\n".join([
        f'                    <p style="color: #475569; font-size: 1rem; line-height: 1.8; margin-bottom: 16px;">\n                        {p}\n                    </p>'
        for p in data["intro_paragraphs"]
    ])

    local_intro = f'''
        <!-- Local Intro Section -->
        <section class="local-intro" style="background: #ffffff; padding: 60px 0;">
            <div class="container">
                <div style="max-width: 900px; margin: 0 auto;">
                    <h2 style="color: #1e4a9e; font-size: 1.8rem; margin-bottom: 20px;">
                        Perkhidmatan Sewa Katil Hospital di {name}
                    </h2>
{intro_paras}
                </div>
            </div>
        </section>

'''

    if 'local-intro' not in html:
        html = html.replace(
            '        <!-- Services Section -->',
            local_intro + '        <!-- Services Section -->'
        )

    # 12. Update Why Choose Us descriptions
    why_titles = ["Penghantaran", "Tanpa Deposit", "Pemasangan Percuma", "Tiada Kontrak", "Sokongan 24/7", "Servis Percuma"]
    for i, title_keyword in enumerate(why_titles):
        if i < len(data["why_us_descriptions"]):
            # Find the why-us-item with this title and replace description
            pattern = rf'(<h3 style="color: #4ade80;">[^<]*{title_keyword}[^<]*</h3>\s*<p style="color: rgba\(255,255,255,0\.9\);">)[^<]+(</p>)'
            html = re.sub(pattern, rf'\g<1>{data["why_us_descriptions"][i]}\2', html, count=1)

    # 13. Diversify gallery alt texts
    gallery_images = re.findall(r'(src="/images/Gallery/[^"]+"\s+alt=")([^"]+)(")', html)
    for i, (prefix, old_alt, suffix) in enumerate(gallery_images):
        if i < len(data["gallery_alts"]):
            html = html.replace(
                f'{prefix}{old_alt}{suffix}',
                f'{prefix}{data["gallery_alts"][i]}{suffix}',
                1
            )

    # 14. Add hospitals section before FAQ
    hosp_cards = ""
    for h_name, h_addr, h_time in data["hospitals"]:
        hosp_cards += f'''
                    <div style="background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #1e4a9e; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <h4 style="color: #1e4a9e; margin: 0 0 8px 0; font-size: 1rem;">{h_name}</h4>
                        <p style="color: #64748b; font-size: 0.85rem; margin: 0;">{h_addr}</p>
                        <p style="color: #22c55e; font-size: 0.8rem; margin-top: 8px;">Penghantaran: {h_time}</p>
                    </div>
'''

    hospitals_section = f'''
        <!-- Local Hospitals Served -->
        <section class="local-hospitals" style="background: #f8fafc; padding: 60px 0;">
            <div class="container">
                <header class="section-header">
                    <h2>Hospital & Klinik Berdekatan yang Kami Servis di {name}</h2>
                    <p>Kami kerap menghantar katil hospital kepada pesakit yang discharge dari hospital-hospital ini</p>
                </header>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-top: 30px;">
{hosp_cards}
                </div>
            </div>
        </section>

        <!-- Google Maps Section -->
        <section class="local-map" style="background: #f1f5f9; padding: 60px 0;">
            <div class="container">
                <header class="section-header">
                    <h2>Lokasi Perkhidmatan di {name}</h2>
                    <p>Kami meliputi seluruh {name} dan kawasan sekitar</p>
                </header>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px; align-items: start;">
                    <div style="border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d200000!2d{data["lng"]}!3d{data["lat"]}!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2s{name.replace(" ", "%20")}!5e0!3m2!1sen!2smy" width="100%" height="350" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>

                    <div>
                        <h3 style="color: #1e4a9e; font-size: 1.2rem; margin-bottom: 16px;">Maklumat Penghantaran {name}</h3>
                        <div style="background: white; padding: 20px; border-radius: 12px; margin-bottom: 16px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 40px; height: 40px; background: #dcfce7; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                    <svg width="20" height="20" fill="none" stroke="#22c55e" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                </div>
                                <div>
                                    <p style="color: #1e4a9e; font-weight: 600; margin: 0;">Masa Penghantaran</p>
                                    <p style="color: #22c55e; font-size: 1.1rem; font-weight: 700; margin: 0;">{data["delivery_time"].title()}</p>
                                </div>
                            </div>
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 12px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 40px; height: 40px; background: #dbeafe; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                    <svg width="20" height="20" fill="none" stroke="#1e4a9e" stroke-width="2" viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                </div>
                                <div>
                                    <p style="color: #1e4a9e; font-weight: 600; margin: 0;">Jarak dari Gudang</p>
                                    <p style="color: #64748b; margin: 0;">{data["distance"]}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

'''

    if 'local-hospitals' not in html:
        html = html.replace(
            '        <!-- FAQ Section -->',
            hospitals_section + '        <!-- FAQ Section -->'
        )

    # 15. Replace FAQ with 6 unique questions
    faq_items = ""
    for i, (q, a) in enumerate(data["faq"]):
        open_attr = ' open' if i == 0 else ''
        faq_items += f'''
                    <details class="faq-item"{open_attr}>
                        <summary>
                            <h3>{q}</h3>
                        </summary>
                        <div class="faq-answer">
                            <p>{a}</p>
                        </div>
                    </details>
'''

    # Replace entire FAQ accordion
    html = re.sub(
        r'<div class="faq-accordion">.*?</div>\s*(?=</div>\s*</section>\s*(?:<!-- CTA|<!-- Local Test))',
        f'<div class="faq-accordion">\n{faq_items}                </div>\n',
        html,
        flags=re.DOTALL
    )

    # 16. Update FAQ schema to match 6 questions
    faq_schema_items = []
    for q, a in data["faq"]:
        clean_a = re.sub(r'<[^>]+>', '', a)  # Strip HTML for schema
        faq_schema_items.append(f'''                {{
                    "@type": "Question",
                    "name": "{q}",
                    "acceptedAnswer": {{
                        "@type": "Answer",
                        "text": "{clean_a}"
                    }}
                }}''')

    faq_schema = ",\n".join(faq_schema_items)

    html = re.sub(
        r'\{\s*"@type":\s*"FAQPage",\s*"mainEntity":\s*\[.*?\]\s*\}',
        f'''{{\n            "@type": "FAQPage",\n            "mainEntity": [\n{faq_schema}\n            ]\n        }}''',
        html,
        flags=re.DOTALL
    )

    # 16b. Fix any existing inline 50px to 60px for consistent spacing
    html = html.replace('padding: 50px 0;', 'padding: 60px 0;')
    html = html.replace('padding: 50px 0"', 'padding: 60px 0"')

    # 17. Add Google Review testimonials section before CTA
    star_svg = '<svg viewBox="0 0 24 24" fill="#FBBC05"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
    five_stars = (star_svg + "\n                            ") * 5

    test_cards = ""
    for t_name, t_initial, t_area, t_text in data["testimonials"]:
        test_cards += f'''
                    <article class="google-review-card">
                        <div class="google-review-header">
                            <div class="google-review-avatar">{t_initial}</div>
                            <div class="google-review-info">
                                <div class="google-review-name">{t_name}</div>
                                <div class="google-review-date">{t_area}</div>
                            </div>
                        </div>
                        <div class="google-review-stars">
                            {five_stars}
                        </div>
                        <p class="google-review-text">"{t_text}"</p>
                    </article>
'''

    testimonials_section = f'''
        <!-- Google Reviews Section -->
        <section class="local-testimonials" style="background: #f8fafc;">
            <div class="container">
                <header class="section-header">
                    <h2>Apa Kata Pelanggan di {name}</h2>
                    <p>Ulasan sebenar daripada pelanggan kami di {name} dan kawasan sekitar</p>
                </header>

                <div class="google-reviews-grid">
{test_cards}
                </div>

                <div class="google-summary-wrapper">
                    <a class="google-summary-link" href="https://share.google/hBmGVugG4LxFv54ok" target="_blank">
                        <span class="google-letter" style="color: #4285F4;">G</span><span class="google-letter" style="color: #EA4335;">o</span><span class="google-letter" style="color: #FBBC05;">o</span><span class="google-letter" style="color: #4285F4;">g</span><span class="google-letter" style="color: #34A853;">l</span><span class="google-letter" style="color: #EA4335;">e</span>
                        <span class="google-rating-num">4.9</span>
                        <span class="google-stars">\u2605\u2605\u2605\u2605\u2605</span>
                        <span class="google-ulasan">500+ ulasan</span>
                        <span class="google-lihat">Lihat Semua</span>
                    </a>
                </div>
            </div>
        </section>

'''

    # Replace existing testimonials section or add new one
    if 'local-testimonials' in html:
        html = re.sub(
            r'        <!-- (?:Local Testimonials|Google Reviews Section) -->.*?</section>\s*',
            testimonials_section,
            html,
            flags=re.DOTALL
        )
    else:
        html = html.replace(
            '        <!-- CTA Section -->',
            testimonials_section + '        <!-- CTA Section -->'
        )

    # 18. Add city directory + nearby locations before footer
    city_links = ""
    for c_name, c_slug in data.get("cities", []):
        city_links += f'                    <a href="/katil-hospital-{c_slug}.html">{c_name}</a>\n'

    nearby_links = ""
    for n_name, n_slug, n_delivery in data.get("nearby_states", []):
        nearby_links += f'''
                    <a href="/katil-hospital-{n_slug}.html" style="background: #f8fafc; padding: 20px; border-radius: 12px; text-decoration: none; text-align: center; transition: all 0.3s ease; border: 2px solid transparent;">
                        <p style="color: #1e4a9e; font-weight: 600; margin: 0 0 4px 0;">{n_name}</p>
                        <p style="color: #64748b; font-size: 0.85rem; margin: 0;">{n_delivery}</p>
                    </a>
'''

    bottom_sections = f'''
        <!-- City Directory -->
        <section style="background: linear-gradient(135deg, #0d3a7d 0%, #1e4a9e 100%); padding: 60px 0;">
            <div class="container">
                <header class="section-header">
                    <h2 style="color: white;">Semua Lokasi di {name}</h2>
                    <p style="color: rgba(255,255,255,0.9);">Pilih kawasan anda untuk maklumat penghantaran yang lebih tepat</p>
                </header>
                <div class="city-directory-grid">
{city_links}                </div>
            </div>
        </section>

        <!-- Nearby Locations -->
        <section class="nearby-locations" style="background: white; padding: 60px 0;">
            <div class="container">
                <header class="section-header">
                    <h2>Negeri Berdekatan {name}</h2>
                    <p>Kami juga menyediakan perkhidmatan sewa katil hospital di negeri-negeri berhampiran</p>
                </header>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 30px;">
{nearby_links}
                </div>
            </div>
        </section>

'''

    if 'nearby-locations' not in html:
        html = html.replace(
            '    </main>\n\n    <!-- Footer -->',
            bottom_sections + '    </main>\n\n    <!-- Footer -->'
        )

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"OK: {slug} ({name}) - transformed")
    return True


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=== Phase 1: Transforming State Pages ===\n")

    success = 0
    fail = 0

    for slug, data in STATES.items():
        try:
            if transform_page(slug, data):
                success += 1
            else:
                fail += 1
        except Exception as e:
            print(f"ERROR: {slug} - {e}")
            fail += 1

    print(f"\n=== Done: {success} OK, {fail} failed ===")
