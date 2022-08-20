# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check: wpf pass
class BmelSpider(BaseSpider):  # 新闻量比较少
    name = 'bmel'
    website_id = 1685
    language_id = 1898
    start_urls = ['https://www.bmel.de/SiteGlobals/Forms/Suche/DE/Pressemitteilungssuche/Pressemitteilungssuche_Formular.html?gtp=42764_list%253D1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .searchresult .c-searchteaser'):
            time_ = str(i.time).strip().split('datetime="')[1].split('"')[0]+' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h2.a.text.strip('\n'),
                        'time_': time_,
                        'category1_': 'Pressemitteilungssuche',
                        'abstract_': i.select_one(' p:nth-child(2)').text.strip(),
                        'images_': ['https://www.bmel.de/'+i.img['src'] if i.img is not None else None]}
                yield Request('https://www.bmel.de/'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('_list%253D' + response.url.split('_list%253D')[1], '_list%253D' + str(int(response.url.split('_list%253D')[1]) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .small-12.medium-10.large-8.s-content-8.column').text.strip()
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item


