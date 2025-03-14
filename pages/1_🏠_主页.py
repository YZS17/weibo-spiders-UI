import streamlit as st
import pandas as pd
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="微博数据分析",
    page_icon="🏠",
    layout="wide"
)

# 页面标题
st.title("🏠 微博数据分析")

# 数据加载功能
def get_all_keywords():
    """获取所有关键词"""
    data_dir = Path("结果文件")  # 假设数据存放在 data 目录下
    return [folder.name for folder in data_dir.iterdir() if folder.is_dir()]

def get_csv_files(keyword):
    """获取指定关键词下的所有 CSV 文件"""
    data_dir = Path("结果文件") / keyword
    return [file for file in data_dir.glob("*.csv")]

def load_data(csv_file):
    """加载 CSV 文件"""
    try:
        df = pd.read_csv(csv_file)
        # 转换时间字段
        df['发布时间'] = pd.to_datetime(df['发布时间'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return pd.DataFrame()

# 侧边栏控制
with st.sidebar:
    st.header("数据选择")
    keyword = st.selectbox("选择关键词", get_all_keywords())
    csv_file = st.selectbox("选择数据文件", get_csv_files(keyword))
    
    st.header("过滤选项")
    min_reposts = st.slider("最小转发数", 0, 400, 0)
    date_range = st.date_input("日期范围", [])  # 默认返回空列表

# 加载数据
df = load_data(csv_file)
# print(df)

# 应用过滤
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    # 如果用户选择了日期范围
    filtered_df = df[
        (df['转发数'] >= min_reposts) &
        (df['发布时间'].dt.date >= date_range[0]) &
        (df['发布时间'].dt.date <= date_range[1])
    ]
elif date_range:  # 如果用户只选择了一个日期
    filtered_df = df[
        (df['转发数'] >= min_reposts) &
        (df['发布时间'].dt.date == date_range)
    ]
else:  # 如果用户没有选择日期
    filtered_df = df[df['转发数'] >= min_reposts]  # 仅应用转发数过滤

# 显示统计卡片
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总微博数", len(filtered_df))
with col2:
    st.metric("总评论数", filtered_df['评论内容'].count())
with col3:
    # 检查点赞数列是否为数值类型
    if pd.api.types.is_numeric_dtype(filtered_df['点赞数']):
        # 计算均值并处理 NaN
        avg_likes = filtered_df['点赞数'].mean()
        if pd.notna(avg_likes):  # 如果均值不是 NaN
            st.metric("平均点赞", round(avg_likes, 1))  # 使用 round() 函数
        else:
            st.metric("平均点赞", "无数据")
    else:
        st.metric("平均点赞", "数据格式错误")

# 数据表格
with st.expander("📊 查看原始数据"):
    st.dataframe(
        filtered_df,
        column_config={
            "微博图片url": st.column_config.ImageColumn(),
            "用户认证": st.column_config.CheckboxColumn()
        },
        use_container_width=True
    )

# 时间序列图
st.subheader("发布趋势")
time_df = filtered_df.set_index('发布时间').resample('D').size()
st.area_chart(time_df)