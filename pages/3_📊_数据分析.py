import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="微博数据看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("📊 微博数据看板")

# 数据文件目录
DATA_DIR = Path("结果文件")

# 颜色主题
theme = {
    "backgroundColor": "#F0F2F6",
    "secondaryBackgroundColor": "#FFFFFF",
    "textColor": "#262730",
    "font": "sans serif"
}

# 缓存数据加载函数
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # 转换时间字段（处理无效日期）
        df['发布时间'] = pd.to_datetime(df['发布时间'], errors='coerce')
        df['评论时间'] = pd.to_datetime(df['评论时间'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return pd.DataFrame()

# 文件选择侧边栏
def sidebar_controls():
    with st.sidebar:
        st.header("📁 数据分析选项")
        
        # 获取所有CSV文件
        csv_files = list(DATA_DIR.glob("**/*.csv"))
        
        # 文件选择器
        selected_file = st.selectbox(
            "选择数据文件",
            csv_files,
            format_func=lambda x: x.parent.name + "/" + x.name
        )
        
        # 时间范围设置
        st.divider()
        st.subheader("⏳ 时间过滤")
        use_time_filter = st.checkbox("启用时间过滤")
        
    return selected_file, use_time_filter

# 主页面布局
def main_page(file_path, use_time_filter):
    df = load_data(file_path)
    
    # 预处理数据：区分主微博和评论
    # 假设每条记录的评论部分有评论人ID、评论人昵称、评论时间、评论内容、点赞次数等字段
    main_weibo = df[['id', 'bid', 'user_id', '用户昵称', '微博正文', '头条文章url', '发布位置', '艾特用户', '话题', '转发数', '评论数', '点赞数', '发布时间', '发布工具', '微博图片url', '微博视频url', 'retweet_id', 'ip', 'user_authentication']].drop_duplicates(subset='id').copy()
    comments = df[['id', '评论人ID', '评论人昵称', '评论时间', '评论内容', '点赞次数']].copy()
    
    # 时间过滤逻辑
    if use_time_filter and not main_weibo.empty:
        valid_weibo = main_weibo[main_weibo['发布时间'].notna()]
        if not valid_weibo.empty:
            start_time = valid_weibo['发布时间'].min().to_pydatetime()
            end_time = valid_weibo['发布时间'].max().to_pydatetime()
            
            selected_range = st.slider(
                "选择时间范围",
                value=(start_time, end_time),
                min_value=start_time,
                max_value=end_time,
                format="YYYY-MM-DD"
            )
            main_weibo = valid_weibo[valid_weibo['发布时间'].between(*selected_range)]

    # 展示关键指标
    display_kpis(main_weibo)
    
    # 数据表和详情查看
    st.divider()
    st.subheader("📋 详细数据浏览")
    
    if not main_weibo.empty:
        # 创建文章选择器
        weibo_options = main_weibo['id'].tolist()
        selected_id = st.selectbox(
            "选择微博查看详情",
            weibo_options,
            format_func=lambda x: f"文章ID: {x} - {main_weibo.loc[main_weibo['id'] == x, '用户昵称'].values[0] if not main_weibo.loc[main_weibo['id'] == x, '用户昵称'].empty else '未知用户'}"
        )
        
        # 获取选中文章的详细信息
        selected_weibo = main_weibo[main_weibo['id'] == selected_id].iloc[0]
        
        # 获取相关评论
        related_comments = comments[comments['id'] == selected_id]
        
        # 展示详情
        display_weibo_detail(selected_weibo, related_comments)
    else:
        st.warning("没有可用的微博数据")
    # 展示完整数据表
    with st.expander("📊 查看完整数据表格"):
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "微博图片url": st.column_config.ImageColumn("图片预览"),
                "微博视频url": st.column_config.LinkColumn("视频链接")
            }
        )
# 展示关键指标
def display_kpis(df):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        count = df['id'].nunique()
        st.metric("总微博数", count if not pd.isna(count) else 0)
    
    with col2:
        avg_reposts = df['转发数'].mean(skipna=True)
        st.metric("平均转发数", f"{avg_reposts:.1f}" if not pd.isna(avg_reposts) else "-")
    
    with col3:
        avg_comments = df['评论数'].mean(skipna=True)
        st.metric("平均评论数", f"{avg_comments:.1f}" if not pd.isna(avg_comments) else "-")
    
    with col4:
        avg_likes = df['点赞数'].mean(skipna=True)
        st.metric("平均点赞数", f"{avg_likes:.1f}" if not pd.isna(avg_likes) else "-")

# 展示单条微博详情
def display_weibo_detail(weibo, comments):
    card = st.container(border=True)
    
    with card:
        col_img, col_text = st.columns([1, 3])
        
        # 图片显示
        with col_img:
            if pd.notna(weibo['微博图片url']):
                images = [img.strip() for img in str(weibo['微博图片url']).split(',') if img.strip()]
                if images:
                    st.image(images[0], use_column_width=True)
        
        # 文本信息
        with col_text:
            time_str = weibo['发布时间'].strftime('%Y-%m-%d %H:%M') if pd.notna(weibo['发布时间']) else "未知时间"
            st.markdown(f"""
            ​**📛 用户昵称**: {weibo.get('用户昵称', '匿名用户')}  
            ​**⏰ 发布时间**: {time_str}  
            ​**📱 发布工具**: {weibo.get('发布工具', '未知设备')}  
            ​**🔁 转发次数**: {weibo.get('转发数', 0)}  
            ​**💬 评论次数**: {weibo.get('评论数', 0)}  
            ​**👍 点赞次数**: {weibo.get('点赞数', 0)}
            """)
            
            st.divider()
            st.markdown(f"**📜 正文内容**:\n\n{weibo.get('微博正文', '')}")
            
            if pd.notna(weibo.get('头条文章url')):
                st.markdown(f"[📰 查看文章全文]({weibo['头条文章url']})")
        
        # 展示评论
        if not comments.empty:
            st.divider()
            st.subheader("💬 评论")
            for _, comment in comments.iterrows():
                comment_time = comment['评论时间'].strftime('%Y-%m-%d %H:%M') if pd.notna(comment['评论时间']) else "未知时间"
                with st.container(border=True):
                    st.markdown(f"""
                    ​**👤 评论人**: {comment['评论人昵称']}  
                    ​**⏰ 评论时间**: {comment_time}  
                    ​**💬 评论内容**: {comment['评论内容']}  
                    ​**👍 点赞次数**: {comment['点赞次数']}
                    """)
# 运行应用
if __name__ == "__main__":
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        st.warning("请将CSV数据文件放入「结果文件」目录")
        st.stop()
    
    selected_file, use_time_filter = sidebar_controls()
    main_page(selected_file, use_time_filter)