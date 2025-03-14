import streamlit as st
import pandas as pd
from utils.data_loader import get_all_keywords, get_csv_files, load_data

# 对比指标函数
def compare_metrics(df1, df2, label1, label2):
    col1, col2 = st.columns(2)
    metrics = ['转发数', '评论数', '点赞数']
    
    with col1:
        st.subheader(label1)
        for metric in metrics:
            avg = df1[metric].mean().round(1)
            st.metric(f"平均{metric}", avg)
    
    with col2:
        st.subheader(label2)
        for metric in metrics:
            avg = df2[metric].mean().round(1)
            st.metric(f"平均{metric}", avg, delta=avg - df1[metric].mean().round(1))

# 对比分析页
def show():
    st.title("📈 对比分析")
    
    # 选择关键词和文件
    col1, col2 = st.columns(2)
    with col1:
        kw1 = st.selectbox("选择关键词1", get_all_keywords())
        file1 = st.selectbox("选择文件1", get_csv_files(kw1))
        
    with col2:
        kw2 = st.selectbox("选择关键词2", get_all_keywords(), index=1)
        file2 = st.selectbox("选择文件2", get_csv_files(kw2))
    
    # 加载数据
    df1 = load_data(file1)
    df2 = load_data(file2)
    
    # 对比指标
    compare_metrics(df1, df2, file1.stem, file2.stem)
    
    # 对比可视化
    st.subheader("互动量分布对比")
    chart_data = pd.concat([
        df1[['转发数', '评论数', '点赞数']].mean().rename(file1.stem),
        df2[['转发数', '评论数', '点赞数']].mean().rename(file2.stem)
    ], axis=1)
    st.bar_chart(chart_data)

# 运行页面
show()