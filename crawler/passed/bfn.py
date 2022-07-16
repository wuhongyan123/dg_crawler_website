from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
# check: wpf pass
# author: robot_2233

class BfnSpider(BaseSpider):
    name = 'bfn'
    website_id = 1737
    language_id = 1898
    start_urls = ['https://www.bfn.de/pressemitteilungen?page=1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .s-search__results-grid .items'):
            ssd = i.select_one(' .field.field--name-field-publishing-date.field__item').text.strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.select_one(' .s-h3').text.strip(), 'time_': time_, 'abstract_': i.select_one(' .field.field--name-field-abstract.field__item').text.strip(), 'category1_': 'News'}
                yield Request('https://www.bfn.de/'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('page='+response.url.split('page=')[1], 'page='+str(int(response.url.split('page=')[1])+1)), meta=meat)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .field.field--name-field-text.field__item p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = []
        yield item
