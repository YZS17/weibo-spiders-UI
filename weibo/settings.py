# -*- coding: utf-8 -*-

BOT_NAME = 'weibo'
SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'SCF=AlUCPW2egbSqfc_oOtNAd87ORjEQXckbLwbJYBy_CBbg6cuxbahqa5_Z-9aD2uipDYTxo03R50RFFTd74Tdon6I.; SUB=_2A25K1dzwDeRhGeNH7FIU9y3Lyj6IHXVpq1A4rDV6PUJbktAbLU7GkW1NSoTtPzDTd4kx95UGwQab5WHr_BqvIU3w; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uMC5nq6ZZ29dvGpU5BI485JpX5KMhUgL.Fo-4S05fS0eNeKz2dJLoI0zLxKnLBK5LB.qLxK.LB-BL1K2LxK.LBoML12eLxK.LBK-L1K-LxKMLBo2LBo541K50S7tt; SSOLoginState=1741794465; ALF=1744386465; _T_WM=0160266cb23f7d1470f844f9bf597dd3; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4784937075214225%26luicode%3D20000061%26lfid%3D4784937075214225; WEIBOCN_FROM=1110106030'
}
ITEM_PIPELINES = {
    'weibo.pipelines.DuplicatesPipeline': 300,
    'weibo.pipelines.CsvPipeline': 301,
    # 'weibo.pipelines.MysqlPipeline': 302,
    # 'weibo.pipelines.MongoPipeline': 303,
    'weibo.pipelines.MyImagesPipeline': 304,
    'weibo.pipelines.MyVideoPipeline': 305
}
KEYWORD_LIST = ['迪丽热巴2']  # 或者 KEYWORD_LIST = 'keyword_list.txt'
WEIBO_TYPE = 2
CONTAIN_TYPE = 0
REGION = ['全部']
START_DATE = '2024-03-01'
END_DATE = '2024-03-03'
FURTHER_THRESHOLD = 40
IMAGES_STORE = './'
FILES_STORE = './'
