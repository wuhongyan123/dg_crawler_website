# encoding: utf-8

from fire.core import Fire
from libs.mysql import Mysql
from config.db_config import *
from common.sql import *
from utils.date_util import DateUtil
import os
import fire

class Main:
    def __init__(self, db='01', time='days_ago:3'):
        self.db = db
        self.time = time
        self.common_db = None
        self.run()

    def run(self):
        command = 'scrapy crawl {} -a db={} -a time={} -a proxy={}'
        while True:
            try:
                self.common_db = Mysql(COMMON_WEBSITE_CONFIG)
                for i in self.common_db.select(SQL_DEVELOPMENT_SELECT):
                    if i[1]+'.py' in os.listdir('crawler/v1') or i[1]+'.py' in os.listdir('crawler/pass'):
                        self.common_db.execute(SQL_DEVELOPMENT_TIME_UPDATE.format(DateUtil.time_now_formate(), i[1]))
                        command_ = command.format(i[1], self.db, self.time, i[2])
                        print(command_)
                        os.system(command_)
                        break
                self.common_db = None
            except Exception as e:
                print("主进程出错 ==> {}".format(e))
                self.common_db = None


# 主进程函数
# python -m main
# python -m main --db=00 --time=now
if __name__ == "__main__":
    fire.Fire(Main)