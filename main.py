import streamlit as st
import pandas as pd
import numpy as np

# ==========================
# Fungsi Generate Data
# ==========================
def generate_population_data(
    start_year=2015,
    end_year=2025,
    initial_population=1000000
):
    years = list(range(start_year, end_year + 1))

    population = [initial_population]

    for _ in range(1, len(years)):
        growth_rate = np.random.uniform(0.8, 2.5) / 100
        next_population = int(population[-1] * (1 + growth_rate))
        population.append(next_population)

    df = pd.DataFrame({
        "Tahun": years,
        "Populasi": population
    })

    return df

# Konfigurasi halaman
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 3rem 1rem;
    border-radius: 15px;
    background: linear-gradient(90deg, #1f77b4, #4CAF50);
    color: white;
}
.feature-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #f5f5f5;
    text-align: center;
    height: 180px;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Navigasi",
    ["Beranda", "Dashboard", "Analisis", "Tentang"]
)

# Halaman Beranda
if menu == "Beranda":

    st.markdown("""
    <div class="hero">
        <h1>🚀 Selamat Datang di Ahmad Learning</h1>
        <p>Aplikasi berbasis Python & Streamlit untuk analisis data dan visualisasi interaktif.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Dashboard</h3>
            <p>Lihat ringkasan data secara real-time.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📈 Analisis</h3>
            <p>Analisis data dengan berbagai metode.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>⚡ Cepat & Mudah</h3>
            <p>Interface sederhana dan responsif.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.subheader("🎯 Tentang Aplikasi")
    st.write("""
    Aplikasi ini dibuat menggunakan **Python** dan **Streamlit**
    untuk membantu pengguna melakukan visualisasi, monitoring,
    dan analisis data secara interaktif.
    """)

    st.info("Mulai dengan memilih menu di sidebar.")

# Halaman Dashboard
elif menu == "Dashboard":
    st.title("📊 Dashboard Populasi")

    if st.button("Generate Data Populasi"):
        df_pop = generate_population_data()

        st.subheader("Data Populasi")
        st.dataframe(df_pop, use_container_width=True)

        st.subheader("Grafik Pertumbuhan Populasi")
        st.line_chart(
            df_pop.set_index("Tahun")["Populasi"]
        )

        total_growth = (
            (df_pop["Populasi"].iloc[-1] -
             df_pop["Populasi"].iloc[0])
            / df_pop["Populasi"].iloc[0]
        ) * 100

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Populasi Awal",
                f"{df_pop['Populasi'].iloc[0]:,}"
            )

        with col2:
            st.metric(
                "Pertumbuhan Total",
                f"{total_growth:.2f}%"
            )

# Halaman Analisis
elif menu == "Analisis":
    st.title("📈 Analisis Data")
    st.write("Konten analisis akan ditampilkan di sini.")

# Halaman Tentang
elif menu == "Tentang":
    st.title("ℹ️ Tentang")
    st.write("""
    Versi: 1.0.0

    Dibangun menggunakan:
    - Python
    - Streamlit
    """)

# Footer
st.markdown("""
<div class="footer">
    © 2026 My Streamlit App | Dibuat dengan ❤️ menggunakan Streamlit
</div>
""", unsafe_allow_html=True)