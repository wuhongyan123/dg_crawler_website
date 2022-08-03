from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

# check:wpf pass


class BremenSpider(BaseSpider):  # author：田宇甲
    name = 'bremen'
    website_id = 1699
    language_id = 1898
    start_urls = ['https://www.senatspressestelle.bremen.de/pressemitteilungen-1464?skip=0']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' tbody tr')[1:]:
            ssd = i.td.text.strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_': time_, 'title_': i.select(' td')[1].text.strip().strip('\n'), 'category1_': 'pressemitteilungen', 'abstract_': i.select(' td')[2].text.strip().strip('\n'), 'images_': []}
                yield Request('https://www.senatspressestelle.bremen.de/'+i.a['href'], callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request(response.url.replace('skip=' + response.url.split('skip=')[1], 'skip=' + str(int(response.url.split('skip=')[1]) + 20)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .main_article p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = response.meta['images_']
        yield item
