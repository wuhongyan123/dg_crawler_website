# encoding: utf-8

# 存储news与html的数据库配置列表
WEBSITE_CONFIG_LIST = {
    '00': {# 此为公用测试数据库（校园网内可使用），可以换成自己的.
        'host': '192.168.235.31',
        'port': 3306,
        'user': 'dg',
        'password': 'dg',
        'db': 'dg_db_website'
    },
    '01': {  # 本地测试数据库,自己搭建
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': ''
    }
}

COMMON_WEBSITE_CONFIG = {
    'host': '192.168.235.31',
    'port': 3306,
    'user': 'dg',
    'password': 'dg',
    'db': 'common_website'
}

