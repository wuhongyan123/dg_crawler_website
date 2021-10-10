# encoding: utf-8

# sql语句
SQL_FILTER = "select md5 from news where website_id = {} and md5 = '{}'"
SQL_DEVELOPMENT_SELECT = 'SELECT * FROM development WHERE is_open = 1 ORDER BY run_time'
SQL_DEVELOPMENT_TIME_UPDATE = "UPDATE development SET run_time = '{}' WHERE name = '{}'"