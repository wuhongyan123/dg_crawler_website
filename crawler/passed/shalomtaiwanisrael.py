# encoding: utf-8
import time

from bs4 import BeautifulSoup
from utils.util_old import Util
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

#Author: 贺佳伊
# check: 彭雨胜
# pass
class shalomtaiwanisraelSpiderSpider(BaseSpider):
    name = 'shalomtaiwanisrael'
    website_id = 1927
    language_id = 1813
    start_urls = ['https://shalomtaiwanisrael.wordpress.com/']

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        a = soup.select('#categories-7 > ul > li')
        for i in a[2:]:
            response.meta['category1'] = i.select_one('a').text
            i1 = i.select('ul > li > a')
            for t in i1[1:]:
                response.meta['category2'] = t.text
                news_page_url = t.get('href')
                yield Request(url=news_page_url, callback=self.parse_page, meta=response.meta)
    def parse_page(self,response):
        time.sleep(3)
        soup=BeautifulSoup(response.text,'lxml')
        flag = True
        a = soup.select('#main > article ')
        for i in a:
            t = i.select_one(' header > div > span.posted-on > a > time.entry-date.published').get('datetime')
            pub_time = t[0:10] + ' ' + t[11:-6]
        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(pub_time):
             for i in a:
                news_url = i.select_one('header > h1 > a').get('href')
                response.meta['title'] = i.select_one('header > h1 > a').text
                t = i.select_one(' header > div > span.posted-on > a > time.entry-date.published').get('datetime')
                response.meta['pub_time'] = t[0:10] + ' ' + t[11:-6]
                response.meta['abstract'] = i.select_one('div > p').text
                try:
                    yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                except:
                    pass
        else:
            self.logger.info("时间截至")
            flag = False
        if flag:
            try:
                next_page_url = soup.select_one('#main > nav > div > div > a').get('href')
                yield Request(url=next_page_url, callback=self.parse_page,meta=response.meta)
            except:
                pass

    def parse_item(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['category2'] = response.meta['category2']
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        a = soup.select('#main > article > div > p ')
        ar = ''
        for i in a:
            try:
                p = i.text
                ar += p + '\n\r'
            except:
                pass
        item['body'] = ar
        item['abstract'] = response.meta['abstract']
        a1 = soup.select('#main > article > div > p > a')
        pic = []
        for i in a1:
            try:
                p = i.get('href')
                if (p[-4] == '.'):
                    pic.append(p)
            except:
                pass
        item['images'] = pic
        yield item