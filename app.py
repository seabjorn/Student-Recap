import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# -------------------------------------------------------
# ⚙️ KONFIGURASI AWAL
# -------------------------------------------------------
st.set_page_config(
    page_title="Rekap Pelanggaran & Prestasi Siswa",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# 🎨 CSS DARK THEME PREMIUM
# -------------------------------------------------------
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #10b981;
    --bg-main: #0a0a0f;
    --bg-card: #1a1a24;
    --bg-sidebar: #13131b;
    --text-primary: #e5e7eb;
    --text-secondary: #9ca3af;
    --border: #2d2d3d;
    --shadow: rgba(0, 0, 0, 0.5);
}

html, body, .main, .stApp {
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
    padding: 2rem 1rem;
}

section[data-testid="stSidebar"] h2 {
    color: var(--primary);
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 500;
    font-size: 0.9rem;
}

section[data-testid="stSidebar"] [data-baseweb="select"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
}

section[data-testid="stSidebar"] button {
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    transition: all 0.3s;
    width: 100%;
}

section[data-testid="stSidebar"] button:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Header */
.main-header {
    background: var(--bg-card);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    box-shadow: 0 4px 20px var(--shadow);
}

.main-header h1 {
    color: var(--primary);
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}

.main-header p {
    color: var(--text-secondary);
    margin: 0.5rem 0 0 0;
    font-size: 0.95rem;
}

/* Cards */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px var(--shadow);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px var(--shadow);
    border-color: var(--primary);
}

.card h2, .card h3 {
    color: var(--primary);
    margin-bottom: 1rem;
    font-weight: 600;
}

/* Stat Boxes */
.stat-box {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    color: white;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    transition: all 0.3s;
}

.stat-box:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 30px rgba(99, 102, 241, 0.5);
}

.stat-box .icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.stat-box .label {
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 500;
}

.stat-box .value {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 0.5rem;
}

/* Form Elements */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    padding: 0.6rem !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}

/* Buttons */
.stButton button {
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton button:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.stDataFrame table {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stDataFrame th {
    background: var(--primary) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 1rem !important;
}

.stDataFrame td {
    border-color: var(--border) !important;
    padding: 0.8rem !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* Metrics */
.stMetric {
    background: var(--bg-card);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.stMetric label {
    color: var(--text-secondary) !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: var(--primary) !important;
}

/* Info/Warning/Success boxes */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}

/* Download button */
.stDownloadButton button {
    background: var(--secondary);
    color: white;
}

.stDownloadButton button:hover {
    background: #059669;
}

/* Caption */
.caption {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-main);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# 🔐 GOOGLE SHEETS SETUP
# -------------------------------------------------------
def get_gspread_client():
    """Inisialisasi client gspread - no caching untuk stabilitas"""
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    
    # Gunakan authorize() method yang lebih stabil
    client = gspread.authorize(creds)
    
    return client

@st.cache_data(ttl=300)
def load_data():
    """Load data dari Google Sheets dengan retry mechanism"""
    import time
    
    SPREADSHEET_ID = "1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            client = get_gspread_client()
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            
            ws_siswa = spreadsheet.worksheet("data_siswa")
            ws_rekap = spreadsheet.worksheet("rekap_pelanggaran")

            # 📊 Ambil semua data (termasuk header)
            all_siswa = ws_siswa.get_all_values()
            all_rekap = ws_rekap.get_all_values()

            # ✅ Data siswa
            if len(all_siswa) <= 1:
                df_siswa = pd.DataFrame(columns=["Nama", "Kelas", "NIS"])
            else:
                df_siswa = pd.DataFrame(all_siswa[1:], columns=all_siswa[0])
                df_siswa.columns = df_siswa.columns.str.strip()

            # ✅ Data rekap pelanggaran
            if len(all_rekap) <= 1:
                df_rekap = pd.DataFrame(columns=[
                    "Tanggal", "Nama Siswa", "Kelas", "pelanggaran",
                    "Poin Pelanggaran", "Poin Prestasi", "Total Poin", "Poin Kumulatif"
                ])
            else:
                df_rekap = pd.DataFrame(all_rekap[1:], columns=all_rekap[0])
                df_rekap.columns = df_rekap.columns.str.strip()

                # Konversi tipe data numerik dengan error handling
                for col in ["Poin Pelanggaran", "Poin Prestasi", "Total Poin", "Poin Kumulatif"]:
                    if col in df_rekap.columns:
                        df_rekap[col] = pd.to_numeric(df_rekap[col], errors='coerce').fillna(0)

            return df_siswa, df_rekap, ws_siswa, ws_rekap
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ Koneksi gagal (percobaan {attempt + 1}/{max_retries}), mencoba lagi...")
                time.sleep(2)  # Tunggu 2 detik sebelum retry
            else:
                st.error(f"❌ Gagal memuat data setelah {max_retries} percobaan: {e}")
                st.info("💡 **Solusi:**\n"
                       "1. Cek koneksi internet Anda\n"
                       "2. Pastikan Google Sheets bisa diakses\n"
                       "3. Tunggu beberapa saat lalu klik 'Refresh Data'\n"
                       "4. Pastikan service account punya akses ke spreadsheet")
                st.stop()


df_siswa, df_rekap, ws_siswa, ws_rekap = load_data()

# -------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION
# -------------------------------------------------------
with st.sidebar:
    st.markdown("<h2>📚 Dashboard Siswa</h2>", unsafe_allow_html=True)
    
    page = st.selectbox(
        "Pilih Menu",
        ["🏠 Beranda", "➕ Tambah Data", "📋 Lihat Data", "👥 Kelola Siswa", "🏆 Ranking"]
    )
    
    st.divider()
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    with st.expander("ℹ️ Informasi"):
        st.write("**Versi:** 3.0 Dark Mode")
        st.write("**Data:** Real-time Google Sheets")
        st.write("**Update:** Auto-refresh 5 menit")

# -------------------------------------------------------
# 🏠 HALAMAN BERANDA
# -------------------------------------------------------
if page == "🏠 Beranda":
    st.markdown(f"""
    <div class='main-header'>
        <h1>🏠 Selamat Datang di Dashboard</h1>
        <p>Kelola pelanggaran dan prestasi siswa secara real-time • Update terakhir: {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='icon'>👥</div>
            <div class='label'>Total Siswa</div>
            <div class='value'>{len(df_siswa)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pelanggaran_count = len(df_rekap[df_rekap.get('Poin Pelanggaran', 0) > 0]) if not df_rekap.empty else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='icon'>⚠️</div>
            <div class='label'>Pelanggaran</div>
            <div class='value'>{pelanggaran_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        prestasi_count = len(df_rekap[df_rekap.get('Poin Prestasi', 0) > 0]) if not df_rekap.empty else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='icon'>⭐</div>
            <div class='label'>Prestasi</div>
            <div class='value'>{prestasi_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Safe mean calculation dengan konversi numerik
        if not df_rekap.empty and 'Poin Pelanggaran' in df_rekap.columns and 'Poin Prestasi' in df_rekap.columns:
            df_temp = df_rekap.copy()
            df_temp['Poin Pelanggaran'] = pd.to_numeric(df_temp['Poin Pelanggaran'], errors='coerce').fillna(0)
            df_temp['Poin Prestasi'] = pd.to_numeric(df_temp['Poin Prestasi'], errors='coerce').fillna(0)
            summary_temp = df_temp.groupby('Nama Siswa').agg({
                'Poin Prestasi': 'sum',
                'Poin Pelanggaran': 'sum'
            })
            summary_temp['Total'] = summary_temp['Poin Prestasi'] - summary_temp['Poin Pelanggaran']
            avg_poin = summary_temp['Total'].mean() if len(summary_temp) > 0 else 0
        else:
            avg_poin = 0
            
        st.markdown(f"""
        <div class='stat-box'>
            <div class='icon'>📊</div>
            <div class='label'>Rata-rata Poin</div>
            <div class='value'>{avg_poin:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chart
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if not df_rekap.empty and 'Kelas' in df_rekap.columns:
        st.subheader("📈 Distribusi Poin per Kelas")
        df_temp = df_rekap.copy()
        df_temp['Poin Pelanggaran'] = pd.to_numeric(df_temp['Poin Pelanggaran'], errors='coerce').fillna(0)
        df_temp['Poin Prestasi'] = pd.to_numeric(df_temp['Poin Prestasi'], errors='coerce').fillna(0)
        df_temp['Total'] = df_temp['Poin Prestasi'] - df_temp['Poin Pelanggaran']
        df_grouped = df_temp.groupby('Kelas')['Total'].sum().reset_index()
        df_grouped.columns = ['Kelas', 'Total Poin']
        fig = px.bar(
            df_grouped, x='Kelas', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Aktivitas Terbaru (5 Terakhir)")
    if not df_rekap.empty:
        recent = df_rekap[['Tanggal', 'Nama Siswa', 'pelanggaran', 'Poin Pelanggaran', 'Poin Prestasi']].tail(5)
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Total Poin Per Siswa
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👥 Total Poin Per Siswa (Akumulatif)")
    if not df_rekap.empty:
        df_rekap_numeric = df_rekap.copy()
        df_rekap_numeric['Poin Pelanggaran'] = pd.to_numeric(df_rekap_numeric['Poin Pelanggaran'], errors='coerce').fillna(0)
        df_rekap_numeric['Poin Prestasi'] = pd.to_numeric(df_rekap_numeric['Poin Prestasi'], errors='coerce').fillna(0)
        
        summary = df_rekap_numeric.groupby('Nama Siswa').agg({
            'Poin Pelanggaran': 'sum',
            'Poin Prestasi': 'sum'
        }).reset_index()
        summary['Total Poin'] = summary['Poin Prestasi'] - summary['Poin Pelanggaran']
        summary = summary.sort_values('Total Poin', ascending=False)
        
        st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data siswa")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ➕ HALAMAN TAMBAH DATA
# -------------------------------------------------------
elif page == "➕ Tambah Data":
    st.markdown("""
    <div class='main-header'>
        <h1>➕ Tambah Data Baru</h1>
        <p>Input pelanggaran atau prestasi siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_siswa.empty:
        st.warning("⚠️ Daftar siswa kosong. Tambahkan siswa terlebih dahulu.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        with st.form("form_tambah"):
            col1, col2 = st.columns(2)
            
            with col1:
                nama = st.selectbox("Nama Siswa", df_siswa["Nama"].tolist())
                # 🔧 FIX: Tangani kasus ketika tidak ada data
                if not df_siswa.empty and nama:
                    kelas_data = df_siswa[df_siswa["Nama"] == nama]["Kelas"]
                    kelas = kelas_data.values[0] if len(kelas_data) > 0 else ""
                else:
                    kelas = ""
                st.text_input("Kelas", value=kelas, disabled=True)
            
            with col2:
                pelanggaran = st.text_input("Jenis Pelanggaran / Prestasi")
                poin_pelanggaran = st.number_input("Poin Pelanggaran", min_value=0, value=0)
                poin_prestasi = st.number_input("Poin Prestasi", min_value=0, value=0)
            
            # Hitung total poin saat ini siswa
            if not df_rekap.empty and nama:
                df_siswa_rekap = df_rekap[df_rekap['Nama Siswa'] == nama]
                total_poin_sebelum = (
                    pd.to_numeric(df_siswa_rekap['Poin Prestasi'], errors='coerce').sum() - 
                    pd.to_numeric(df_siswa_rekap['Poin Pelanggaran'], errors='coerce').sum()
                )
            else:
                total_poin_sebelum = 0
            
            poin_baru = poin_prestasi - poin_pelanggaran
            total_poin_sesudah = total_poin_sebelum + poin_baru
            
            st.info(f"📊 **Poin Sebelum:** {total_poin_sebelum:+.0f} → **Poin Input:** {poin_baru:+d} → **Total Poin Setelah:** {total_poin_sesudah:+.0f}")
            
            submit = st.form_submit_button("✅ Simpan Data", use_container_width=True)
            
            if submit and pelanggaran.strip():
                try:
                    # Refresh client untuk operasi tulis
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_rekap_write = spreadsheet.worksheet("rekap_pelanggaran")
                    
                    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Simpan dengan kolom Poin Kumulatif
                    ws_rekap_write.append_row([
                        tanggal, nama, kelas, pelanggaran,
                        poin_pelanggaran, poin_prestasi, poin_baru, total_poin_sesudah
                    ])
                    st.success(f"✅ Data berhasil disimpan untuk {nama}! Total poin sekarang: {total_poin_sesudah:+.0f}")
                    st.balloons()
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal menyimpan: {e}")
            elif submit:
                st.warning("⚠️ Lengkapi semua field!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 📋 HALAMAN LIHAT DATA
# -------------------------------------------------------
elif page == "📋 Lihat Data":
    st.markdown("""
    <div class='main-header'>
        <h1>📋 Data Rekap</h1>
        <p>Lihat, filter, dan export data</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📜 Riwayat Transaksi", "📊 Total Poin Per Siswa"])
    
    with tab1:
        st.markdown("### 📜 Semua Riwayat Transaksi")
        if df_rekap.empty:
            st.info("📭 Belum ada data")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search = st.text_input("🔍 Cari nama atau deskripsi", "")
            
            with col2:
                kelas_filter = st.selectbox("Filter Kelas", ["Semua"] + sorted(df_rekap['Kelas'].unique().tolist()))
            
            with col3:
                st.write("")
                st.write("")
                if st.button("🔄 Terapkan Filter", use_container_width=True):
                    st.rerun()
            
            df_filtered = df_rekap.copy()
            
            if search:
                df_filtered = df_filtered[
                    df_filtered['Nama Siswa'].str.contains(search, case=False, na=False) |
                    df_filtered['pelanggaran'].str.contains(search, case=False, na=False)
                ]
            
            if kelas_filter != "Semua":
                df_filtered = df_filtered[df_filtered['Kelas'] == kelas_filter]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                "📥 Export CSV",
                csv,
                f"rekap_transaksi_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            st.caption(f"Menampilkan {len(df_filtered)} dari {len(df_rekap)} transaksi")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Total Poin Akumulatif Per Siswa")
        if df_rekap.empty:
            st.info("📭 Belum ada data")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # Hitung total per siswa
            df_rekap_numeric = df_rekap.copy()
            df_rekap_numeric['Poin Pelanggaran'] = pd.to_numeric(df_rekap_numeric['Poin Pelanggaran'], errors='coerce').fillna(0)
            df_rekap_numeric['Poin Prestasi'] = pd.to_numeric(df_rekap_numeric['Poin Prestasi'], errors='coerce').fillna(0)
            
            summary = df_rekap_numeric.groupby(['Nama Siswa', 'Kelas']).agg({
                'Poin Pelanggaran': 'sum',
                'Poin Prestasi': 'sum'
            }).reset_index()
            summary['Total Poin'] = summary['Poin Prestasi'] - summary['Poin Pelanggaran']
            summary = summary.sort_values('Total Poin', ascending=False)
            
            # Filter
            search_siswa = st.text_input("🔍 Cari nama siswa", "", key="search_summary")
            if search_siswa:
                summary = summary[summary['Nama Siswa'].str.contains(search_siswa, case=False, na=False)]
            
            st.dataframe(summary, use_container_width=True, hide_index=True)
            
            csv_summary = summary.to_csv(index=False)
            st.download_button(
                "📥 Export Summary CSV",
                csv_summary,
                f"summary_poin_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            st.caption(f"Menampilkan {len(summary)} siswa")
            st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 👥 HALAMAN KELOLA SISWA
# -------------------------------------------------------
elif page == "👥 Kelola Siswa":
    st.markdown("""
    <div class='main-header'>
        <h1>👥 Kelola Siswa</h1>
        <p>Manajemen data siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Daftar Siswa")
        
        search = st.text_input("🔍 Cari siswa", "")
        df_filtered = df_siswa.copy()
        
        if search:
            df_filtered = df_filtered[df_filtered['Nama'].str.contains(search, case=False, na=False)]
        
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        if not df_siswa.empty:
            per_kelas = df_siswa['Kelas'].value_counts().to_dict()
            st.caption(f"📊 Distribusi: {per_kelas}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("➕ Tambah Siswa")
        
        with st.form("form_siswa"):
            new_nama = st.text_input("Nama Lengkap")
            new_kelas = st.text_input("Kelas")
            new_nis = st.text_input("NIS")
            
            submit = st.form_submit_button("✅ Simpan", use_container_width=True)
            
            if submit and all([new_nama.strip(), new_kelas.strip(), new_nis.strip()]):
                try:
                    # Refresh client untuk operasi tulis
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_siswa_write = spreadsheet.worksheet("data_siswa")
                    
                    ws_siswa_write.append_row([new_nama, new_kelas, new_nis])
                    st.success(f"✅ {new_nama} berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal: {e}")
            elif submit:
                st.warning("⚠️ Lengkapi semua field!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 🏆 HALAMAN RANKING
# -------------------------------------------------------
elif page == "🏆 Ranking":
    st.markdown("""
    <div class='main-header'>
        <h1>🏆 Ranking Siswa</h1>
        <p>Leaderboard berdasarkan total poin</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_rekap.empty:
        st.warning("📭 Belum ada data untuk ranking")
    else:
        # Konversi Total Poin ke numerik sebelum groupby
        df_rekap_numeric = df_rekap.copy()
        df_rekap_numeric['Poin Pelanggaran'] = pd.to_numeric(df_rekap_numeric['Poin Pelanggaran'], errors='coerce').fillna(0)
        df_rekap_numeric['Poin Prestasi'] = pd.to_numeric(df_rekap_numeric['Poin Prestasi'], errors='coerce').fillna(0)
        
        ranking = df_rekap_numeric.groupby('Nama Siswa').agg({
            'Poin Prestasi': 'sum',
            'Poin Pelanggaran': 'sum'
        }).reset_index()
        ranking['Total Poin'] = ranking['Poin Prestasi'] - ranking['Poin Pelanggaran']
        ranking = ranking.sort_values('Total Poin', ascending=False).reset_index(drop=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🥇 Top 3 Performer")
        
        medals = ["🥇", "🥈", "🥉"]
        colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        
        for idx, row in ranking.head(3).iterrows():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {colors[idx]}, rgba(255,255,255,0.1)); 
                        padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border: 1px solid {colors[idx]};'>
                <h3 style='margin:0; color: white;'>{medals[idx]} {row['Nama Siswa']}</h3>
                <p style='margin:0.3rem 0 0 0; color: white; opacity: 0.9;'>
                    Total Poin: <strong>{row['Total Poin']:.0f}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Ranking Lengkap")
        st.dataframe(ranking, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        fig = px.bar(
            ranking.head(10), x='Nama Siswa', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='RdYlGn',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e5e7eb',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🥇 Siswa Terbaik", ranking.iloc[0]['Nama Siswa'])
        with col2:
            st.metric("📈 Poin Tertinggi", f"{ranking.iloc[0]['Total Poin']:.0f}")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.divider()
st.markdown(
    f"<div style='text-align: center; color: var(--text-secondary); padding: 1rem;'>"
    f"💻 Dashboard Siswa v3.0 Dark Mode | "
    f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
    f"© 2024"
    f"</div>",
    unsafe_allow_html=True
)
