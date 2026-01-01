import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- 1. CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="BRB - Fuzzy House Analyzer", 
    page_icon="https://i.ibb.co.com/yFptBkkq/logotab.png", 
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown(f"""
    <style>
    /* Global Smooth Scroll */
    html {{
        scroll-behavior: smooth;
    }}
    .block-container {{
        padding: 0rem !important;
    }}
    
    /* Sticky Navigation Bar - Dioptimalkan untuk LOGO PUTIH */
    .nav-bar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        padding: 0 8%;
        display: flex;
        align-items: center;
        z-index: 999999; /* Sangat tinggi agar tidak tertutup */
        background: rgba(0, 0, 0, 0.5); /* Background lebih gelap agar logo putih kontras */
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .logo-img {{
        height: 35px;
        width: auto;
        display: block;
        /* Memastikan logo putih benar-benar cerah */
        filter: drop-shadow(0px 0px 5px rgba(255,255,255,0.2)); 
    }}
    
    /* Hero Section */
    .hero-section {{
        background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                          url("https://i.ibb.co.com/Pzw0zjGX/perumahan.webp");
        background-size: cover;
        background-position: center;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        padding: 0 20px;
    }}
    
    .hero-title {{
        font-size: clamp(35px, 8vw, 75px);
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: -2px;
        line-height: 1;
    }}
    
    .hero-subtitle {{
        font-size: clamp(16px, 2.5vw, 24px);
        margin-bottom: 40px;
        opacity: 0.9;
        max-width: 800px;
        font-weight: 300;
        line-height: 1.4;
    }}

    /* Modern CTA Button */
    .cta-button {{
        background: linear-gradient(135deg, #3498DB 0%, #2E86C1 100%);
        color: white !important;
        padding: 18px 45px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 16px;
        text-decoration: none !important;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    .cta-button:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(46, 134, 193, 0.5);
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 60px 20px;
        color: #8899A6;
    }}

    /* Mobile Responsive */
    @media (max-width: 768px) {{
        .nav-bar {{ height: 60px; padding: 0 5%; }}
        .logo-img {{ height: 25px; }}
        div.stButton > button {{ width: 100% !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
st.markdown('''
    <div class="nav-bar">
        <img src="https://i.ibb.co.com/gLtn0GCT/logo.png" class="logo-img" alt="BRB Logo">
    </div>
''', unsafe_allow_html=True)

# --- 3. SISTEM FUZZY (LOGIC) ---
@st.cache_resource
def init_fuzzy():
    le = ctrl.Antecedent(np.linspace(0, 2000, 1000), 'Luas Efektif')
    kf = ctrl.Antecedent(np.linspace(0, 25, 200), 'Kapasitas Fasilitas')
    h = ctrl.Antecedent(np.linspace(0, 20000000000, 1000), 'Harga(Rp)')
    iw = ctrl.Consequent(np.linspace(0, 100, 101), 'Indeks Kewajaran')

    le['Kecil'] = fuzz.trapmf(le.universe, [0, 0, 100, 250])
    le['Sedang'] = fuzz.trimf(le.universe, [150, 400, 750])
    le['Besar'] = fuzz.trapmf(le.universe, [600, 900, 2000, 2000])

    kf['Kurang'] = fuzz.trapmf(kf.universe, [0, 0, 3, 5])
    kf['Cukup'] = fuzz.trimf(kf.universe, [4, 8, 14])
    kf['Banyak'] = fuzz.trapmf(kf.universe, [10, 15, 25, 25])

    h['Murah'] = fuzz.trapmf(h.universe, [0, 0, 900000000, 1100000000])
    h['Normal'] = fuzz.trimf(h.universe, [1000000000, 2000000000, 4200000000])
    h['Mahal'] = fuzz.trapmf(h.universe, [4000000000, 7000000000, 20000000000, 20000000000])

    iw['Sangat Tidak Wajar'] = fuzz.trimf(iw.universe, [0, 0, 35])
    iw['Tidak Wajar'] = fuzz.trimf(iw.universe, [25, 45, 65])
    iw['Cukup Wajar'] = fuzz.trimf(iw.universe, [55, 70, 85])
    iw['Wajar'] = fuzz.trimf(iw.universe, [75, 85, 95])
    iw['Sangat Wajar'] = fuzz.trimf(iw.universe, [85, 100, 100])

    # Rules Base
    rules = [
        ctrl.Rule(h['Mahal'] & le['Kecil'], iw['Sangat Tidak Wajar']),
        ctrl.Rule(h['Mahal'] & kf['Kurang'], iw['Sangat Tidak Wajar']),
        ctrl.Rule(h['Normal'] & le['Sedang'] & kf['Cukup'], iw['Cukup Wajar']),
        ctrl.Rule(h['Murah'] & le['Besar'], iw['Sangat Wajar']),
        ctrl.Rule(h['Normal'] & le['Besar'] & kf['Banyak'], iw['Sangat Wajar']),
        ctrl.Rule(h['Murah'] & kf['Banyak'], iw['Sangat Wajar']),
        ctrl.Rule(h['Normal'] & le['Sedang'] & kf['Banyak'], iw['Wajar']),
        ctrl.Rule(h['Normal'] & le['Besar'] & kf['Cukup'], iw['Wajar']),
        ctrl.Rule(h['Murah'] & le['Sedang'] & kf['Cukup'], iw['Wajar'])
    ]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

# --- 4. HERO SECTION ---
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">Pintar Menilai Properti</h1>
        <p class="hero-subtitle">
            Uji kelayakan harga hunian Anda dengan <b>Logika Fuzzy Mamdani</b> secara objektif.<br> 
            Analisis divalidasi menggunakan dataset pasar Bandung tahun 2024,<br>
            yang dihimpun secara mendalam melalui portal <i>rumah123.com</i>.
        </p>
        <div style="margin-top: 20px;">
            <a href="#input-area" class="cta-button">
                MULAI ANALISIS SEKARANG
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Anchor Point
st.markdown('<div id="input-area" style="padding-top: 80px;"></div>', unsafe_allow_html=True)

# --- 5. MAIN CONTENT ---
l_pad, content, r_pad = st.columns([0.1, 0.8, 0.1])

with content:
    st.markdown("## 🏠 Masukkan Data Properti")
    st.write("Lengkapi formulir di bawah untuk mendapatkan estimasi kewajaran harga.")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        lt = st.number_input("Luas Tanah (m²)", min_value=0, value=150, step=10)
        lb = st.number_input("Luas Bangunan (m²)", min_value=0, value=110, step=10)
        harga_raw = st.number_input("Harga Penawaran (Rp)", min_value=100000000, value=810000000, step=10000000)
        st.info(f"💰 **Konfirmasi Harga:** Rp {harga_raw:,.0f}".replace(",", "."))

    with col2:
        kt = st.slider("Jumlah Kamar Tidur", 0, 10, 2)
        km = st.slider("Jumlah Kamar Mandi", 0, 10, 1)
        gr = st.slider("Kapasitas Garasi", 0, 10, 1)

    st.write("") 
    btn_run = st.button("HITUNG KEWAJARAN HARGA", use_container_width=True, type="primary")

    if btn_run:
        try:
            sim = init_fuzzy()
            val_le = lt + lb
            val_kf = kt + km + gr
            
            sim.input['Luas Efektif'] = min(val_le, 2000)
            sim.input['Kapasitas Fasilitas'] = min(val_kf, 25)
            sim.input['Harga(Rp)'] = min(harga_raw, 20000000000)
            
            sim.compute()
            skor = sim.output['Indeks Kewajaran']

            st.markdown("---")
            st.write("### 📊 Hasil Analisis")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Skor Kewajaran", f"{skor:.1f}%")
            m2.metric("Luas Efektif", f"{val_le} m²")
            m3.metric("Total Fasilitas", f"{val_kf}")

            if skor >= 85: 
                st.success("KESIMPULAN: **SANGAT WAJAR (BEST DEAL)**")
                st.balloons()
            elif skor >= 75: st.info("KESIMPULAN: **WAJAR (GOOD DEAL)**")
            elif skor >= 55: st.warning("KESIMPULAN: **CUKUP WAJAR (HARGA PASAR)**")
            else: st.error("KESIMPULAN: **TIDAK WAJAR (KEMAHALAN)**")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# --- 6. FOOTER ---
st.markdown(f"""
    <div class="footer">
        <hr style="border: 0.5px solid #EAECEE; width: 80%; margin: auto; margin-bottom: 30px;">
        <p>© 2026 | BRB - Bandung Real-Estate Benchmark</p>
        <p>Dibuat oleh <b><a href="https://irfannurf.my.id" target="_blank">Irfan Nur Fahrudin</a></b></p>
        <p style="font-size: 14px; margin-top: 10px;">
            <a href="https://github.com/irfannurf21" target="_blank">GitHub</a> • 
            <a href="https://irfannurf.my.id" target="_blank">Portfolio</a>
        </p>
    </div>

""", unsafe_allow_html=True)
