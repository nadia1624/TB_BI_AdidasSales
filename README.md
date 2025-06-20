# 📊 Dashboard Adidas BI

Selamat datang di **Dashboard Adidas BI**! Proyek ini adalah solusi Business Intelligence (BI) untuk menganalisis data penjualan Adidas. Dengan visualisasi yang interaktif dan intuitif, dashboard ini membantu Anda memahami tren penjualan, performa produk, dan mendukung pengambilan keputusan berbasis data.

## 🚀 Fitur Utama

- 📈 **Visualisasi Data Penjualan**: Grafik interaktif untuk memahami performa penjualan Adidas.
- 🛍️ **Analisis Performa Produk**: Lihat produk mana yang unggul di pasar.
- 📅 **Laporan Tren Penjualan**: Pantau tren penjualan berdasarkan waktu.
- 🔍 **Filter Waktu**: Sesuaikan data berdasarkan periode tertentu dengan mudah.

## 🛠️ Teknologi yang Digunakan

- **Python**: Proses ETL (Extract, Transform, Load) untuk pengolahan data.
- **PostgreSQL**: Data warehouse untuk menyimpan dan mengelola data.
- **Streamlit**: Framework untuk membangun dashboard interaktif.

## 📋 Cara Penggunaan

### 1. Instal Python
- Unduh dan instal Python dari [python.org](https://www.python.org/downloads/) (versi 3.8 atau lebih baru).
- Pastikan opsi **"Add Python to PATH"** dicentang saat instalasi.
- Verifikasi instalasi dengan perintah:
  ```bash
  python --version
  ```

### 2. Instal Dependensi Python
- Buka terminal atau command prompt.
- Instal pustaka yang diperlukan dengan perintah:
  ```bash
  pip install pandas matplotlib seaborn plotly sqlalchemy scikit-learn psycopg2-binary streamlit
  ```
- Pastikan proses instalasi selesai tanpa error.

### 3. Konfigurasi PostgreSQL
- Pastikan PostgreSQL berjalan (gunakan `pg_ctl start` atau pgAdmin).
- Buat database baru dengan perintah SQL:
  ```sql
  CREATE DATABASE DW_Adidas;
  ```
- Siapkan kredensial (username, password, host, port) sesuai konfigurasi PostgreSQL Anda.
- Buat tabel sesuai desain data warehouse yang telah dirancang.

### 4. Jalankan Proses ETL
- Buka dan jalankan file `ETL_AdidasSales.ipynb` untuk memproses data menggunakan Jupyter Notebook atau editor serupa.

### 5. Luncurkan Dashboard
- Jalankan dashboard Streamlit dengan perintah:
  ```bash
  streamlit run app.py
  ```
- Dashboard akan terbuka secara otomatis di browser Anda (default: `http://localhost:8501`).

## 👩‍💻 Kontributor

- **Nadia Deari Hanifah** (2211521004)
- **Azhra Meisa Khairani** (2211523010)
- **Rania Shofi Malika** (2211523014)


