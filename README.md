# AHP Kriteria

Aplikasi berbasis web untuk mendukung pengambilan keputusan menggunakan metode Analytic Hierarchy Process (AHP), terutama dalam konteks pemilihan motif kain terbaik berdasarkan beberapa kriteria terstruktur.

## 🔍 Deskripsi Singkat

AHP Kriteria dikembangkan untuk membantu perusahaan atau individu dalam melakukan analisis multikriteria. Aplikasi ini memungkinkan pengguna untuk:

- Menginput kriteria dan alternatif
- Melakukan perbandingan berpasangan antar kriteria
- Menghitung bobot dan skor akhir otomatis menggunakan metode AHP
- Melihat hasil ranking alternatif
- Mengekspor laporan ke PDF
- Menyimpan riwayat penilaian

## 🚀 Teknologi yang Digunakan

- **Frontend**: HTML, Bootstrap, Chart.js
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Ekspor PDF**: jsPDF, html2canvas
- **Pengolahan Data**: Pandas, NumPy

## 📂 Struktur Fitur

- **Dashboard**: Statistik jumlah upload, motif terpopuler, skor tertinggi, dan grafik 5 skor tertinggi terbaru.
- **Kriteria**: Input nama kriteria penilaian.
- **Alternatif**: Input nama alternatif atau objek yang akan dinilai.
- **Perbandingan Kriteria**: Matriks perbandingan berpasangan antar kriteria.
- **Hitung Bobot**: Hasil bobot AHP, konsistensi rasio (CR), dan validasi konsistensi.
- **Upload Data Pesanan**: Upload file Excel berisi data motif dan atributnya.
- **Riwayat Skoring**: Menampilkan hasil perhitungan terdahulu dengan detail skor dan ranking.

## 📥 Cara Install dan Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/CallMeSahril/ahp_kriteria.git
cd ahp_kriteria
```
