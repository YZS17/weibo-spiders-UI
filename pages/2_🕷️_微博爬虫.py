import streamlit as st
import os
import subprocess

# 动态获取 settings.py 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
SETTINGS_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'weibo', 'settings.py'))

# 读取当前设置
def read_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# 写入新的设置
def write_settings(new_settings):
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_settings)

# 页面标题
st.title("🕷️ 微博爬虫控制面板")

# 使用表单让用户输入参数
with st.form("settings_form"):
    # 关键词列表
    st.markdown("### 🔍 关键词列表")
    keyword_list = st.text_input("输入关键词列表，多个关键词用换行分隔", value="迪丽热巴")

    # 微博类型
    st.markdown("### 📰 微博类型")
    weibo_type = st.selectbox(
        "选择微博类型",
        options=[0, 1, 2, 3, 4, 5, 6],
        index=2,  # 默认选择热门微博
        format_func=lambda x: [
            "全部微博", "全部原创微博", "热门微博", "关注人微博", "认证用户微博", "媒体微博", "观点微博"
        ][x],
    )

    # 包含类型
    st.markdown("### 📂 筛选结果微博中必需包含的内容")
    contain_type = st.selectbox(
        "选择包含类型",
        options=[0, 1, 2, 3, 4],
        index=0,  # 默认不筛选
        format_func=lambda x: [
            "不筛选", "包含图片", "包含视频", "包含音乐", "包含短链接"
        ][x],
    )

    # 地区筛选
    st.markdown("### 🌍 筛选微博的发布地区")
    region = st.text_input("输入地区，多个地区用逗号分隔", value="全部")

    # 起始日期
    st.markdown("### 📅 搜索的起始日期")
    start_date = st.text_input("输入起始日期（yyyy-mm-dd）", value="2024-03-01")

    # 终止日期
    st.markdown("### 📅 搜索的终止日期")
    end_date = st.text_input("输入终止日期（yyyy-mm-dd）", value="2024-03-03")

    # 细分搜索阈值
    st.markdown("### 📏 细分搜索阈值")
    further_threshold = st.number_input(
        "输入细分搜索阈值（建议 40-50）", value=40, min_value=1, max_value=100
    )

    # 提交按钮
    if st.form_submit_button("💾 保存设置"):
        # 构建新的设置内容
        new_settings = f"""# -*- coding: utf-8 -*-

BOT_NAME = 'weibo'
SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {{
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'SCF=AlUCPW2egbSqfc_oOtNAd87ORjEQXckbLwbJYBy_CBbg6cuxbahqa5_Z-9aD2uipDYTxo03R50RFFTd74Tdon6I.; SUB=_2A25K1dzwDeRhGeNH7FIU9y3Lyj6IHXVpq1A4rDV6PUJbktAbLU7GkW1NSoTtPzDTd4kx95UGwQab5WHr_BqvIU3w; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uMC5nq6ZZ29dvGpU5BI485JpX5KMhUgL.Fo-4S05fS0eNeKz2dJLoI0zLxKnLBK5LB.qLxK.LB-BL1K2LxK.LBoML12eLxK.LBK-L1K-LxKMLBo2LBo541K50S7tt; SSOLoginState=1741794465; ALF=1744386465; _T_WM=0160266cb23f7d1470f844f9bf597dd3; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4784937075214225%26luicode%3D20000061%26lfid%3D4784937075214225; WEIBOCN_FROM=1110106030'
}}
ITEM_PIPELINES = {{
    'weibo.pipelines.DuplicatesPipeline': 300,
    'weibo.pipelines.CsvPipeline': 301,
    # 'weibo.pipelines.MysqlPipeline': 302,
    # 'weibo.pipelines.MongoPipeline': 303,
    'weibo.pipelines.MyImagesPipeline': 304,
    'weibo.pipelines.MyVideoPipeline': 305
}}
KEYWORD_LIST = {repr(keyword_list.splitlines())}  # 或者 KEYWORD_LIST = 'keyword_list.txt'
WEIBO_TYPE = {weibo_type}
CONTAIN_TYPE = {contain_type}
REGION = {repr([r.strip() for r in region.split(",")])}
START_DATE = '{start_date}'
END_DATE = '{end_date}'
FURTHER_THRESHOLD = {further_threshold}
IMAGES_STORE = './'
FILES_STORE = './'
"""
        # 写入新的设置
        write_settings(new_settings)
        st.success("✅ 设置已保存！")
        st.rerun()

# 运行爬虫按钮
if st.button("🚀 运行爬虫"):
    os.system("scrapy crawl search")
    st.success("✅ 爬虫已启动！")