# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check:wpf pass
class BundeswehrSpider(BaseSpider): 
    name = 'bundeswehr'
    website_id = 1721
    language_id = 1898
    start_urls = ['https://www.bundeswehr.de/service/bwre/queryListFilter/43250?&limit=8&offset=0']

    def parse(self, response):
        for i in response.json()['items']:
            time_ = i['metaData']['date']['dateTime'] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i['headline'],
                        'time_': time_,
                        'category1_': 'meldungen',
                        'images_': [i['picture']['fallbackSrc']]}
                yield Request(i['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('&offset=' + response.url.split('&offset=')[1], '&offset=' + str(int(response.url.split('&offset=')[1]) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = '\n'.join([i.text for i in soup.select(' .c-rte.c-rte--content p')])
        item['abstract'] = soup.select_one(' .c-rte.c-rte--content p').text.strip().strip('\n')
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item
