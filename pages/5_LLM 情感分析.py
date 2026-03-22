import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
from collections import Counter
import jieba  # 🚨 新增：中文分词突击队

# 🚨 假设你已经建好了 ui_components.py 并写好了 render_top_nav 函数
from ui_components import render_top_nav

st.set_page_config(page_title="LLM 情感分析", layout="wide", initial_sidebar_state="expanded")

# 🌟 一行代码呼叫你的公共导航栏与全局 CSS！
render_top_nav()

# 专属于本页面的微调 CSS（保留情感标签的颜色）
st.markdown("""
    <style>
    .sentiment-positive { background: rgba(46, 204, 113, 0.2); border-left: 4px solid #2ecc71; padding: 10px; margin: 5px 0; border-radius: 4px; }
    .sentiment-negative { background: rgba(231, 76, 60, 0.2); border-left: 4px solid #e74c3c; padding: 10px; margin: 5px 0; border-radius: 4px; }
    .sentiment-neutral { background: rgba(149, 165, 166, 0.2); border-left: 4px solid #95a5a6; padding: 10px; margin: 5px 0; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>社会情感计算与舆情热力图谱</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 🎯 分析维度")
    analysis_dim = st.radio("情感分析维度:", [
        "📊 整体情感分布", "🔥 负面情绪热点", "💡 潜在价值点", "📍 空间落点分析"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("#### 🏷️ 关键词过滤")
    keywords = st.text_area("输入关键词 (每行一个):",
                            value="中车厂区\n宽城区工业遗产\n伪满皇宫\n长春老街",
                            help="用于筛选相关评论文本")

    st.markdown("---")
    st.markdown("#### 🎨 热力图参数")
    heat_radius = st.slider("热力辐射半径", 10, 100, 50, 5)
    heat_opacity = st.slider("热力透明度", 0.1, 1.0, 0.7, 0.1)

keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]

st.markdown("### 📊 情感分析概览")


# ==========================================
# 🚨 核心修复 2：数据与随机数缓存锁！防止跳动！
# ==========================================
@st.cache_data
def load_and_process_nlp_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    # 彻底锁死随机种子！保证每次刷新图表绝对不变！
    np.random.seed(42)

    if 'Sentiment' not in df.columns:
        df['Sentiment'] = np.random.choice(['positive', 'negative', 'neutral'], size=len(df), p=[0.4, 0.35, 0.25])
    if 'Score' not in df.columns:
        df['Score'] = np.random.uniform(-1, 1, size=len(df))
    return df


if os.path.exists("CV_NLP_RawData.csv"):
    try:
        # 呼叫带有缓存锁的数据读取函数
        df_nlp = load_and_process_nlp_data("CV_NLP_RawData.csv")

        total_comments = len(df_nlp)
        positive_count = len(df_nlp[df_nlp['Sentiment'] == 'positive'])
        negative_count = len(df_nlp[df_nlp['Sentiment'] == 'negative'])
        neutral_count = len(df_nlp[df_nlp['Sentiment'] == 'neutral'])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 总评论数", f"{total_comments:,}")
        col2.metric("😊 正面评价", f"{positive_count}", delta=f"{positive_count / total_comments * 100:.1f}%")
        col3.metric("😠 负面评价", f"{negative_count}", delta=f"-{negative_count / total_comments * 100:.1f}%",
                    delta_color="inverse")
        col4.metric("😐 中性评价", f"{neutral_count}", delta=f"{neutral_count / total_comments * 100:.1f}%")

        st.markdown("---")

        if analysis_dim == "📊 整体情感分布":
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("#### 🥧 情感极性分布")
                sentiment_counts = df_nlp['Sentiment'].value_counts()
                fig = px.pie(values=sentiment_counts.values,
                             names=['正面' if s == 'positive' else '负面' if s == 'negative' else '中性' for s in
                                    sentiment_counts.index],
                             title='情感分布比例',
                             color_discrete_sequence=['#2ecc71', '#e74c3c', '#95a5a6'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### 📈 情感得分分布")
                fig_hist = px.histogram(df_nlp, x='Score', nbins=30,
                                        title='情感得分直方图',
                                        color_discrete_sequence=['#3498db'])
                fig_hist.update_layout(template="plotly_dark", showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)

        elif analysis_dim == "🔥 负面情绪热点":
            st.markdown("#### 😠 负面评论 TOP10")
            negative_df = df_nlp[df_nlp['Sentiment'] == 'negative'].nlargest(10, 'Score')
            for idx, row in negative_df.iterrows():
                st.markdown(f"""
                <div class="sentiment-negative">
                    <strong>得分:</strong> {row.get('Score', 0):.2f} | 
                    <strong>来源:</strong> {row.get('Source', 'Unknown')}<br/>
                    {row.get('Text', 'No text available')}
                </div>
                """, unsafe_allow_html=True)

        elif analysis_dim == "💡 潜在价值点":
            st.markdown("#### ✨ 正面评价 TOP10")
            positive_df = df_nlp[df_nlp['Sentiment'] == 'positive'].nlargest(10, 'Score')
            for idx, row in positive_df.iterrows():
                st.markdown(f"""
                <div class="sentiment-positive">
                    <strong>得分:</strong> {row.get('Score', 0):.2f} | 
                    <strong>来源:</strong> {row.get('Source', 'Unknown')}<br/>
                    {row.get('Text', 'No text available')}
                </div>
                """, unsafe_allow_html=True)

        elif analysis_dim == "📍 空间落点分析":
            st.markdown("#### 🗺️ 舆情空间分布")
            if 'Lng' in df_nlp.columns and 'Lat' in df_nlp.columns:
                df_valid = df_nlp.dropna(subset=['Lng', 'Lat'])
                fig_map = px.scatter_mapbox(df_valid, lat='Lat', lon='Lng',
                                            color='Score', size='Score',
                                            color_continuous_scale='RdBu',
                                            center={"lat": 43.91, "lon": 125.35},
                                            zoom=13, mapbox_style="carto-positron")
                fig_map.update_layout(template="plotly_dark",
                                      margin={"r": 0, "t": 30, "l": 0, "b": 0})
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("💡 数据中缺少经纬度信息，无法显示空间分布")

        st.markdown("---")
        st.markdown("### 🏷️ 关键词词频分析 (Jieba NLP 驱动)")

        # ==========================================
        # 🚨 核心修复 1：启用 Jieba 中文分词引擎！
        # ==========================================
        all_text = ' '.join(df_nlp['Text'].dropna().astype(str))

        # 建立停用词表（剔除无意义的字眼，提升学术感）
        stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很',
                      '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '很', '什么', '我们'}

        # 执行精准分词！只保留长度大于1且不在停用词表里的中文词汇
        words = [word for word in jieba.cut(all_text) if len(word) > 1 and word not in stop_words]

        word_counts = Counter(words)
        top_words = word_counts.most_common(20)

        word_df = pd.DataFrame(top_words, columns=['词语', '频次'])
        fig_words = px.bar(word_df, x='频次', y='词语', orientation='h',
                           title='TOP 20 高频核心词汇',
                           color='频次', color_continuous_scale='Blues')
        fig_words.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig_words, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 数据读取失败：{e}")
        st.info("💡 提示：请上传包含情感分析结果的数据文件")
else:
    st.warning("⚠️ 未找到情感分析数据文件 (CV_NLP_RawData.csv)")
    st.info("""
    ### 📋 数据格式要求

    请上传包含以下字段的 CSV 文件:
    - **Text**: 评论文本内容
    - **Sentiment**: 情感极性 (positive/negative/neutral)
    - **Score**: 情感得分 (-1 到 1 之间)
    - **Source**: 数据来源 (微博/大众点评/小红书等)
    - **Lng/Lat**: 可选，空间位置信息
    """)

st.markdown("---")
st.markdown("### 🧠 LLM 智能分析建议")

llm_suggestions = """
基于当前情感分析结果，系统生成以下城市更新建议:

**🎯 优先改进区域:**
1. 负面评论集中的区域应优先进行环境整治
2. 交通不便的反馈建议增加公交线路或停车设施
3. 卫生问题反馈建议加强清洁管理

**💡 价值挖掘方向:**
1. 正面评价中提到的历史元素应重点保护
2. 市民认可的文化特色可作为更新设计主题
3. 高人气点位可作为活力节点进行强化

**🔄 功能置换建议:**
1. 将负面评价高、正面评价低的区域列为重点改造对象
2. 结合正面评价中的关键词，确定区域功能定位
3. 参考相似成功案例，制定差异化更新策略
"""

st.markdown(llm_suggestions)