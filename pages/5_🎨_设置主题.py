import streamlit as st

# 页面配置
st.set_page_config(
    page_title="显示设置",
    page_icon="⚙️",
    layout="centered"
)

# 应用主题的函数
def apply_theme(theme):
    css = f"""
    <style>
    .stApp {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    .stButton>button {{
        background-color: {theme['primary']};
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 页面标题
st.title("⚙️ 显示设置")

# 主题选择器
theme = st.selectbox("选择主题", [
    {"name": "浅色", "bg": "#ffffff", "text": "#000000", "primary": "#4a86e8"},
    {"name": "深色", "bg": "#2d3436", "text": "#dfe6e9", "primary": "#0984e3"},
    {"name": "专业蓝", "bg": "#f0f5f9", "text": "#2d3436", "primary": "#2d3436"}
], format_func=lambda x: x["name"])

# 应用主题按钮
if st.button("应用主题"):
    apply_theme(theme)
    st.success("主题已更新！")

# 布局设置
st.subheader("布局选项")
grid_view = st.toggle("网格视图", True)
st.session_state['grid_view'] = grid_view