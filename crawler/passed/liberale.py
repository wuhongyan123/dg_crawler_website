# encoding: utf-8
import time

from bs4 import BeautifulSoup
from utils.util_old import Util
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

#Author: 贺佳伊
class LiberaleSpiderSpider(BaseSpider):
    name = 'liberale'
    website_id = 1713
    language_id = 1898
    start_urls = ['https://www.liberale.de/page/meldungen?tags=&themes=']

    def parse(self,response):
        # time.sleep(3)
        soup=BeautifulSoup(response.text,'lxml')
        flag = True
        a = soup.select(
            '#top > div > div.panel-lcs-box.panel-lcs-box-2 > div > div > div > div.view-content > div > ul > li > div')
        for i in a:
            t = i.select_one('span').text
            t1 = t.split('.')
            pub_time = t1[2] + '-' + t1[1] + '-' + t1[0] + " 00:00:00"
        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(pub_time):
             for i in a:
                news_url = 'https://www.liberale.de/' + i.select_one('a').get('href')
                response.meta['title'] = i.select_one('h3 > a ').text
                t = i.select_one('span').text
                t1 = t.split('.')
                response.meta['pub_time'] = t1[2] + '-' + t1[1] + '-' + t1[0] + " 00:00:00"
                response.meta['abstract'] = i.select_one('p').text
                response.meta['category1'] = i.select_one('span:nth-child(3)').text
                try:
                    response.meta['category2'] = i.select_one('span.tag.tagLast').text
                except:
                    response.meta['category2'] = None
                try:
                    yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                except:
                    pass
        else:
            self.logger.info("时间截至")
            flag = False
        if flag:
            try:
                next_page_url = 'https://www.liberale.de/' + soup.select_one('#top > div > div.panel-lcs-box.panel-lcs-box-2 > div > div > div > div.item-list > ul > li.pager-next > a').get('href')
                yield Request(url=next_page_url, callback=self.parse,meta=response.meta)
            except:
                pass

    def parse_item(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['category2'] = response.meta['category2']
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        item['body'] = ''
        a1 = soup.select('#block-system-main > div > div > div > div > div > div > div > div > p')
        for i in a1:
            item['body'] += i.text + '\n\r'
        item['abstract'] = response.meta['abstract']
        item['images'] = []
        a = soup.select_one('#block-system-main > div > div > div > div.panel-col-first.panel-panel > div > div > div > div > span.image > img').get('src')
        item['images'].append(a)
        yield item