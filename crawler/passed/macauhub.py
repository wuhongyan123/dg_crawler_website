# encoding: utf-8
import requests
import scrapy
from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
import re
import common.date as date

# author:凌敏
ENGLISH_MONTH = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12',
    }
DAY = {'1': '01', '2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07', '8': '08', '9': '09'}

class macauhubSpider(BaseSpider):
    name = 'macauhub'
    website_id = 2087
    language_id = 2266
    start_urls = ['https://macauhub.com.mo/']  # http://www.macauhub.com.mo/cn/
    # is_http = 1

    def parse(self, response):
        soup = BeautifulSoup(response.text, features='lxml')
        for i in soup.find('ul', class_='dropdown-menu').find_all('li')[1:]:
            cate_url = i.find('a').get('href')
            category1 = i.find('a').text
            meta1 = {'category1': category1}
            yield scrapy.Request(url=cate_url, callback=self.parse2, meta=meta1)

        cate_url = soup.find('li', id='menu-item-40497').find('a').get('href')
        category1 = soup.find('li', id='menu-item-40497').find('a').text
        meta1 = {'category1': category1}
        yield scrapy.Request(url=cate_url, callback=self.parse2, meta=meta1)

    def parse2(self, response, **kwargs):
        soup = BeautifulSoup(response.text, features='lxml')
        last_time = ''
        for i in soup.find('div', class_='main-news-box').find_all('div', class_='main-sub-news-block'):
            title = i.find('div', class_='mh-news-title').find('h2').find('a').text
            content_url = i.find('div', class_='mh-news-title').find('h2').find('a').get('href')
            t = i.find('div', class_='mh-news-date-tag').find('div', class_='news-date').text
            year = t.split(' ')[2]
            month = ENGLISH_MONTH[t.split(' ')[1]]
            d = t.split(' ')[0]
            if d in DAY.keys():
                day = DAY[d]
            else:
                day = t.split(' ')[0]
            pub_time = year + '-' + month + '-' + day + ' 00:00:00'
            abstract = i.find('div', class_='mh-news-desc').find('a').text
            meta = {
                'category1': response.meta['category1'],
                'title': title,
                'pub_time': pub_time,
                'abstract': abstract
            }
            last_time = pub_time
            yield scrapy.Request(content_url, callback=self.parse3, meta=meta)
        turn_page = soup.find('div', class_='pagination').find_all('a')[-2].get('href')
        if self.time is not None:
            if self.time < DateUtil.formate_time2time_stamp(last_time):
                yield scrapy.Request(url=turn_page, callback=self.parse2, meta=response.meta)
            else:
                self.logger.info("时间截止")
        else:
            yield scrapy.Request(url=turn_page, callback=self.parse2, meta=response.meta)


    def parse3(self, response, **kwargs):
        item = NewsItem()
        soup = BeautifulSoup(response.text, features='lxml')
        item['body'] = ''
        for i in soup.find('div', class_='detail-body-text').find_all('p'):
            item['body'] += i.text
        item['abstract'] = response.meta['abstract']
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        item['category1'] = response.meta['category1']
        item['category2'] = ''
        item['images'] = []
        yield item
