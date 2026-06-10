import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from calculations import (
    hitung_gpp,
    hitung_1rm,
    tentukan_intensitas,
    iterasi_beban,
    iterasi_pullup,
)

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator GPP & Beban Latihan",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Matplotlib dark style helper ─────────────────────────────────────────────
BG       = "#0f1117"
CARD_BG  = "#1e2130"
GRID_CLR = "#2d3348"
CYAN     = "#22d3ee"
BLUE     = "#0ea5e9"
GREEN    = "#4ade80"
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

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem; font-weight: 700;
        color: #e2e8f0; line-height: 1.15; margin-bottom: 0.2rem;
    }
    .hero-sub { font-size: 1rem; color: #64748b; margin-bottom: 2rem; }
    .accent   { color: #22d3ee; }
    .card {
        background: #1e2130; border: 1px solid #2d3348;
        border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem;
        font-weight: 600; color: #94a3b8; text-transform: uppercase;
        letter-spacing: 0.08em; margin-bottom: 0.6rem;
    }
    .metric-big { font-family: 'Space Grotesk', sans-serif; font-size: 2.8rem; font-weight: 700; color: #22d3ee; line-height:1; }
    .metric-label { font-size: 0.82rem; color: #64748b; margin-top: 0.2rem; }
    .gpp-bar-wrap { background:#2d3348; border-radius:999px; height:13px; width:100%; margin:0.5rem 0 0.3rem; overflow:hidden; }
    .gpp-bar-fill { height:100%; border-radius:999px; }
    .badge { display:inline-block; padding:0.22rem 0.75rem; border-radius:999px; font-size:0.76rem; font-weight:600; letter-spacing:0.04em; }
    .badge-cyan  { background:#083344; color:#22d3ee; }
    .badge-green { background:#052e16; color:#4ade80; }
    .badge-amber { background:#431407; color:#fb923c; }
    .badge-red   { background:#3f0b0b; color:#f87171; }
    .step-num {
        display:inline-flex; align-items:center; justify-content:center;
        width:26px; height:26px; border-radius:50%;
        background:#083344; color:#22d3ee; font-weight:700; font-size:0.82rem;
        margin-right:0.5rem; flex-shrink:0;
    }
    .step-row  { display:flex; align-items:center; margin-bottom:0.45rem; }
    .step-text { color:#cbd5e1; font-size:0.9rem; }
    div[data-testid="stSidebar"] { background:#13161f; border-right:1px solid #2d3348; }
    div[data-testid="stSidebar"] label { color:#94a3b8 !important; font-size:0.88rem; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏋️ Input Data")

    st.markdown("### 👤 Profil")
    umur   = st.number_input("Umur (tahun)", 10, 80, 25)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    bb     = st.number_input("Berat Badan (kg)", 30.0, 200.0, 70.0, 0.5)
    tb     = st.number_input("Tinggi Badan (cm, opsional)", 100, 220, 170)

    st.markdown("---")
    st.markdown("### 🧪 Tes Kebugaran")
    pushup = st.number_input("Push-up Maks (rep)", 0, 200, 35)
    situp  = st.number_input("Sit-up Maks (rep)", 0, 200, 40)
    lari   = st.number_input("Lari 12 Menit (meter)", 0, 5000, 2400)

    st.markdown("---")
    st.markdown("### 🏗 Data Latihan")
    st.caption("Isi beban & repetisi latihan yang sudah dilakukan.")

    col_a, col_b = st.columns(2)
    with col_a: bp_w  = st.number_input("Bench Press kg",  0.0, 300.0, 60.0, 2.5)
    with col_b: bp_r  = st.number_input("Bench Press rep", 0, 30, 8)

    col_a, col_b = st.columns(2)
    with col_a: sq_w  = st.number_input("Squat kg",  0.0, 400.0, 80.0, 2.5)
    with col_b: sq_r  = st.number_input("Squat rep", 0, 30, 8)

    col_a, col_b = st.columns(2)
    with col_a: lp_w  = st.number_input("Lat Pulldown kg",  0.0, 200.0, 50.0, 2.5)
    with col_b: lp_r  = st.number_input("Lat Pulldown rep", 0, 30, 10)

    col_a, col_b = st.columns(2)
    with col_a: dl_w  = st.number_input("Deadlift kg",  0.0, 400.0, 0.0, 2.5)
    with col_b: dl_r  = st.number_input("Deadlift rep", 0, 30, 0)

    col_a, col_b = st.columns(2)
    with col_a: ohp_w = st.number_input("OHP kg",  0.0, 200.0, 0.0, 2.5)
    with col_b: ohp_r = st.number_input("OHP rep", 0, 30, 0)

    pu_rep = st.number_input("Pull-Up Maks (rep, 0 = skip)", 0, 50, 6)

    st.markdown("---")
    st.markdown("### ⚙️ Parameter Iterasi")
    rpe_target = st.slider("Target RPE", 6.0, 9.0, 8.0, 0.5)
    k_val      = st.slider("Konstanta k", 0.5, 5.0, 2.0, 0.5)
    max_iter   = st.slider("Max Iterasi", 5, 30, 15)

    hitung = st.button("🔢 Hitung GPP & Rekomendasi", use_container_width=True, type="primary")


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="hero-title">Kalkulator <span class="accent">GPP</span> &<br>Rekomendasi Beban Latihan</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Berbasis metode numerik — Fixed Point Iteration · Epley 1RM · Intensity Scaling</p>', unsafe_allow_html=True)

if not hitung:
    st.info("👈 Isi data di sidebar, lalu klik **Hitung GPP & Rekomendasi**.")
    st.stop()

# ─── Kumpulkan latihan valid ──────────────────────────────────────────────────
exercises_raw = {
    "Bench Press":  (bp_w,  bp_r),
    "Squat":        (sq_w,  sq_r),
    "Lat Pulldown": (lp_w,  lp_r),
    "Deadlift":     (dl_w,  dl_r),
    "OHP":          (ohp_w, ohp_r),
}
exercises = {n: v for n, v in exercises_raw.items() if v[0] > 0 and v[1] > 0}

# ─── Kalkulasi ────────────────────────────────────────────────────────────────
gpp_result   = hitung_gpp(pushup, situp, lari)
intensitas   = tentukan_intensitas(gpp_result["gpp"])
rm_results   = {name: hitung_1rm(w, r) for name, (w, r) in exercises.items()}
beban_awal   = {name: round(intensitas["pct"] * rm, 2) for name, rm in rm_results.items()}
iter_results = {name: iterasi_beban(b0, rpe_target, k_val, max_iter) for name, b0 in beban_awal.items()}
pullup_result = iterasi_pullup(pu_rep, bb) if pu_rep > 0 else None


# ════════════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📊 GPP & Profil", "💪 Estimasi 1RM", "🔁 Iterasi Numerik", "📋 Rekomendasi Akhir"])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — GPP
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    gpp = gpp_result["gpp"]
    g   = gpp_result

    if gpp < 50:   badge, color = '<span class="badge badge-red">Kurang</span>',        "#f87171"
    elif gpp < 60: badge, color = '<span class="badge badge-amber">Cukup</span>',       "#fb923c"
    elif gpp < 70: badge, color = '<span class="badge badge-amber">Rata-rata</span>',   "#fbbf24"
    elif gpp < 80: badge, color = '<span class="badge badge-cyan">Baik</span>',         "#22d3ee"
    elif gpp < 90: badge, color = '<span class="badge badge-green">Sangat Baik</span>', "#4ade80"
    else:          badge, color = '<span class="badge badge-green">Luar Biasa</span>',  "#a3e635"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Skor GPP</div>
            <div class="metric-big">{gpp:.1f}</div>
            <div class="gpp-bar-wrap">
                <div class="gpp-bar-fill" style="width:{min(gpp,100):.1f}%;
                     background:linear-gradient(90deg,#0ea5e9,{color});"></div>
            </div>
            {badge}
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Intensitas Latihan</div>
            <div class="metric-big">{int(intensitas['pct']*100)}%</div>
            <div class="metric-label">dari 1RM · Rentang GPP {intensitas['range']}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        bmi = round(bb / ((tb / 100) ** 2), 1)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Profil Atlet</div>
            <div style="color:#e2e8f0;font-size:0.95rem;line-height:2;">
                {umur} tahun · {gender}<br>
                {bb} kg · {tb} cm<br>
                BMI <strong style="color:#22d3ee">{bmi}</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔢 Langkah Perhitungan GPP")
    st.markdown(f"""
    <div class="card">
        <div class="step-row"><span class="step-num">1</span>
        <span class="step-text"><b>Normalisasi Push-up:</b> S_PU = {g['pushup']} / 60 × 100 = <b>{g['s_pu']:.2f}</b></span></div>
        <div class="step-row"><span class="step-num">2</span>
        <span class="step-text"><b>Normalisasi Sit-up:</b> S_SU = {g['situp']} / 60 × 100 = <b>{g['s_su']:.2f}</b></span></div>
        <div class="step-row"><span class="step-num">3</span>
        <span class="step-text"><b>Normalisasi Lari:</b> S_L = {g['lari']} / 3000 × 100 = <b>{g['s_l']:.2f}</b></span></div>
        <div class="step-row"><span class="step-num">4</span>
        <span class="step-text"><b>GPP</b> = 0.4 × {g['s_l']:.2f} + 0.3 × {g['s_pu']:.2f} + 0.3 × {g['s_su']:.2f} = <b>{gpp:.2f}</b></span></div>
    </div>""", unsafe_allow_html=True)

    # ── Radar chart (matplotlib) ─────────────────────────────────────────────
    labels  = ["Push-up", "Sit-up", "Kardio"]
    vals    = [g['s_pu'], g['s_su'], g['s_l']]
    N       = len(labels)
    angles  = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_c  = vals + [vals[0]]
    angles_c = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD_BG)
    ax.plot(angles_c, vals_c, color=CYAN, linewidth=2)
    ax.fill(angles_c, vals_c, color=CYAN, alpha=0.15)
    ax.scatter(angles, vals, color=CYAN, s=60, zorder=5)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color=TEXT_CLR, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], color=TEXT_CLR, fontsize=7)
    ax.grid(color=GRID_CLR, linewidth=0.7)
    ax.spines['polar'].set_color(GRID_CLR)
    plt.tight_layout()

    col_radar, _ = st.columns([1, 1])
    with col_radar:
        st.pyplot(fig, use_container_width=False)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — 1RM
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("#### 📐 Estimasi 1RM — Rumus Epley: `1RM = W × (1 + R/30)`")

    if not rm_results:
        st.warning("Tidak ada data latihan valid. Isi beban & repetisi di sidebar.")
    else:
        rows = []
        for name, (w, r) in exercises.items():
            rm = rm_results[name]
            rows.append({"Latihan": name, "Beban (kg)": w, "Repetisi": r,
                         "1RM (kg)": round(rm, 2), "Beban Awal (kg)": beban_awal[name]})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Bar chart
        names_list = df["Latihan"].tolist()
        x = np.arange(len(names_list))
        w_bar = 0.35

        fig, ax = plt.subplots(figsize=(max(5, len(names_list)*1.4), 4))
        apply_dark(fig, ax)
        b1 = ax.bar(x - w_bar/2, df["1RM (kg)"],      w_bar, label="1RM",        color=CYAN,  alpha=0.85)
        b2 = ax.bar(x + w_bar/2, df["Beban Awal (kg)"], w_bar, label="Beban Awal", color=BLUE, alpha=0.75)
        ax.set_xticks(x); ax.set_xticklabels(names_list, color=TEXT_CLR, fontsize=9)
        ax.set_ylabel("kg", color=TEXT_CLR)
        ax.bar_label(b1, fmt="%.1f", color=CYAN,  fontsize=8, padding=3)
        ax.bar_label(b2, fmt="%.1f", color=BLUE,  fontsize=8, padding=3)
        ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=9)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ITERASI
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"#### 🔁 Fixed Point Iteration · Target RPE = {rpe_target} · k = {k_val}")
    st.markdown("Rumus: **W(n+1) = W(n) + k × (RPE_t − RPE(n))**")
    st.markdown("Konvergensi: **|RPE_t − RPE(n)| < 0.5** atau **|ΔW| < 0.5 kg**")

    if not iter_results:
        st.warning("Tidak ada data latihan.")
    else:
        for name, result in iter_results.items():
            with st.expander(f"📌 {name} — Konvergen iterasi ke-{result['converged_at']}", expanded=True):
                df_iter = pd.DataFrame(result['history'],
                                       columns=["Iterasi", "Beban (kg)", "RPE Estimasi", "|ΔRPE|", "|ΔW|"])
                st.dataframe(df_iter, use_container_width=True, hide_index=True)

                # Line chart
                fig, ax = plt.subplots(figsize=(6, 2.6))
                apply_dark(fig, ax)
                iters  = df_iter["Iterasi"].tolist()
                beban_ = df_iter["Beban (kg)"].tolist()
                ax.plot(iters, beban_, color=CYAN, linewidth=2, marker="o", markersize=5)
                ax.axhline(result['final_weight'], color=GREEN, linewidth=1.2,
                           linestyle="--", label=f"Beban Akhir: {result['final_weight']} kg")
                ax.set_xlabel("Iterasi", color=TEXT_CLR, fontsize=9)
                ax.set_ylabel("Beban (kg)", color=TEXT_CLR, fontsize=9)
                ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=8)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

    if pullup_result:
        st.markdown("---")
        st.markdown("#### 🔁 Pull-Up — Iterasi Progresi Repetisi")
        st.markdown("Rumus: **R(n+1) = R(n) + 0.2 × (R_t − R(n))**")
        df_pu = pd.DataFrame(pullup_result['history'], columns=["Iterasi", "Repetisi", "|ΔR|"])
        st.dataframe(df_pu, use_container_width=True, hide_index=True)
        if pullup_result['weighted']:
            st.success(f"✅ Pull-up ≥ 10 rep → **Weighted Pull-Up** +{pullup_result['extra_weight']:.1f} kg ({bb} kg × 5%)")
        else:
            st.info(f"🎯 Target progresi pull-up: **{pullup_result['target_rep']} rep**")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — REKOMENDASI AKHIR
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("#### 📋 Rekomendasi Beban Latihan Akhir")

    rows_final = []
    for name, result in iter_results.items():
        rows_final.append({
            "Latihan":         name,
            "1RM (kg)":        round(rm_results[name], 2),
            "Intensitas":      f"{int(intensitas['pct']*100)}%",
            "Beban Awal (kg)": beban_awal[name],
            "Beban Akhir (kg)":result['final_weight'],
            "RPE Akhir":       result['final_rpe'],
            "Iterasi":         result['converged_at'],
        })

    if pullup_result:
        rows_final.append({
            "Latihan":         "Pull-Up",
            "1RM (kg)":        "—",
            "Intensitas":      "BW",
            "Beban Awal (kg)": "BW",
            "Beban Akhir (kg)": f"BW + {pullup_result['extra_weight']:.1f} kg" if pullup_result['weighted']
                                 else f"BW ({pullup_result['target_rep']} rep)",
            "RPE Akhir":       "—",
            "Iterasi":         len(pullup_result['history']),
        })

    if rows_final:
        st.dataframe(pd.DataFrame(rows_final), use_container_width=True, hide_index=True)
    else:
        st.warning("Tidak ada data latihan untuk direkomendasikan.")

    st.markdown("---")
    st.markdown("#### 🧠 Analisis & Rekomendasi")

    gpp = gpp_result["gpp"]
    g   = gpp_result
    komponen = {"Kardio (Lari)": g['s_l'], "Push-up": g['s_pu'], "Sit-up": g['s_su']}
    lemah    = min(komponen, key=komponen.get)
    terkuat  = max(komponen, key=komponen.get)

    analisis_map = [
        (50,  "Kondisi fisik **kurang** — prioritaskan latihan aerobik dan kapasitas fungsional dasar."),
        (60,  "Kondisi fisik **cukup** — butuh peningkatan konsisten di semua aspek kebugaran."),
        (70,  "Kondisi fisik **rata-rata** — ada ruang signifikan untuk berkembang."),
        (80,  "Kondisi fisik **baik** — siap program latihan terstruktur dengan beban menengah-tinggi."),
        (90,  "Kondisi fisik **sangat baik** — dapat menangani volume dan intensitas tinggi."),
        (200, "Kondisi fisik **luar biasa** — pertahankan dan fokus pada spesialisasi."),
    ]
    analisis_gpp = next(txt for thr, txt in analisis_map if gpp < thr)

    push_ex  = [n for n in iter_results if any(k in n for k in ["Bench", "OHP", "Push"])]
    pull_ex  = [n for n in iter_results if any(k in n for k in ["Pull", "Lat", "Row"])]
    legs_ex  = [n for n in iter_results if any(k in n for k in ["Squat", "Deadlift", "Leg"])]

    def avg_rm(names):
        vals = [rm_results[n] for n in names if n in rm_results]
        return round(sum(vals)/len(vals), 1) if vals else None

    push_avg = avg_rm(push_ex)
    pull_avg = avg_rm(pull_ex)
    legs_avg = avg_rm(legs_ex)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
**Tingkat Kebugaran (GPP = {gpp:.1f})**

{analisis_gpp}

- **Terkuat:** {terkuat} ({komponen[terkuat]:.1f}/100)
- **Terlemah:** {lemah} ({komponen[lemah]:.1f}/100) — prioritaskan peningkatan di sini
        """)
    with col2:
        st.markdown("**Kekuatan Relatif per Pola Gerak (rata-rata 1RM)**")
        if push_avg: st.markdown(f"- 🔵 **Push:** {push_avg} kg")
        if pull_avg: st.markdown(f"- 🟢 **Pull:** {pull_avg} kg")
        if legs_avg: st.markdown(f"- 🟡 **Legs:** {legs_avg} kg")
        if not any([push_avg, pull_avg, legs_avg]):
            st.markdown("_Data belum cukup untuk analisis pola gerak._")

    st.markdown("""
**Progresi Latihan Berikutnya**
- Tambah **2.5–5 kg** setelah semua set selesai dengan RPE < 8
- Terapkan **progressive overload** mingguan pada latihan compound
- Jika RPE selalu ≥ 9, turunkan beban 5–10% dan perbaiki teknik
- Evaluasi ulang GPP setiap **4–6 minggu**
    """)

st.markdown("---")
st.caption("GPP Calculator · Epley 1RM + Fixed Point Iteration · Streamlit & Python")