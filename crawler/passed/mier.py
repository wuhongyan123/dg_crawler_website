# encoding: utf-8
import html
import json
from bs4 import BeautifulSoup
import common
import utils.date_util
from common.date import ENGLISH_MONTH
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
import time


# Author:陈卓玮
# check：凌敏 pass

class mier_spider(BaseSpider):
    name = 'mier'
    website_id = 708
    language_id = 2037
    start_urls = ['https://www.mier.org.my/op-ed/page/1']

    def parse(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.select('#pro-gallery-margin-container a div article'):
            time = (i.select_one('div ul li .post-metadata__date').text)
            title = (i.select_one('h2').text)
            url = (i.select_one("div > div.JMCi2v.blog-post-homepage-link-hashtag-hover-color.so9KdE.lyd6fK > a").get(
                'href'))
            abstract = (i.select_one('.BOlnTh').text)
            yield Request(url = url,callback=self.parse_essay,meta={'time':time,'title':title,'abstract':abstract})

        time = (soup.select_one('#pro-gallery-margin-container a div article div ul li .post-metadata__date').text)
        try:
            if self.time==None or self.time <=utils.date_util.DateUtil.formate_time2time_stamp(self.format_time(time)):
                n_url = (soup.find('a', {'aria-label': 'Next page'}).get('href'))
                yield Request(url=n_url)
        except:
            pass

    def parse_essay(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        item['title'] = response.meta['title']
        item['category1'] = 'News'
        item['body'] = ''.join([i.text for i in soup.select('article p')])
        item['abstract'] = response.meta['abstract']
        item['pub_time'] = self.format_time(response.meta['time'])
        item['images'] = [i.get('src') for i in soup.select('img')]
        yield item

    def format_time(self,time):
        if 'ago' in time:
            day = int(time.split(' ')[0])
            return utils.date_util.DateUtil.time_stamp2formate_time(utils.date_util.DateUtil.time_ago(day=day))

        elif len(time.split(' ')) == 2:
            day = time.split(' ')[1]
            month = str(common.date.ENGLISH_MONTH[time.split(' ')[0]])
            year = '2022'
            return year + '-' + month + '-' + day + ' 00:00:00'

        elif len(time.split(' ')) == 3:
            time = time.replace(',', '')
            day = time.split(' ')[1]
            month = str(common.date.ENGLISH_MONTH[time.split(' ')[0]])
            year = time.split(' ')[2]
            return year + '-' + month + '-' + day + ' 00:00:00'

