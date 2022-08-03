from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


# check:wpf pass
class HamburgSpider(BaseSpider):  # author：田宇甲
    name = 'hamburg'
    website_id = 1700
    language_id = 1898
    start_urls = ['https://www.hamburg.de/pressemeldungen/']  # 这网站只返回最新的六十条消息

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .row.row-eq-height .col-xs-12.col-md-12'):
            sssd = i.select_one(' .teaser-text-meta').extract()
            ssd = sssd.text.strip().split('.')
            time_ = ssd[-1]+'-'+ssd[1]+'-'+ssd[0] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_': time_, 'title_': i.h3.text.strip().strip('\n'), 'category1_': 'pressemeldungen', 'abstract_': i.select_one(' .teaser-text.hidden-sm-down').text.strip().strip('\n'), 'images_': ['https://www.hamburg.de'+i.picture.img['src']]}
                yield Request(i.a['href'], callback=self.parse_item, meta=meta)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = '\n'.join([i.text for i in soup.select(' .richtext p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = response.meta['images_']
        yield item
