import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from calculations import (
    hitung_gpp,
    hitung_1rm,
    tentukan_intensitas,
    iterasi_beban,
    iterasi_pullup,
)

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator GPP & Beban Latihan",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0f1117; }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #e2e8f0;
        line-height: 1.15;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .accent { color: #22d3ee; }

    .card {
        background: #1e2130;
        border: 1px solid #2d3348;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.8rem;
    }
    .metric-big {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #22d3ee;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.2rem;
    }

    .gpp-bar-wrap {
        background: #2d3348;
        border-radius: 999px;
        height: 14px;
        width: 100%;
        margin: 0.6rem 0 0.3rem;
        overflow: hidden;
    }
    .gpp-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #0ea5e9, #22d3ee);
        transition: width 0.6s ease;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .badge-cyan  { background: #083344; color: #22d3ee; }
    .badge-green { background: #052e16; color: #4ade80; }
    .badge-amber { background: #431407; color: #fb923c; }
    .badge-red   { background: #3f0b0b; color: #f87171; }

    .stDataFrame { border-radius: 8px; overflow: hidden; }
    thead tr th { background: #2d3348 !important; color: #94a3b8 !important; }

    .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px; height: 28px;
        border-radius: 50%;
        background: #083344;
        color: #22d3ee;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        flex-shrink: 0;
    }
    .step-row { display: flex; align-items: center; margin-bottom: 0.5rem; }
    .step-text { color: #cbd5e1; font-size: 0.92rem; }

    div[data-testid="stSidebar"] {
        background: #13161f;
        border-right: 1px solid #2d3348;
    }
    div[data-testid="stSidebar"] label { color: #94a3b8 !important; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR — INPUT
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
    st.caption("Isi dengan beban & repetisi yang sudah dilakukan.")

    latihan_data = {}

    col_a, col_b = st.columns(2)
    with col_a:
        bp_w = st.number_input("Bench Press — kg", 0.0, 300.0, 60.0, 2.5)
    with col_b:
        bp_r = st.number_input("Bench Press — rep", 0, 30, 8)

    col_a, col_b = st.columns(2)
    with col_a:
        sq_w = st.number_input("Squat — kg", 0.0, 400.0, 80.0, 2.5)
    with col_b:
        sq_r = st.number_input("Squat — rep", 0, 30, 8)

    col_a, col_b = st.columns(2)
    with col_a:
        lp_w = st.number_input("Lat Pulldown — kg", 0.0, 200.0, 50.0, 2.5)
    with col_b:
        lp_r = st.number_input("Lat Pulldown — rep", 0, 30, 10)

    col_a, col_b = st.columns(2)
    with col_a:
        dl_w = st.number_input("Deadlift — kg", 0.0, 400.0, 0.0, 2.5)
    with col_b:
        dl_r = st.number_input("Deadlift — rep", 0, 30, 0)

    col_a, col_b = st.columns(2)
    with col_a:
        ohp_w = st.number_input("OHP — kg", 0.0, 200.0, 0.0, 2.5)
    with col_b:
        ohp_r = st.number_input("OHP — rep", 0, 30, 0)

    pu_rep = st.number_input("Pull-Up Maks (rep, 0 = skip)", 0, 50, 6)

    st.markdown("---")
    st.markdown("### ⚙️ Parameter Iterasi")
    rpe_target = st.slider("Target RPE", 6.0, 9.0, 8.0, 0.5)
    k_val      = st.slider("Konstanta k", 0.5, 5.0, 2.0, 0.5)
    max_iter   = st.slider("Max Iterasi", 5, 30, 15)

    hitung = st.button("🔢 Hitung GPP & Rekomendasi", use_container_width=True, type="primary")


# ════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="hero-title">Kalkulator <span class="accent">GPP</span> &<br>Rekomendasi Beban Latihan</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Berbasis metode numerik — Fixed Point Iteration · Epley 1RM · Intensity Scaling</p>', unsafe_allow_html=True)

if not hitung:
    st.info("👈 Isi data di sidebar, lalu klik **Hitung GPP & Rekomendasi**.")
    st.stop()

# ─── Collect exercises ───────────────────────────────────────────────────────
exercises_raw = {
    "Bench Press":  (bp_w,  bp_r),
    "Squat":        (sq_w,  sq_r),
    "Lat Pulldown": (lp_w,  lp_r),
    "Deadlift":     (dl_w,  dl_r),
    "OHP":          (ohp_w, ohp_r),
}
exercises = {n: v for n, v in exercises_raw.items() if v[0] > 0 and v[1] > 0}

# ─── Run calculations ────────────────────────────────────────────────────────
gpp_result   = hitung_gpp(pushup, situp, lari)
intensitas   = tentukan_intensitas(gpp_result["gpp"])
rm_results   = {name: hitung_1rm(w, r) for name, (w, r) in exercises.items()}
beban_awal   = {name: round(intensitas["pct"] * rm, 2) for name, rm in rm_results.items()}

iter_results = {}
for name, b0 in beban_awal.items():
    iter_results[name] = iterasi_beban(b0, rpe_target, k_val, max_iter)

pullup_result = None
if pu_rep > 0:
    pullup_result = iterasi_pullup(pu_rep, bb)


# ════════════════════════════════════════════════════════════════════════════
# TAB LAYOUT
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📊 GPP & Profil", "💪 Estimasi 1RM", "🔁 Iterasi Numerik", "📋 Rekomendasi Akhir"])


# ─── TAB 1: GPP ──────────────────────────────────────────────────────────────
with tab1:
    gpp = gpp_result["gpp"]

    # Badge category
    if gpp < 50:
        badge = '<span class="badge badge-red">Kurang</span>'
        color = "#f87171"
    elif gpp < 60:
        badge = '<span class="badge badge-amber">Cukup</span>'
        color = "#fb923c"
    elif gpp < 70:
        badge = '<span class="badge badge-amber">Rata-rata</span>'
        color = "#fbbf24"
    elif gpp < 80:
        badge = '<span class="badge badge-cyan">Baik</span>'
        color = "#22d3ee"
    elif gpp < 90:
        badge = '<span class="badge badge-green">Sangat Baik</span>'
        color = "#4ade80"
    else:
        badge = '<span class="badge badge-green">Luar Biasa</span>'
        color = "#a3e635"

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Skor GPP</div>
            <div class="metric-big">{gpp:.1f}</div>
            <div class="gpp-bar-wrap">
                <div class="gpp-bar-fill" style="width:{min(gpp,100):.1f}%; background: linear-gradient(90deg,#0ea5e9,{color});"></div>
            </div>
            {badge}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Intensitas Latihan</div>
            <div class="metric-big">{int(intensitas['pct']*100)}%</div>
            <div class="metric-label">dari 1RM · Rentang GPP {intensitas['range']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        bmi = round(bb / ((tb / 100) ** 2), 1)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Profil Atlet</div>
            <div style="color:#e2e8f0; font-size:0.95rem; line-height:1.9;">
                {umur} tahun · {gender}<br>
                {bb} kg · {tb} cm<br>
                BMI <strong style="color:#22d3ee">{bmi}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔢 Langkah Perhitungan GPP")

    g = gpp_result
    steps_html = f"""
    <div class="card">
        <div class="step-row"><span class="step-num">1</span>
        <span class="step-text"><b>Normalisasi Push-up:</b> S_PU = {g['pushup']} / 60 × 100 = <b>{g['s_pu']:.2f}</b></span></div>

        <div class="step-row"><span class="step-num">2</span>
        <span class="step-text"><b>Normalisasi Sit-up:</b> S_SU = {g['situp']} / 60 × 100 = <b>{g['s_su']:.2f}</b></span></div>

        <div class="step-row"><span class="step-num">3</span>
        <span class="step-text"><b>Normalisasi Lari:</b> S_L = {g['lari']} / 3000 × 100 = <b>{g['s_l']:.2f}</b></span></div>

        <div class="step-row"><span class="step-num">4</span>
        <span class="step-text"><b>GPP:</b> 0.4 × {g['s_l']:.2f} + 0.3 × {g['s_pu']:.2f} + 0.3 × {g['s_su']:.2f} = <b>{gpp:.2f}</b></span></div>
    </div>
    """
    st.markdown(steps_html, unsafe_allow_html=True)

    # Radar chart
    categories = ["Push-up", "Sit-up", "Kardio"]
    values = [g['s_pu'], g['s_su'], g['s_l']]
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(34,211,238,0.15)',
        line=dict(color='#22d3ee', width=2),
        marker=dict(size=8, color='#22d3ee'),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='#1e2130',
            radialaxis=dict(visible=True, range=[0, 100], color='#475569', gridcolor='#2d3348'),
            angularaxis=dict(color='#94a3b8', gridcolor='#2d3348'),
        ),
        paper_bgcolor='#0f1117',
        plot_bgcolor='#0f1117',
        font=dict(color='#94a3b8', family='Inter'),
        margin=dict(l=60, r=60, t=30, b=30),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)


# ─── TAB 2: 1RM ──────────────────────────────────────────────────────────────
with tab2:
    st.markdown("#### 📐 Estimasi 1RM — Rumus Epley: 1RM = W × (1 + R/30)")

    if not rm_results:
        st.warning("Tidak ada data latihan yang valid. Isi beban & repetisi di sidebar.")
    else:
        rows = []
        for name, (w, r) in exercises.items():
            rm = rm_results[name]
            rows.append({"Latihan": name, "Beban (kg)": w, "Repetisi": r,
                         "1RM (kg)": round(rm, 2), "Beban Awal (kg)": beban_awal[name]})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='1RM', x=df['Latihan'], y=df['1RM (kg)'],
                               marker_color='#22d3ee', opacity=0.8))
        fig2.add_trace(go.Bar(name='Beban Awal', x=df['Latihan'], y=df['Beban Awal (kg)'],
                               marker_color='#0ea5e9', opacity=0.6))
        fig2.update_layout(
            barmode='group',
            paper_bgcolor='#0f1117', plot_bgcolor='#1e2130',
            font=dict(color='#94a3b8', family='Inter'),
            legend=dict(bgcolor='#1e2130', bordercolor='#2d3348'),
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            xaxis=dict(gridcolor='#2d3348'), yaxis=dict(gridcolor='#2d3348'),
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─── TAB 3: ITERASI ──────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"#### 🔁 Fixed Point Iteration · Target RPE = {rpe_target} · k = {k_val}")
    st.markdown("Rumus: **W(n+1) = W(n) + k × (RPE_t − RPE(n))**")
    st.markdown("Konvergensi jika **|RPE_t − RPE(n)| < 0.5** atau **|ΔW| < 0.5 kg**")

    if not iter_results:
        st.warning("Tidak ada data latihan.")
    else:
        for name, result in iter_results.items():
            with st.expander(f"📌 {name} — Konvergen di iterasi {result['converged_at']}", expanded=True):
                df_iter = pd.DataFrame(result['history'])
                df_iter.columns = ["Iterasi", "Beban (kg)", "RPE Estimasi", "|ΔRPE|", "|ΔW|"]
                st.dataframe(df_iter, use_container_width=True, hide_index=True)

                fig3 = go.Figure()
                iters = df_iter["Iterasi"].tolist()
                fig3.add_trace(go.Scatter(x=iters, y=df_iter["Beban (kg)"],
                                           mode='lines+markers', name='Beban',
                                           line=dict(color='#22d3ee', width=2),
                                           marker=dict(size=7)))
                fig3.add_hline(y=result['final_weight'], line_dash='dash',
                               line_color='#4ade80', annotation_text='Beban Akhir')
                fig3.update_layout(
                    paper_bgcolor='#0f1117', plot_bgcolor='#1e2130',
                    font=dict(color='#94a3b8', family='Inter'),
                    margin=dict(l=20, r=20, t=10, b=20),
                    height=220,
                    xaxis=dict(gridcolor='#2d3348', title='Iterasi'),
                    yaxis=dict(gridcolor='#2d3348', title='Beban (kg)'),
                )
                st.plotly_chart(fig3, use_container_width=True)

    if pullup_result:
        st.markdown("---")
        st.markdown("#### 🔁 Pull-Up — Iterasi Progresi Repetisi")
        st.markdown("Rumus: **R(n+1) = R(n) + 0.2 × (R_t − R(n))**")
        df_pu = pd.DataFrame(pullup_result['history'])
        df_pu.columns = ["Iterasi", "Repetisi", "|ΔR|"]
        st.dataframe(df_pu, use_container_width=True, hide_index=True)
        if pullup_result['weighted']:
            st.success(f"✅ Pull-up ≥ 10 rep → Rekomendasikan **Weighted Pull-Up** +{pullup_result['extra_weight']:.1f} kg ({bb} × 5%)")
        else:
            st.info(f"🎯 Target progressi pull-up: **{pullup_result['target_rep']} rep**")


# ─── TAB 4: REKOMENDASI ───────────────────────────────────────────────────────
with tab4:
    st.markdown("#### 📋 Rekomendasi Beban Latihan Akhir")

    rows_final = []
    for name, result in iter_results.items():
        rows_final.append({
            "Latihan": name,
            "1RM (kg)": round(rm_results[name], 2),
            "Intensitas": f"{int(intensitas['pct']*100)}%",
            "Beban Awal (kg)": beban_awal[name],
            "Beban Akhir (kg)": result['final_weight'],
            "RPE Akhir": result['final_rpe'],
            "Iterasi": result['converged_at'],
        })

    if pullup_result:
        rows_final.append({
            "Latihan": "Pull-Up",
            "1RM (kg)": "—",
            "Intensitas": "BW",
            "Beban Awal (kg)": "BW",
            "Beban Akhir (kg)": f"BW + {pullup_result['extra_weight']:.1f} kg" if pullup_result['weighted'] else f"BW ({pullup_result['target_rep']} rep)",
            "RPE Akhir": "—",
            "Iterasi": len(pullup_result['history']),
        })

    if rows_final:
        df_final = pd.DataFrame(rows_final)
        st.dataframe(df_final, use_container_width=True, hide_index=True)
    else:
        st.warning("Tidak ada data latihan untuk direkomendasikan.")

    st.markdown("---")
    st.markdown("#### 🧠 Analisis & Rekomendasi")

    gpp = gpp_result["gpp"]
    g   = gpp_result

    # Weakness analysis
    komponen = {"Kardio (Lari)": g['s_l'], "Push-up": g['s_pu'], "Sit-up": g['s_su']}
    lemah    = min(komponen, key=komponen.get)
    terkuat  = max(komponen, key=komponen.get)

    if gpp < 50:
        analisis_gpp = "Kondisi fisik **kurang** — prioritaskan latihan aerobik dan peningkatan kapasitas fungsional dasar."
    elif gpp < 60:
        analisis_gpp = "Kondisi fisik **cukup** — butuh peningkatan konsisten di semua aspek kebugaran."
    elif gpp < 70:
        analisis_gpp = "Kondisi fisik **rata-rata** — ada ruang signifikan untuk berkembang di latihan beban dan aerobik."
    elif gpp < 80:
        analisis_gpp = "Kondisi fisik **baik** — siap untuk program latihan terstruktur dengan beban menengah-tinggi."
    elif gpp < 90:
        analisis_gpp = "Kondisi fisik **sangat baik** — dapat menangani volume dan intensitas tinggi."
    else:
        analisis_gpp = "Kondisi fisik **luar biasa** — pertahankan dan fokus pada spesialisasi."

    # Push / pull / legs classification
    push_ex  = [n for n in iter_results if any(k in n for k in ["Bench", "OHP", "Push"])]
    pull_ex  = [n for n in iter_results if any(k in n for k in ["Pull", "Lat", "Row"])]
    legs_ex  = [n for n in iter_results if any(k in n for k in ["Squat", "Deadlift", "Leg"])]

    def avg_rm(names):
        vals = [rm_results[n] for n in names if n in rm_results]
        return round(sum(vals) / len(vals), 1) if vals else None

    push_avg = avg_rm(push_ex)
    pull_avg = avg_rm(pull_ex)
    legs_avg = avg_rm(legs_ex)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Tingkat Kebugaran (GPP = {gpp:.1f})**

        {analisis_gpp}

        **Komponen Terkuat:** {terkuat} ({komponen[terkuat]:.1f}/100)
        **Komponen Terlemah:** {lemah} ({komponen[lemah]:.1f}/100) — prioritaskan peningkatan di area ini.
        """)

    with col2:
        st.markdown("**Kekuatan Relatif per Pola Gerak (rata-rata 1RM)**")
        if push_avg: st.markdown(f"- 🔵 **Push (dorong):** {push_avg} kg")
        if pull_avg: st.markdown(f"- 🟢 **Pull (tarik):** {pull_avg} kg")
        if legs_avg: st.markdown(f"- 🟡 **Legs (kaki):** {legs_avg} kg")
        if not any([push_avg, pull_avg, legs_avg]):
            st.markdown("_Data latihan belum cukup untuk analisis pola gerak._")

    st.markdown("""
    **Progresi Latihan Berikutnya**
    - Tambah beban **2.5–5 kg** setelah berhasil menyelesaikan semua set dengan RPE < 8
    - Gunakan **progressive overload** mingguan pada latihan compound utama
    - Jika RPE selalu ≥ 9, turunkan beban 5–10% dan fokus pada teknik
    - Evaluasi ulang GPP tiap **4–6 minggu** untuk menyesuaikan intensitas
    """)

st.markdown("---")
st.caption("GPP Calculator · Berbasis metode numerik Epley 1RM + Fixed Point Iteration · Dibuat dengan Streamlit & Python")