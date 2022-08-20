# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233

class CsuSpider(BaseSpider):
    name = 'csu'
    website_id = 1714
    language_id = 1898
    start_urls = ['https://www.csu.de/aktuell/meldungen/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .lay-teaser .mod-teaser'):
            ssd = i.select_one(' .m-date').text.strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0].strip('.') + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.select_one(' .m-content').text.strip('\n'), 'time_': time_, 'abstract_': i.select_one(' .js-text').text, 'images_': ['https://www.csu.de/'+i.img['src']]}
                yield Request('https://www.csu.de/'+i.a['href'], callback=self.parse_item, meta=meat)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = 'meldungen'
        item['category2'] = None
        item['body'] = '\n'.join([i.text for i in soup.select(' .m-text p')[1:]])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item
