import streamlit as st

st.title("📖 关于")
st.markdown("""
### 微博数据看板
这是一个用于分析微博数据的工具，支持以下功能：
- 浏览单篇微博及其评论
- 对比多篇微博数据
- 自定义主题设置
- 更多功能正在开发中...
""")

if st.button("返回主页"):
    st.switch_page("pages/1_🏠_主页.py")