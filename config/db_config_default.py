# encoding: utf-8

# 存储news与html的数据库配置列表
WEBSITE_CONFIG_LIST = {
    '00': {# 此为公用测试数据库，可以换成自己的
        'host': '192.168.235.5',
        'port': 3306,
        'user': 'dg',
        'password': 'dg',
        'db': 'dg_db_website'
    },
    '01': {
        'host': '192.168.235.162',
        'port': 3306,
        'user': 'dg_xxx',
        'password': 'dg_xxx',
        'db': 'dg_test'
    },
    '02': {
        'host': '120.24.240.87',
        'port': 3307,
        'user': 'dg_xxx',
        'password': 'dg_xxx',
        'db': 'dg_test'
    }
}

# website常量数据库配置列表
COMMON_WEBSITE_CONFIG = {
    'host': '120.24.240.87',
    'port': 3308,
    'user': 'dg',
    'password': 'dg',
    'db': 'common_website'
}

# COMMON_WEBSITE_CONFIG = {
#     'host': '192.168.235.5',
#     'port': 3306,
#     'user': 'dg',
#     'password': 'dg',
#     'db': 'common_website'
# }