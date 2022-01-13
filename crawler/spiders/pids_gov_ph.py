import socket

import common.date
from crawler.spiders import BaseSpider
# 此文件包含的头文件不要修改
import scrapy
from utils.util_old import *
from crawler.items import *
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from utils import date_util

from datetime import datetime
import time
import re
import requests

# author:魏芃枫


class Pids(BaseSpider):
    name = 'pids_gov_ph'
    start_urls = ['https://pids.gov.ph/press-releases']
    website_id = 1256  # 网站的id(必填)
    language_id = 1866  # 所用语言的id

    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):  # 获取不同年份下的不同页
        socket.setdefaulttimeout(30)
        for i in range(2013, 2022):
            head_url = "https://pids.gov.ph/press-releases?year="+str(i)
            response_page = requests.get(head_url)
            soup = BeautifulSoup(response_page.text, 'html.parser')
            page_list = soup.select(".paginate-wrapper>ul>li")
            page_num = int(len(page_list) / 2 - 4) # 根据li标签数量计算得页数
            for j in range(1, page_num+1):
                url = head_url+"&pagenum="+str(j)
                yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        socket.setdefaulttimeout(30)
        soup = BeautifulSoup(response.text, 'html.parser')
        menu = soup.find_all(attrs={'class': "row column content-list arrow-button with-icon"})
        for i in menu:
            try:
                title = i.select_one("h4").text
                date = i.select_one('p').text.split(" ")
                month = str(common.date.ENGLISH_MONTH[date[1]])
                day = date[2].replace(',', "")
                year = date[3]
                pub_time = str(year) + "-" + str(month) + "-" + str(day) + " 00:00:00"
                timestamp = date_util.DateUtil.formate_time2time_stamp(pub_time)
                if self.time == None or timestamp >= int(self.time):
                    href = "https://pids.gov.ph"+i.select_one("a").get('href')
                    meta = {'title': title, 'pub_time': pub_time}
                    yield Request(href, callback=self.parse_detail, meta=meta)
                else:
                    self.logger.info('时间截止！')
            except:
                continue

    def parse_detail(self, response):
        socket.setdefaulttimeout(30)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find(attrs={"class": 'large-8 columns page-content-column'}).text
        item = NewsItem()
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        item['body'] = body
        item['abstract'] = body
        item['category1'] = None
        item['category2'] = None
        item['images'] = None
        return item