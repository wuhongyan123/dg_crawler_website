# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check:wpf pass


class BdiSpider(BaseSpider):
    name = 'bdi'
    website_id = 1717
    language_id = 1898
    start_urls = ['https://www.bdi.de/themen-und-politik/nachrichten/seite-1/']  # 目前就三页新闻
    page = 2

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' #news-container-1401 .article.articletype-0'):
            time_ = str(i.time).split('datetime="')[1].split('"')[0]+' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h2.text.strip('\n'), 'time_': time_, 'category1_': 'nachrichten', 'images_': ['https://www.bdi.de/'+i.img['src']], 'abstract_': i.select_one(' .teaser-text p').text.strip()}
                yield Request('https://www.bdi.de/'+i.h2.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request('https://www.bdi.de/themen-und-politik/nachrichten/seite-'+str(BdiSpider.page)+'/')
            BdiSpider.page += 1

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .news-text-wrap').text
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item
