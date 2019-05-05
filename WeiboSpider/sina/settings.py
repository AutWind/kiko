# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'_T_WM=55367956451; ALF=1559198637; SCF=AuAzAyf0wbBySG6r63fQTrbh8pSWeGujRs0Zd_t5pF3WEmzswN9HKnWMys5C3R2JrCg_mvBld3F_Qni_sibc88o.; SUB=_2A25xzFkaDeRhGeBO6FoS8yzMyT-IHXVTT2dSrDV6PUJbktAKLVj7kW1NSh8AnXrHZTyyuiuthsGbIYx2_I6Ehap-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-H9lEKC-wF6sJkueADXUH5JpX5K-hUgL.Foq7e0n0e0z7eoe2dJLoI7HWdLv2Cntt; SUHB=05i65kvL88ngFW'
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'SinaData'
