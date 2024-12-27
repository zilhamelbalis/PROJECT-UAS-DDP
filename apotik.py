import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import time

class PatientData:
    def __init__(self, nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan):
        self.nama = nama
        self.usia = usia
        self.tanggal_lahir = tanggal_lahir
        self.jenis_kelamin = jenis_kelamin
        self.alamat = alamat
        self.kota = kota
        self.telepon = telepon
        self.keluhan = keluhan

    def to_dict(self):
        return {
            'nama': self.nama,
            'usia': self.usia,
            'tanggal_lahir': self.tanggal_lahir,
            'jenis_kelamin': self.jenis_kelamin,
            'alamat': self.alamat,
            'kota': self.kota,
            'telepon': self.telepon,
            'keluhan': self.keluhan,
        }

class PharmacySystem:
    def __init__(self):
        self.inital_data()
        
    def inital_data(self):
        # Initialize patient data storage
        if 'semua_pasien' not in st.session_state:
            st.session_state.semua_pasien = []
        
        # Initialize current patient
        if 'current_patient' not in st.session_state:
            st.session_state.current_patient = None
            
        # Initialize list of diseases/conditions
        self.daftar_penyakit = [
            "Demam",
            "Analgesik"
            "Obat Batuk",
            "Antihistamin",
            "Sakit Kepala",
            "Obat Diabetes",
            "Obat Hipertensi",
            "Sakit Gigi",
            "Sakit Perut",
            "Obat Lambung",
            "Lainnya"
        ]
        

        # Initialize pharmacy location data
        self.pharmacy_data = pd.DataFrame([
            {
                'nama': 'Apotek K-24 Kelapa Dua Depok',
                'latitude': -6.3657701, 
                'longitude': 106.8431499,
                'alamat': 'Jl. Klp. Dua Raya Jl. Rtm No.17C, Kota Depok',
                'rating': 4.4,
                'kontak': '0821-7319-1790',
                'ketersediaan_obat': ['Umum', 'Resep'],
                'kota': 'Depok'
            },
            {
                'nama': 'Apotek Kimia Farma 382 Kelapa Dua Depok',
                'latitude': -6.3549191, 
                'longitude': 106.8454358,
                'alamat': 'Jl. Akses UI No.45 C, Kota Depok',
                'rating': 4.1,
                'kontak': '0811-1067-8339',
                'ketersediaan_obat': ['Umum', 'Resep', 'Spesialis'],
                'kota': 'Depok'
            },
            {
                'nama': 'Apotek K-24 Akses UI',
                'latitude': -6.3657857, 
                'longitude': 106.8379179,
                'alamat': 'Ruko Graha Citra, Jl. Akses UI No.45, Tugu, Kec. Cimanggis, Kota Depok, Jawa Barat 16451',
                'rating': 4.5,
                'kontak': '0812-9317-0276',
                'ketersediaan_obat': ['Umum', 'Anak', 'Resep'],
                'kota': 'Depok'
            },
            {
                'nama': 'Apotek Nusantara',
                'latitude': -6.353715, 
                'longitude': 106.8269568,
                'alamat': 'Apotik Nusantara, Jl. Nusantara No.9, Tugu, Kec. Cimanggis, Kota Depok, Jawa Barat 16451',
                'rating': 4.4,
                'kontak': '0838-7196-9893',
                'ketersediaan_obat': ['Umum', 'Resep','Pesan Antar'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Roxy Depok',
                'latitude': -6.3843652, 
                'longitude': 106.795725,
                'alamat': 'Jl. Nusantara Raya No.76, Beji, Kecamatan Beji, Kota Depok, Jawa Barat 16421',
                'rating': 4.0,
                'kontak': '0811-2729-368',
                'ketersediaan_obat': ['Umum','Resep', '24 Jam'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Imani',
                'latitude': -6.3590914, 
                'longitude': 106.797095,
                'alamat': 'Jl. K.H.M. Usman No.17D, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425',
                'rating': 4.5,
                'kontak': '0819-0549-0028',
                'ketersediaan_obat': ['Umum', 'Anak', 'Resep'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Kimia Farma 352 Margonda',
                'latitude': -6.3755, 
                'longitude': 106.8134066,
                'alamat': 'Jl. Margonda No.326, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16424',
                'rating': 3.8,
                'kontak': '0811-1067-8325',
                'ketersediaan_obat': ['Umum', 'Resep'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Mars',
                'latitude': -6.3536323, 
                'longitude': 106.8235182,
                'alamat': 'Jl. Nusantara No.15, Tugu, Kec. Cimanggis, Kota Depok, Jawa Barat 16451',
                'rating': 4.5,
                'kontak': '0812-9109-0139',
                'ketersediaan_obat': ['Umum','Resep', 'Spesialis'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Century Pesona Khayangan Depok',
                'latitude': -6.3829587, 
                'longitude': 106.81101,
                'alamat': 'Jl. Margonda Raya No.45, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16423',
                'rating': 4.3,
                'kontak': '021-7721-1057',
                'ketersediaan_obat': ['Umum', 'Anak', 'Resep'],
                'kota' : 'Depok'
            },
            {
                'nama': 'Apotek Damai',
                'latitude': -6.358, 
                'longitude': 106.8372566,
                'alamat': 'Jl. Menpor No.12, Tugu, Kec. Cimanggis, Kota Depok, Jawa Barat 16451',
                'rating': 4.3,
                'kontak': '021-8719-032',
                'ketersediaan_obat': ['Umum', 'Resep','Pesan Antar'],
                'kota' : 'Depok'
            },
        ])

        # Initialize medicine inventory with expanded list
        self.medicine_inventory = [
            {"nama": "Paracetamol", "kategori": "Analgesik"},
            {"nama": "Paracetamol", "kategori": "Analgesik"},
            {"nama": "Amoxicillin", "kategori": "Antibiotik"},
            {"nama": "Omeprazole", "kategori": "Obat Lambung"},
            {"nama": "Ibuprofen", "kategori": "Analgesik"},
            {"nama": "OBH", "kategori": "Obat Batuk"},
            {"nama": "Cetirizine", "kategori": "Antihistamin"},
            {"nama": "Antasida", "kategori": "Obat Lambung"},
            {"nama": "Amlodipine", "kategori": "Obat Hipertensi"},
            {"nama": "Metformin", "kategori": "Obat Diabetes"},
            {"nama": "Ibu Profen", "kategori": "Sakit Gigi"},
            {"nama": "Colidan", "kategori": "Sakit Perut"},
            {"nama": "Mefinal", "kategori": "Sakit Perut"},
            {"nama": "Berlosid", "kategori": "Obat Lambung"},
            {"nama": "Bidium", "kategori": "Diare"},
            {"nama": "Loperamidp", "kategori": "Diare"},
            {"nama": "Cataflam", "kategori": "Sakit Gigi"},
            {"nama": "Aspirin", "kategori": "Demam"},
            {"nama": "Metronidazol", "kategori": "Sakit Gigi"},
            {"nama": "Bodrex", "kategori": "Sakit Kepala"},
            {"nama": "Panadol", "kategori": "Sakit Kepala"},
        ]
    
    def jalanin(self):
                
        st.set_page_config(
            page_title="Sistem Manajemen Apotek",
            page_icon="💊",
            layout="wide"
        )
        
        # Sidebar navigation
        st.sidebar.title("🏥 Sistem Apotek Digital")
        menu = st.sidebar.radio(
            "Pilih Menu",
            ["📝 Pendaftaran Pasien", "👥 Daftar Pasien", "💊 Inventaris Obat", "🗺️ Lokasi Apotek"]
        )
        
        if menu == "📝 Pendaftaran Pasien":
            self.patient_registration()
        elif menu == "👥 Daftar Pasien":
            self.patient_list()
        elif menu == "💊 Inventaris Obat":
            self.inventory_management()
        else:
            self.pharmacy_locations()

    def patient_registration(self):
        st.title("Selamat Datang Di Aplikasi Manajemen Obat Apoteker✨")
        st.image("gambar.png", use_container_width=True)
        # Menambahkan CSS untuk memusatkan gambar
        st.markdown(
            """
            <style>
            .stImage {
                display: flex;
                justify-content: center;
                }
            </style>
            """,
            unsafe_allow_html=True
            )
        st.title("📝 Formulir Pasien")

        # Create form columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Lengkap")
            usia = st.number_input("Usia", min_value=1, max_value=150, step=1)
            tanggal_lahir = st.date_input(
                'Tanggal Lahir',
                min_value=datetime(1900, 1, 1),
                max_value=datetime.today()
            )
            jenis_kelamin = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            
        with col2:
            telepon = st.text_input("Nomor Telepon")
            keluhan = st.selectbox("Keluhan/Penyakit", self.daftar_penyakit)
            kota = st.text_input("Kota")
            alamat = st.text_area("Alamat Lengkap")
            
            # Menambahkan text input "Lainnya"
        if keluhan == "Lainnya":
            keluhan_lainnya = st.text_input("Sebutkan keluhan lainnya:")
            keluhan = keluhan_lainnya if keluhan_lainnya else "Lainnya"
            st.session_state.current_patient.keluhan = keluhan

        if st.button("Submit Pendaftaran"):
            if self.process_registration(nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan):
                st.success("Pendaftaran berhasil!")
                self.display_patient_data(nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan)
            
    def process_registration(self, nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan):
        if not all([nama, alamat, kota, telepon, keluhan]):
            st.warning("Mohon lengkapi semua data!")
            return False

        if not self.validate_phone(telepon):
            st.warning("Format nomor telepon tidak valid!")
            return False

        with st.spinner("Memproses pendaftaran..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
                
            new_patient = PatientData(nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan)
            st.session_state.semua_pasien.append(new_patient)
            st.session_state.current_patient = new_patient
            
            return True

    def patient_list(self):
        st.title("📋 Daftar Pasien")
        
        if not st.session_state.semua_pasien:
            st.info("Belum ada pasien terdaftar")
            return
        
        # Create a list of dictionaries for the table
        patients_data = []
        for patient in st.session_state.semua_pasien:
            patients_data.append({
                'Nama': patient.nama,
                'Usia': f"{patient.usia} tahun",
                'Tanggal Lahir': patient.tanggal_lahir.strftime('%d-%m-%Y'),
                'Jenis Kelamin': patient.jenis_kelamin,
                'Alamat': patient.alamat,
                'Kota': patient.kota,
                'Telepon': patient.telepon,
                'Keluhan': patient.keluhan
            })
        
        # Convert to DataFrame and display as table
        df_patients = pd.DataFrame(patients_data)
        
        # Add search functionality
        search_term = st.text_input("🔍 Cari Pasien:", "")
        
        if search_term:
            df_filtered = df_patients[
                df_patients['Nama'].str.contains(search_term, case=False) |
                df_patients['Kota'].str.contains(search_term, case=False) |
                df_patients['Keluhan'].str.contains(search_term, case=False)
            ]
        else:
            df_filtered = df_patients
        
        # Display total patients
        st.write(f"Total Pasien: {len(df_filtered)}")
        
        # Display the table with custom styling
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Nama': st.column_config.TextColumn('Nama', width='medium'),
                'Usia': st.column_config.TextColumn('Usia', width='small'),
                'Tanggal Lahir': st.column_config.TextColumn('Tanggal Lahir', width='medium'),
                'Jenis Kelamin': st.column_config.TextColumn('Jenis Kelamin', width='medium'),
                'Alamat': st.column_config.TextColumn('Alamat', width='large'),
                'Kota': st.column_config.TextColumn('Kota', width='medium'),
                'Telepon': st.column_config.TextColumn('Telepon', width='medium'),
                'Keluhan': st.column_config.TextColumn('Keluhan', width='medium')
            }
        )
        
        # Add export functionality
        if st.button("📥 Export Data Pasien (CSV)"):
            df_patients.to_csv("data_pasien.csv", index=False)
            st.success("Data pasien berhasil diexport ke file 'data_pasien.csv'")
    
    def pharmacy_locations(self):
        st.title("🗺️ Lokasi Apotek")

        # Mengambil kota dan pasien saat ini jika data tersedia
        
        default_kota = ""
        if st.session_state.current_patient:
            default_kota = st.session_state.current_patient.kota

        # Mencari lokasi
        kota = st.text_input("Cari berdasarkan kota:", value=default_kota)
        
        if kota:
            filtered_pharmacies = self.pharmacy_data[
                self.pharmacy_data['kota'].str.lower().str.contains(kota.lower())
            ]
            
            if not filtered_pharmacies.empty:
                st.subheader(f"Apotek di {kota}")
                st.dataframe(
                    filtered_pharmacies[['nama', 'alamat', 'rating', 'kontak']],
                    use_container_width=True
                )
                
                
                # Membuat dan menampilkan maps
                map = self.create_pharmacy_map(filtered_pharmacies)
                folium_static(map)
            else:
                st.warning(f"Tidak ada apotek yang ditemukan di {kota}")

    def create_pharmacy_map(self, pharmacies):
        m = folium.Map(
            location=[pharmacies.iloc[0]['latitude'], pharmacies.iloc[0]['longitude']],
            zoom_start=13
        )
        
        for _, pharmacy in pharmacies.iterrows():
            folium.Marker(
                [pharmacy['latitude'], pharmacy['longitude']],
                popup=f"""
                <b>{pharmacy['nama']}</b><br>
                Rating: {pharmacy['rating']}⭐<br>
                Kontak: {pharmacy['kontak']}
                """,
                icon=folium.Icon(color='green', icon='plus-sign')
            ).add_to(m)
            
        return m
    
    @staticmethod 
    def validate_phone(phone):
        return phone.isdigit() and 8 <= len(phone) <= 13
    
    @staticmethod 
    def display_patient_data(nama, usia, tanggal_lahir, jenis_kelamin, alamat, kota, telepon, keluhan):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nama:** {nama}")
            st.write(f"**Usia:** {usia} tahun")
            st.write(f"**Tanggal Lahir:** {tanggal_lahir.strftime('%d-%m-%Y')}")
            st.write(f"**Jenis Kelamin:** {jenis_kelamin}")
        
        with col2:
            st.write(f"**Alamat:** {alamat}")
            st.write(f"**Kota:** {kota}")
            st.write(f"**Telepon:** {telepon}")
            st.write(f"**Keluhan:** {keluhan}")

    def inventory_management(self):
        st.title("📦 Manajemen Inventaris Obat")
        
        default_keluhan = None
        if st.session_state.current_patient:
            default_keluhan = st.session_state.current_patient.keluhan

        # Inventory overview
        df_inventory = pd.DataFrame(self.medicine_inventory)
        
        # Filter section
        st.subheader("🔍 Filter Inventaris")
        categories = list(set(med['kategori'] for med in self.medicine_inventory))
        selected_categories = st.multiselect("Filter berdasarkan kategori:", categories, default = default_keluhan)
        
        if selected_categories:
            filtered_df = df_inventory[df_inventory['kategori'].isin(selected_categories)]
        else:
            filtered_df = df_inventory

        st.dataframe(filtered_df, use_container_width=True)
            
if __name__ == "__main__":
    system = PharmacySystem()
    system.jalanin()