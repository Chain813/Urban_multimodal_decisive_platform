import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 呼叫你的公共导航栏
from ui_components import render_top_nav

st.set_page_config(page_title="数据总览", layout="wide", initial_sidebar_state="expanded")

# 引入头部导航和 CSS
render_top_nav()

# 补充本页专属的卡片交互 CSS
st.markdown("""
    <style>
    .data-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .data-card:hover { background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>多源数据资产总览与完整性评估</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 📊 数据筛选")
    filter_type = st.radio("数据状态", ["全部", "✅ 已有数据", "⚠️ 部分缺失", "❌ 待采集"], label_visibility="collapsed")

st.markdown("### 📈 数据资产概览")


# ==========================================
# 🚨 核心修复 3：文件雷达动态侦测函数！
# ==========================================
def check_status(file_path):
    # 如果明确标记为待采集，就是 missing
    if file_path in ["待采集", "待生成"]:
        return "missing"
    # 如果文件或文件夹在硬盘里真实存在，返回 complete，否则判定为 partial (缺失)
    return "complete" if os.path.exists(file_path) else "partial"


# 通过 check_status() 动态加载文件状态！系统活过来了！
data_categories = {
    "物理空间数据": {
        "streetview": {"name": "街景图片", "status": check_status("StreetViews/"), "file": "StreetViews/",
                       "count": "300+ 采样点", "description": "百度街景全景图片，覆盖伪满皇宫周边核心区"},
        "poi": {"name": "POI 数据", "status": check_status("Changchun_POI_Real.csv"), "file": "Changchun_POI_Real.csv",
                "count": "CSV 文件", "description": "兴趣点数据，包含商业、交通等设施"},
        "traffic": {"name": "交通设施", "status": check_status("Changchun_Traffic_Real.csv"),
                    "file": "Changchun_Traffic_Real.csv", "count": "CSV 文件", "description": "公共交通站点、停车场等"},
        "points": {"name": "精确点位", "status": check_status("Changchun_Precise_Points.xlsx"),
                   "file": "Changchun_Precise_Points.xlsx", "count": "Excel 文件",
                   "description": "精确地理坐标采样点位"}
    },
    "视觉感知数据": {
        "gvi": {"name": "绿视率分析", "status": check_status("GVI_Results_Analysis.csv"),
                "file": "GVI_Results_Analysis.csv", "count": "CSV 文件", "description": "基于 DeepLabV3+ 的指标测度"},
        "cv_nlp": {"name": "CV+NLP 数据", "status": check_status("CV_NLP_RawData.csv"), "file": "CV_NLP_RawData.csv",
                   "count": "CSV 文件", "description": "视觉与情感融合分析数据"}
    },
    "社会情感数据": {
        "weibo": {"name": "微博数据", "status": check_status("待采集"), "file": "待采集", "count": "-",
                  "description": "公众讨论文本"},
        "dianping": {"name": "大众点评", "status": check_status("待采集"), "file": "待采集", "count": "-",
                     "description": "商户评论与打卡数据"}
    }
}

total_complete = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "complete")
total_partial = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "partial")
total_missing = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "missing")

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ 已有数据", f"{total_complete} 项")
col2.metric("⚠️ 缺失数据", f"{total_partial} 项")
col3.metric("❌ 待采集", f"{total_missing} 项")
col4.metric("📊 数据完整率", f"{total_complete / (total_complete + total_partial + total_missing) * 100:.1f}%")

st.markdown("---")

for category, items in data_categories.items():
    filtered_items = {k: v for k, v in items.items() if filter_type == "全部" or
                      (filter_type == "✅ 已有数据" and v["status"] == "complete") or
                      (filter_type == "⚠️ 部分缺失" and v["status"] == "partial") or
                      (filter_type == "❌ 待采集" and v["status"] == "missing")}

    if filtered_items:
        st.markdown(f"#### {category}")
        cols = st.columns(len(filtered_items))
        for idx, (key, item) in enumerate(filtered_items.items()):
            with cols[idx]:
                st.markdown(f'<div class="data-card">', unsafe_allow_html=True)
                st.markdown(f"#### {item['name']}")

                status_icon = "✅ 在线" if item["status"] == "complete" else "⚠️ 离线/丢失" if item[
                                                                                                  "status"] == "partial" else "❌ 计划中"
                st.info(f"**状态:** {status_icon}\n\n**雷达寻址:** `{item['file']}`\n\n**规模:** {item['count']}")
                st.markdown(f"*{item['description']}*")
                st.markdown('</div>', unsafe_allow_html=True)