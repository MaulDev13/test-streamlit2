import streamlit as st

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
        <h1>🚀 Selamat Datang di My Streamlit App</h1>
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
    st.title("📊 Dashboard")
    st.write("Konten dashboard akan ditampilkan di sini.")

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