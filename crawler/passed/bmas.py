# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check: wpf pass
class BmasSpider(BaseSpider):
    name = 'bmas'
    website_id = 1683
    language_id = 1898
    start_urls = ['https://www.bmas.de/SiteGlobals/Forms/Suche/Aktuelles-Suche_Formular.html?showNoStatus.HASH=925f4fc0676854b71498&showNoGesetzesstatus=true&showNoStatus=true&showNoGesetzesstatus.HASH=1b0d1c32947e6a70d38e&gtp=%2526901e4b79-b3c2-43ca-b117-ce35f3e2f243_list%253D1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .relative pp-teaser'):
            time_ = str(i.time).strip().split('datetime="')[1].split('"')[0]+' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h3.text.strip('\n'),
                        'time_': time_,
                        'category1_': 'Pressemitteilungssuche',
                        'abstract_': i.select_one(' .text').text.strip(),
                        'images_': []}
                yield Request(i.select_one(' pp-link')['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('_list%253D' + response.url.split('_list%253D')[1], '_list%253D' + str(int(response.url.split('_list%253D')[1]) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .body-text').text.strip()
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item


