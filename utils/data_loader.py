import pandas as pd
from pathlib import Path
import streamlit as st

DATA_DIR = Path("结果文件")

@st.cache_data
def load_data(file_path):
    """加载并预处理CSV数据"""
    try:
        df = pd.read_csv(file_path)
        
        # 处理时间字段
        df['发布时间'] = pd.to_datetime(df['发布时间'], errors='coerce')
        df['评论时间'] = pd.to_datetime(df['评论时间'], errors='coerce')
        
        # 处理图片URL
        df['图片列表'] = df['微博图片url'].apply(
            lambda x: x.split(',') if pd.notna(x) else [])
            
        return df.dropna(subset=['id'])
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return pd.DataFrame()

def get_all_keywords():
    """获取所有关键词分类"""
    return [p.name for p in DATA_DIR.iterdir() if p.is_dir()]

def get_csv_files(keyword):
    """获取指定关键词分类下的CSV文件"""
    keyword_dir = DATA_DIR / keyword
    return list(keyword_dir.glob("*.csv"))