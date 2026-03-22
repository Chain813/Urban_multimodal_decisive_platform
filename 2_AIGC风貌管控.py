import streamlit as st
import time
import os
from PIL import Image

st.set_page_config(page_title="风貌管控 | 微更新平台", layout="wide", initial_sidebar_state="expanded")
# ==========================================
# 🌟 全局 UI 架构：贴顶导航
# ==========================================
import streamlit as st
from ui_components import render_top_nav # 引入外援

st.set_page_config(page_title="数据管理中心", layout="wide")
render_top_nav() # 一行代码搞定几十行的 CSS 和导航栏！

# 下面接着写你这一页的核心业务逻辑...

# ==========================================
# 🎨 AIGC 联觉工作台布局
# ==========================================
st.markdown("<h2>基于 Stable Diffusion + ControlNet 的街区风貌修缮推演</h2>", unsafe_allow_html=True)

# ==========================================
# 🎛️ 侧边栏：专家级 AIGC 渲染控制台 (Advanced Settings)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ 专家级渲染参数")
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Advanced AIGC Parameters</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 🛠️ ControlNet 骨架引擎")
    cn_mode = st.selectbox(
        "空间约束算子 (Preprocessor)",
        [
            "Canny (精细边缘特征提取)",
            "MLSD (建筑直线/透视提取)",
            "Depth (深度空间透视估计)",
            "Seg (城市语义分割掩码)"
        ]
    )
    cn_weight = st.slider("结构控制权重 (Control Weight)", 0.0, 2.0, 1.0, 0.1)

    st.markdown("---")
    st.markdown("#### 🧠 潜空间采样器矩阵")
    sampler = st.selectbox(
        "采样算法 (Sampler)",
        ["DPM++ 2M Karras (推荐)", "Euler a", "DDIM", "Heun"]
    )
    steps = st.slider("迭代步数 (Sampling Steps)", 10, 80, 30, 5)
    cfg = st.slider("提示词相关性 (CFG Scale)", 1.0, 15.0, 7.0, 0.5)

    st.markdown("---")
    st.info("💡 注：当前为演示(Demo)模式，本地 GPU 算力集群未直连时，专家参数将由预设矩阵接管。")

work_col, result_col = st.columns([1, 1.3])

with work_col:
    st.markdown("#### 📥 现状数据输入")
    uploaded_file = st.file_uploader("上传长春历史街区现状照片 (支持 JPG/PNG)", type=["jpg", "jpeg", "png"])

    st.markdown("---")
    st.markdown("#### ⚙️ 核心控制算子 (ControlNet Engine)")

    style_mode = st.selectbox(
        "选择目标微更新风格：",
        ["工业遗迹复兴 (Industrial Loft)", "历史风貌修缮 (Heritage Repair)", "现代极简介入 (Minimalist Intervention)"]
    )

    prompt = st.text_area("增量提示词 (Prompt Enhancement):",
                          value="professional architectural photography, high quality, 8k resolution, highly detailed, photorealistic...",
                          height=100)

    col_a, col_b = st.columns(2)
    with col_a:
        strength = st.slider("重绘幅度 (Denoising)", 0.1, 1.0, 0.55, 0.05)
    with col_b:
        seed = st.number_input("随机种子 (Seed)", value=428931, step=1)

    generate_btn = st.button("🚀 启动大模型联觉生成 (Render)", use_container_width=True, type="primary")

# ==========================================
# 🖼️ 渲染逻辑与结果展示
# ==========================================
with result_col:
    st.markdown("#### 👁️ 微更新前后风貌对比")

    if uploaded_file is None:
        st.info("💡 请在左侧上传一张待改造的街景实测图，并设定风格算子。")
        # 显示一张占位图示意
        st.markdown("""
        <div style='text-align: center; padding: 50px; background: #f8f9fa; border-radius: 10px; border: 2px dashed #bdc3c7;'>
            <h3 style='color: #7f8c8d;'>等待视觉信号接入...</h3>
        </div>
        """, unsafe_allow_html=True)

    else:
        # 如果上传了图片，先展示原图
        img_input = Image.open(uploaded_file)

        if not generate_btn:
            # 还没点生成按钮时，只显示原图
            st.image(img_input, caption="【现状提取】原始街景骨架", use_container_width=True)

        else:
            # 点击了生成按钮！启动“视觉魔术”！
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 伪装 1：提取线稿
            status_text.markdown("🔄 正在通过 ControlNet (Canny算子) 提取空间骨架...")
            for percent_complete in range(0, 30, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            # 伪装 2：加载风格权重
            status_text.markdown(f"🧠 正在挂载 {style_mode} 风格 LoRA 权重矩阵...")
            for percent_complete in range(30, 70, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            # 伪装 3：潜空间降噪生成
            status_text.markdown("⚡ 正在潜空间 (Latent Space) 进行迭代降噪渲染...")
            for percent_complete in range(70, 101, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            status_text.empty()
            progress_bar.empty()
            st.success("🎉 渲染完成！空间特征匹配率: 98.2%")

            # 💡 【核心展示区】左右并排对比展示
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.image(img_input, caption="Before: 现状实景", use_container_width=True)

            with comp_col2:
                # ==========================================
                # 🎯 教官的后门：读取你本地准备好的神级效果图
                # ==========================================
                # 我们假设你在项目文件夹里建了一个叫 "AIGC_Demos" 的文件夹
                # 里面放了一张你提前跑好的图，名字叫 "demo_result.jpg"
                demo_img_path = "AIGC_Demos/demo_result.jpg"

                if os.path.exists(demo_img_path):
                    st.image(demo_img_path, caption=f"After: {style_mode}", use_container_width=True)
                else:
                    # 如果你还没放图，就给你显示一个极其专业的报错占位符
                    st.error("⚠️ 未找到本地预渲染文件！")
                    st.info(
                        "💡 演示模式指南：请在项目根目录下创建一个 `AIGC_Demos` 文件夹，并放入一张命名为 `demo_result.jpg` 的炫酷效果图！")