# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check: wpf pass
class BmuSpider(BaseSpider):
    name = 'bmu'
    website_id = 1689
    language_id = 1898
    start_urls = ['https://www.bmuv.de/presse/pressemitteilungen?cHash=58e263871d6725de4fcfae8736816765&tx_bmubarticles_articles%5B%40widget_0%5D%5BcurrentPage%5D=1']
    page = 2

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .rf-c-articles-list article'):
            ssd = i.select_one(' .rf-c-articles-list__meta').text.strip().split(' ')[-1].strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.a.text.strip('\n'), 'time_': time_, 'category1_': 'pressemitteilungen', 'images_': [], 'abstract_': ''}
                yield Request('https://www.bmuv.de'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request('https://www.bmuv.de/presse/pressemitteilungen?cHash=58e263871d6725de4fcfae8736816765&tx_bmubarticles_articles%5B%40widget_0%5D%5BcurrentPage%5D='+str(BmuSpider.page))
            BmuSpider.page += 1

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .o-body__item').text
        item['abstract'] = soup.select_one(' .o-body__item p').text
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item
