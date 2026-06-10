# 🏋️ Kalkulator GPP & Rekomendasi Beban Latihan

Aplikasi Streamlit untuk menghitung **General Physical Preparedness (GPP)** dan memberikan rekomendasi beban latihan berbasis metode numerik.

## Metode yang Digunakan
- **Normalisasi GPP** — push-up, sit-up, lari 12 menit
- **Epley Formula** — estimasi 1RM dari beban & repetisi
- **Fixed Point Iteration** — optimasi beban berdasarkan target RPE
- **Iterasi Repetisi** — progresi pull-up menuju weighted pull-up

---

## Cara Menjalankan

### 1. Persiapan (sekali saja)

```bash
# Pastikan Python 3.9+ sudah terinstall
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser: `http://localhost:8501`

---

## Struktur File

```
gpp_calculator/
├── app.py              # UI Streamlit (tampilan & interaksi)
├── calculations.py     # Logika perhitungan numerik
├── requirements.txt    # Dependencies Python
└── README.md           # Panduan ini
```

---

## Cara Pakai

1. **Isi profil** — umur, jenis kelamin, berat & tinggi badan
2. **Isi tes kebugaran** — jumlah push-up, sit-up, dan jarak lari 12 menit
3. **Isi data latihan** — beban & repetisi untuk setiap gerakan
4. **Klik "Hitung GPP & Rekomendasi"**
5. Lihat hasil di 4 tab:
   - **GPP & Profil** — skor, radar chart, langkah perhitungan
   - **Estimasi 1RM** — tabel & grafik 1RM per latihan
   - **Iterasi Numerik** — tabel konvergensi tiap latihan
   - **Rekomendasi Akhir** — beban final + analisis

---

## Kustomisasi

Di sidebar tersedia parameter iterasi:
- **Target RPE** (default 8) — skala usaha yang diinginkan (1–10)
- **Konstanta k** (default 2) — kecepatan konvergensi iterasi
- **Max Iterasi** (default 15) — batas iterasi maksimum