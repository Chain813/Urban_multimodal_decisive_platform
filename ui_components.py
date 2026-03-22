import streamlit as st


def render_top_nav():
    st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important;}

    a[data-testid="stPageLink-NavLink"] {
        background-color: rgba(255, 255, 255, 0.1) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important; padding: 0.6rem 1rem !important; display: flex !important; justify-content: center !important;
        text-decoration: none !important; transition: all 0.3s ease !important;
    }
    a[data-testid="stPageLink-NavLink"]:hover {
        background-color: rgba(255, 255, 255, 0.25) !important; border-color: rgba(255, 255, 255, 0.5) !important; transform: translateY(-2px);
    }
    a[data-testid="stPageLink-NavLink"] p, a[data-testid="stPageLink-NavLink"] span {
        font-size: 18px !important; font-weight: 600 !important; color: #f8fafc !important; margin: 0 !important;
    }

    .stApp { background-color: #0f172a; }
    h1, h2, h3, h4, h5, label, .stMarkdown p { color: #f8fafc !important; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155 !important; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    div[data-baseweb="select"] > div, textarea, input, section[data-testid="stFileUploader"] {
        background-color: #1e293b !important; color: #f8fafc !important; border: 1px solid #475569 !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #f8fafc !important; }
    [data-testid="stDeckGlJsonChart"] { height: 75vh !important; min-height: 650px !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
    with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
    with col3: st.page_link("pages/2_AIGC风貌管控.py", label="🎨 AIGC风貌管控", use_container_width=True)  # 🚨 空格已拔除
    with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
    with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
    with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
    with col7: st.page_link("pages/6_数据总览.py", label="📋 数据总览", use_container_width=True)
    st.markdown("---")

