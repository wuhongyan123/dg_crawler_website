from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233

class NachhaltigkeitsratSpider(BaseSpider):
    name = 'nachhaltigkeitsrat'
    website_id = 1730
    language_id = 1898
    start_urls = ['https://www.nachhaltigkeitsrat.de/aktuelles/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .post-previews.inner-grid .panel'):
            try:  # 有些不是新闻
                time_ = str(i.time).strip().split('datetime="')[1].split('"')[0].replace('T', ' ').split('+')[0]
                if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                    meat = {'title_': i.h4.text.strip(), 'time_': time_, 'category1_': i.select_one(' .category.category-name').text, 'images_': (i.img['src'])}
                    yield Request(i.a['href'], callback=self.parse_item, meta=meat)
            except:
                pass
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            if 'seite/' not in response.url:
                yield Request(response.url+'seite/2/')
            else:
                yield Request(response.url.replace('seite/'+response.url.split('seite/')[1], 'seite/'+str(int(response.url.split('seite/')[1].strip('/'))+1)+'/'))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .entry-content p')])
        item['abstract'] = item['body'].split('\n')[0]
        item['pub_time'] = response.meta['time_']
        item['images'] = [response.meta['images_']]
        yield item
