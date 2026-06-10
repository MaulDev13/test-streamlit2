"""
helper_page.py
Halaman dokumentasi interaktif — penjelasan semua variabel dan cara
perhitungan yang digunakan dalam kalkulator GPP & Beban Latihan.
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ── Warna konsisten dengan app.py ────────────────────────────────────────────
BG       = "#0f1117"
CARD_BG  = "#1e2130"
GRID_CLR = "#2d3348"
CYAN     = "#22d3ee"
BLUE     = "#0ea5e9"
GREEN    = "#4ade80"
AMBER    = "#fbbf24"
RED      = "#f87171"
TEXT_CLR = "#94a3b8"


def apply_dark(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT_CLR, labelsize=9)
    ax.xaxis.label.set_color(TEXT_CLR)
    ax.yaxis.label.set_color(TEXT_CLR)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_CLR)
    ax.grid(color=GRID_CLR, linewidth=0.6, linestyle="--")


def render():
    """Render seluruh isi halaman helper."""

    st.markdown("## 📖 Panduan & Penjelasan Variabel")
    st.markdown(
        "Halaman ini menjelaskan **setiap variabel** yang digunakan dan "
        "**cara perhitungannya** step-by-step. Cocok sebagai referensi saat "
        "kamu melihat output kalkulator."
    )

    # ── NAVIGASI CEPAT ────────────────────────────────────────────────────────
    st.markdown("""
    **Navigasi Cepat:**
    [GPP](#1-gpp-general-physical-preparedness) ·
    [1RM Epley](#2-estimasi-1rm-rumus-epley) ·
    [Intensitas](#3-intensitas-latihan-berdasarkan-gpp) ·
    [RPE](#4-rpe-rate-of-perceived-exertion) ·
    [Fixed Point Iteration](#5-fixed-point-iteration-optimasi-beban) ·
    [Pull-Up](#6-iterasi-pull-up)
    """)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 1. GPP
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 1. GPP — General Physical Preparedness")
    st.markdown("""
GPP adalah **skor kebugaran umum** (0–100) yang menggabungkan tiga komponen
fisik dasar: daya tahan kardiovaskular, kekuatan otot atas, dan kekuatan inti.
Semakin tinggi GPP, semakin siap tubuh untuk beban latihan yang lebih berat.
""")

    with st.expander("📐 Variabel & Rumus GPP", expanded=True):

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
| Simbol | Nama Lengkap | Satuan | Keterangan |
|--------|-------------|--------|------------|
| `PU` | Push-up | repetisi | Jumlah push-up maksimal tanpa henti |
| `SU` | Sit-up | repetisi | Jumlah sit-up maksimal dalam satu set |
| `L` | Lari 12 menit | meter | Jarak yang ditempuh dalam 12 menit |
| `S_PU` | Skor Push-up | 0–100 | Nilai push-up setelah dinormalisasi |
| `S_SU` | Skor Sit-up | 0–100 | Nilai sit-up setelah dinormalisasi |
| `S_L` | Skor Lari | 0–100 | Nilai lari setelah dinormalisasi |
| `GPP` | Skor GPP Akhir | 0–100 | Nilai kebugaran umum tertimbang |
""")

        with col2:
            st.markdown("""
**Langkah perhitungan:**

**① Normalisasi Push-up**
```
S_PU = (PU / 60) × 100
```
Acuan: 60 rep = skor sempurna (100)

**② Normalisasi Sit-up**
```
S_SU = (SU / 60) × 100
```
Acuan: 60 rep = skor sempurna (100)

**③ Normalisasi Lari**
```
S_L = (L / 3000) × 100
```
Acuan: 3000 meter = skor sempurna (100)

**④ GPP Tertimbang**
```
GPP = 0.4 × S_L + 0.3 × S_PU + 0.3 × S_SU
```
Kardio diberi bobot lebih (40%) karena dampaknya
lebih besar terhadap kapasitas latihan umum.
""")

        st.markdown("**Contoh perhitungan nyata:**")
        st.code("""
# Input
PU = 35 rep,  SU = 40 rep,  L = 2400 m

# Normalisasi
S_PU = (35 / 60) × 100 = 58.33
S_SU = (40 / 60) × 100 = 66.67
S_L  = (2400 / 3000) × 100 = 80.00

# GPP
GPP = 0.4×80.00 + 0.3×58.33 + 0.3×66.67
    = 32.00 + 17.50 + 20.00
    = 69.50  → Kategori: Rata-rata (60–70)
""", language="python")

    with st.expander("📊 Tabel Kategori GPP"):
        st.markdown("""
| Skor GPP | Kategori | Intensitas Latihan | Artinya |
|----------|----------|-------------------|---------|
| < 50 | 🔴 Kurang | 55% 1RM | Pemula mutlak, fokus teknik & aerobik |
| 50–60 | 🟠 Cukup | 65% 1RM | Aktif tapi belum konsisten |
| 60–70 | 🟡 Rata-rata | 70% 1RM | Kebugaran umum orang aktif |
| 70–80 | 🔵 Baik | 75% 1RM | Siap program latihan terstruktur |
| 80–90 | 🟢 Sangat Baik | 80% 1RM | Atlet rekreasi terlatih |
| > 90 | 🌟 Luar Biasa | 85% 1RM | Atlet kompetitif / kondisi puncak |
""")

    # Visualisasi distribusi bobot GPP
    with st.expander("📈 Visualisasi Bobot Komponen GPP"):
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))

        # Pie chart bobot
        ax = axes[0]
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        sizes  = [40, 30, 30]
        labels = ["Kardio\n(Lari)", "Push-up", "Sit-up"]
        colors = [CYAN, BLUE, AMBER]
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct="%1.0f%%", startangle=90,
            textprops={"color": TEXT_CLR, "fontsize": 10},
        )
        for at in autotexts:
            at.set_color(BG); at.set_fontweight("bold")
        ax.set_title("Bobot GPP", color=TEXT_CLR, fontsize=11, pad=10)

        # Bar skor vs komponen
        ax2 = axes[1]
        apply_dark(fig, ax2)
        komponen = ["Push-up\n(35 rep)", "Sit-up\n(40 rep)", "Lari\n(2400 m)"]
        skor     = [58.33, 66.67, 80.0]
        bars = ax2.barh(komponen, skor, color=[BLUE, AMBER, CYAN], alpha=0.85)
        ax2.set_xlim(0, 110)
        ax2.axvline(100, color=GRID_CLR, linewidth=1, linestyle="--")
        for bar, val in zip(bars, skor):
            ax2.text(val + 1.5, bar.get_y() + bar.get_height()/2,
                     f"{val:.1f}", va="center", color=TEXT_CLR, fontsize=9)
        ax2.set_title("Contoh Skor per Komponen", color=TEXT_CLR, fontsize=11)
        ax2.set_xlabel("Skor (0–100)", color=TEXT_CLR)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 2. EPLEY 1RM
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 2. Estimasi 1RM — Rumus Epley")
    st.markdown("""
**1RM (One Repetition Maximum)** adalah beban terberat yang bisa kamu angkat
**tepat satu kali** dengan teknik yang benar. Mengetes 1RM secara langsung
berisiko cedera, jadi kita estimasi dari data latihan yang lebih aman.
""")

    with st.expander("📐 Variabel & Rumus Epley", expanded=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
| Simbol | Nama | Satuan | Keterangan |
|--------|------|--------|------------|
| `W` | Beban latihan | kg | Beban yang dipakai saat latihan (bukan 1RM) |
| `R` | Repetisi | rep | Jumlah pengulangan yang berhasil dilakukan |
| `1RM` | One Rep Max | kg | Estimasi kekuatan maksimum satu repetisi |
""")

        with col2:
            st.markdown("""
**Rumus Epley:**
```
1RM = W × (1 + R / 30)
```

**Penjelasan logika:**
- Semakin banyak repetisi yang bisa dilakukan
  dengan beban tertentu → beban terasa lebih ringan
  → artinya 1RM kamu lebih tinggi dari beban itu
- Faktor `R/30` mewakili "seberapa jauh" beban
  latihanmu dari batas maksimum
- Rumus ini paling akurat untuk R = 2–12 rep
""")

        st.markdown("**Contoh perhitungan:**")
        st.code("""
# Bench Press: angkat 60 kg sebanyak 8 kali
W = 60 kg,  R = 8 rep

1RM = 60 × (1 + 8/30)
    = 60 × (1 + 0.267)
    = 60 × 1.267
    = 76.0 kg

# Artinya: estimasi kamu bisa angkat maksimal ~76 kg
# untuk 1 repetisi penuh
""", language="python")

    with st.expander("📈 Visualisasi — Pengaruh Repetisi terhadap 1RM"):
        fig, ax = plt.subplots(figsize=(7, 3.5))
        apply_dark(fig, ax)

        reps   = np.arange(1, 16)
        beban  = 60
        rm_vals = [beban * (1 + r / 30) for r in reps]

        ax.plot(reps, rm_vals, color=CYAN, linewidth=2.5, marker="o", markersize=5)
        ax.axhline(beban, color=AMBER, linewidth=1.2, linestyle="--",
                   label=f"Beban latihan ({beban} kg)")
        ax.fill_between(reps, beban, rm_vals, alpha=0.1, color=CYAN)
        ax.set_xlabel("Jumlah Repetisi (R)", fontsize=10)
        ax.set_ylabel("Estimasi 1RM (kg)", fontsize=10)
        ax.set_title(f"Estimasi 1RM dari Beban {beban} kg — Berbagai Repetisi",
                     color=TEXT_CLR, fontsize=11)
        ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR)

        for r, rm in zip(reps, rm_vals):
            if r in [1, 5, 8, 12, 15]:
                ax.annotate(f"{rm:.1f}", (r, rm), textcoords="offset points",
                            xytext=(0, 8), ha="center", color=CYAN, fontsize=8)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.caption("Grafik di atas: beban latihan tetap 60 kg, repetisi berubah → 1RM estimasi berbeda")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 3. INTENSITAS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 3. Intensitas Latihan Berdasarkan GPP")
    st.markdown("""
Setelah GPP diketahui, sistem menentukan **persentase intensitas** yang
aman dan efektif. Ini adalah **titik awal** beban sebelum dioptimasi oleh
Fixed Point Iteration.
""")

    with st.expander("📐 Variabel & Tabel Intensitas", expanded=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
| Simbol | Nama | Keterangan |
|--------|------|------------|
| `GPP` | Skor kebugaran | Input dari Tahap 1 |
| `I` | Intensitas | Persentase dari 1RM (0.55 – 0.85) |
| `B_awal` | Beban awal | Beban titik mulai sebelum iterasi |

**Rumus beban awal:**
```
B_awal = I × 1RM
```
""")
        with col2:
            st.markdown("""
| GPP | Intensitas (I) | B_awal (contoh 1RM=76kg) |
|-----|---------------|--------------------------|
| < 50 | 55% | 41.8 kg |
| 50–60 | 65% | 49.4 kg |
| 60–70 | 70% | 53.2 kg |
| 70–80 | **75%** | **57.0 kg** |
| 80–90 | 80% | 60.8 kg |
| > 90 | 85% | 64.6 kg |
""")

        st.markdown("**Contoh:**")
        st.code("""
# GPP = 69.5 → masuk rentang 60–70 → I = 70% = 0.70
# 1RM Bench Press = 76 kg

B_awal = 0.70 × 76 = 53.2 kg

# Ini adalah beban AWAL sebelum iterasi numerik menyesuaikannya
# ke target RPE yang diinginkan
""", language="python")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 4. RPE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 4. RPE — Rate of Perceived Exertion")
    st.markdown("""
**RPE** adalah skala subyektif tingkat usaha saat latihan.
Dalam sistem ini, RPE dipakai sebagai **sinyal umpan balik** —
iterasi numerik menyesuaikan beban sampai RPE mendekati target.
""")

    with st.expander("📐 Skala RPE & Variabel Terkait", expanded=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
| Simbol | Nama | Keterangan |
|--------|------|------------|
| `RPE` | Rate of Perceived Exertion | Skala usaha 1–10 |
| `RPE_t` | Target RPE | RPE yang diinginkan (default: 8) |
| `RPE_n` | RPE saat iterasi ke-n | Estimasi RPE pada beban W_n |
| `rpe_awal` | RPE awal | Diasumsikan 6.0 pada B_awal |
""")
        with col2:
            st.markdown("""
| Nilai RPE | Artinya |
|-----------|---------|
| 1–3 | Sangat ringan, bisa bicara panjang lebar |
| 4–5 | Ringan, sedikit terasa |
| **6** | Sedang, mulai terasa tapi nyaman |
| **7–8** | Berat, napas pendek, fokus penuh ← zona target |
| 9 | Sangat berat, hampir tidak bisa lanjut |
| 10 | Maksimal absolut |
""")

        st.markdown("**Model Estimasi RPE Internal:**")
        st.code("""
# RPE diestimasi secara linier dari perubahan beban relatif terhadap B_awal
# RPE awal (pada B_awal) = 6.0

rasio = (W_sekarang - B_awal) / B_awal
RPE_n = 6.0 + rasio × 20

# Contoh:
# B_awal = 53.2 kg, W = 57 kg
# rasio = (57 - 53.2) / 53.2 = 0.0714
# RPE = 6.0 + 0.0714 × 20 = 6.0 + 1.43 = 7.43
""", language="python")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 5. FIXED POINT ITERATION
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 5. Fixed Point Iteration — Optimasi Beban")
    st.markdown("""
Ini adalah **inti metode numerik** dalam sistem ini. Setelah beban awal
ditetapkan berdasarkan GPP, iterasi ini menyesuaikan beban secara bertahap
hingga RPE mendekati target (default: 8).
""")

    with st.expander("📐 Semua Variabel Iterasi", expanded=True):
        st.markdown("""
| Simbol | Nama | Default | Keterangan |
|--------|------|---------|------------|
| `W_n` | Beban iterasi ke-n | — | Beban pada iterasi saat ini (kg) |
| `W_(n+1)` | Beban iterasi berikutnya | — | Hasil update beban |
| `W_0` / `B_awal` | Beban awal | dari GPP | Titik mulai iterasi |
| `RPE_t` | Target RPE | 8.0 | RPE yang ingin dicapai |
| `RPE_n` | RPE estimasi iterasi ke-n | — | Dihitung dari model linier |
| `k` | Konstanta langkah | 2.0 | Mengontrol seberapa besar setiap koreksi beban |
| `tol_RPE` | Toleransi RPE | 0.5 | Batas selisih RPE agar iterasi berhenti |
| `tol_W` | Toleransi beban | 0.5 kg | Batas perubahan beban agar iterasi berhenti |
| `max_iter` | Iterasi maksimum | 15 | Batas atas putaran iterasi |
""")

    with st.expander("🔁 Rumus & Alur Iterasi", expanded=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
**Rumus update beban:**
```
W(n+1) = W(n) + k × (RPE_t − RPE(n))
```

**Kondisi berhenti (salah satu terpenuhi):**
```
|RPE_t − RPE(n)| < 0.5   → RPE sudah cukup dekat
|W(n+1) − W(n)| < 0.5 kg → beban sudah stabil
```

**Pengaruh konstanta `k`:**
- `k` kecil (0.5–1) → konvergen lambat, lebih halus
- `k` sedang (2) → seimbang ← **default**
- `k` besar (4–5) → konvergen cepat, berisiko overshooting
""")
        with col2:
            st.markdown("**Contoh trace iterasi:**")
            st.code("""
B_awal = 53.2 kg,  RPE_target = 8,  k = 2

Iter 0: W=53.20, RPE=6.00, ΔRPE=2.00, ΔW=4.00
  → W_baru = 53.2 + 2×(8−6.0) = 57.20

Iter 1: W=57.20, RPE=7.43, ΔRPE=0.57, ΔW=1.14
  → W_baru = 57.2 + 2×(8−7.43) = 58.34

Iter 2: W=58.34, RPE=7.86, ΔRPE=0.14 < 0.5 ✅
  → KONVERGEN. Beban akhir = 58.84 kg
""", language="text")

    with st.expander("📈 Visualisasi Konvergensi Iterasi"):
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))

        # Simulasi beberapa nilai k
        b0      = 53.2
        rpe_t   = 8.0
        rpe_init = 6.0

        def sim(k_val, max_i=15):
            w = b0
            ws, rpes = [w], []
            for _ in range(max_i):
                rasio = (w - b0) / b0 if b0 else 0
                rpe_n = min(10, max(1, rpe_init + rasio * 20))
                rpes.append(rpe_n)
                if abs(rpe_t - rpe_n) < 0.5:
                    break
                w = max(0, w + k_val * (rpe_t - rpe_n))
                ws.append(w)
            rpes.append(min(10, max(1, rpe_init + ((ws[-1]-b0)/b0)*20)))
            return ws, rpes

        ax1, ax2 = axes

        for k_plot, col, lbl in [(0.5, AMBER, "k=0.5"), (2.0, CYAN, "k=2.0 (default)"), (4.0, RED, "k=4.0")]:
            ws, rpes = sim(k_plot)
            x = list(range(len(ws)))
            apply_dark(fig, ax1)
            apply_dark(fig, ax2)
            ax1.plot(x, ws,   marker="o", markersize=4, color=col, label=lbl, linewidth=1.8)
            ax2.plot(x, rpes, marker="o", markersize=4, color=col, label=lbl, linewidth=1.8)

        ax1.axhline(b0, color=GRID_CLR, linestyle=":", linewidth=1)
        ax1.set_title("Beban per Iterasi", color=TEXT_CLR, fontsize=10)
        ax1.set_xlabel("Iterasi", fontsize=9); ax1.set_ylabel("Beban (kg)", fontsize=9)
        ax1.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=8)

        ax2.axhline(rpe_t, color=GREEN, linestyle="--", linewidth=1.2, label=f"Target RPE={rpe_t}")
        ax2.set_title("RPE per Iterasi", color=TEXT_CLR, fontsize=10)
        ax2.set_xlabel("Iterasi", fontsize=9); ax2.set_ylabel("RPE", fontsize=9)
        ax2.set_ylim(4, 10.5)
        ax2.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=8)

        fig.suptitle("Perbandingan Kecepatan Konvergensi — Nilai k Berbeda",
                     color=TEXT_CLR, fontsize=11, y=1.02)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.caption(
            "k=0.5: lambat tapi stabil · k=2.0: seimbang (default) · "
            "k=4.0: cepat tapi bisa overshoot"
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # 6. PULL-UP
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 6. Iterasi Pull-Up — Progresi Repetisi")
    st.markdown("""
Pull-up menggunakan **berat badan sendiri** sebagai beban, sehingga
pendekatan berbeda diperlukan — bukan optimasi beban, melainkan
**progresi jumlah repetisi** menuju target.
""")

    with st.expander("📐 Variabel & Rumus Pull-Up", expanded=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
| Simbol | Nama | Default | Keterangan |
|--------|------|---------|------------|
| `R_n` | Repetisi iterasi ke-n | — | Rep saat ini |
| `R_t` | Target repetisi | 10 | Jumlah pull-up yang dituju |
| `R_(n+1)` | Rep berikutnya | — | Estimasi progressi |
| `BB` | Berat badan | — | Input pengguna (kg) |
| `B_tambahan` | Beban tambahan | — | Beban weighted pull-up |
""")
        with col2:
            st.markdown("""
**Rumus iterasi repetisi:**
```
R(n+1) = R(n) + 0.2 × (R_t − R(n))
```

**Jika rep awal ≥ 10 (target tercapai):**
```
B_tambahan = 5% × BB
```
Artinya: tambah beban vest/dumbbell sebesar
5% dari berat badan untuk menambah intensitas.

**Konvergensi:** berhenti ketika `|R_t − R_n| < 0.5`
""")

        st.markdown("**Contoh trace (rep awal = 6, target = 10):**")
        st.code("""
R_0 = 6,  R_t = 10,  faktor = 0.2

Iter 0: R = 6.00,  ΔR = 4.00
  → R_baru = 6 + 0.2×(10−6) = 6.80

Iter 1: R = 6.80,  ΔR = 3.20
  → R_baru = 6.8 + 0.2×(10−6.8) = 7.44

Iter 2: R = 7.44,  ΔR = 2.56
  ...

Iter 8: R = 9.58,  ΔR = 0.42 < 0.5 ✅ KONVERGEN
  → Target: lakukan 10 rep pull-up

# Jika rep awal = 12 (≥ 10):
BB = 70 kg
B_tambahan = 0.05 × 70 = 3.5 kg → Weighted Pull-Up +3.5 kg
""", language="python")

    with st.expander("📈 Visualisasi Konvergensi Pull-Up"):
        fig, ax = plt.subplots(figsize=(7, 3.5))
        apply_dark(fig, ax)

        r     = 6.0
        r_t   = 10
        rs    = [r]
        for _ in range(20):
            delta = r_t - r
            if abs(delta) < 0.5:
                break
            r = r + 0.2 * delta
            rs.append(r)

        x = list(range(len(rs)))
        ax.plot(x, rs, color=CYAN, linewidth=2.5, marker="o", markersize=6)
        ax.axhline(r_t, color=GREEN, linewidth=1.5, linestyle="--",
                   label=f"Target: {r_t} rep")
        ax.fill_between(x, rs, r_t, alpha=0.08, color=CYAN)
        ax.set_xlabel("Iterasi", fontsize=10)
        ax.set_ylabel("Estimasi Repetisi", fontsize=10)
        ax.set_title("Progresi Pull-Up: 6 rep → Target 10 rep", color=TEXT_CLR, fontsize=11)
        ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR)

        for i, rv in enumerate(rs):
            if i % 2 == 0:
                ax.annotate(f"{rv:.2f}", (i, rv), textcoords="offset points",
                            xytext=(0, 9), ha="center", color=CYAN, fontsize=8)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # RINGKASAN ALUR
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🗺️ Ringkasan Alur Sistem")

    st.markdown("""
```
INPUT
  └─ Profil (umur, BB, TB)
  └─ Kebugaran (push-up, sit-up, lari)
  └─ Latihan (beban × rep tiap gerakan)
       │
       ▼
TAHAP 1 — Hitung GPP
  S_PU, S_SU, S_L → GPP = 0.4·S_L + 0.3·S_PU + 0.3·S_SU
       │
       ▼
TAHAP 2 — Estimasi 1RM (Epley)
  1RM = W × (1 + R/30)   ← per latihan
       │
       ▼
TAHAP 3 — Tentukan Intensitas
  GPP → I (55%–85% dari 1RM)
       │
       ▼
TAHAP 4 — Beban Awal
  B_awal = I × 1RM   ← per latihan
       │
       ▼
TAHAP 5 — Fixed Point Iteration
  W(n+1) = W(n) + k·(RPE_t − RPE_n)
  → sampai |ΔRPE| < 0.5 atau |ΔW| < 0.5
       │
       ▼
OUTPUT — Beban Akhir per Latihan + Analisis GPP
```
""")

    st.info(
        "💡 **Tips penggunaan:** Mulai dengan `k=2` dan `RPE target=8`. "
        "Jika beban akhir terasa terlalu berat di sesi pertama, turunkan "
        "`k` ke 1.5 atau RPE target ke 7.5."
    )