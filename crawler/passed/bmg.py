# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check: wpf pass
German_month = {
    'Januar': '01',
    'Februar': '02',
    'März': '03',
    'April': '04',
    'Mai': '05',
    'Juni': '06',
    'Juli': '07',
    'August': '08',
    'September': '09',
    'Oktober': '10',
    'November': '11',
    'Dezember': '12'
}

class BmgSpider(BaseSpider):
    name = 'bmg'
    website_id = 1687
    language_id = 1898
    start_urls = ['https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen.html']
    page = 1

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .news .o-grid.c-component ul li')[0:9]:
            ssd = i.span.text.strip().split(' ')
            time_ = ssd[-1] + '-' + German_month[ssd[1]] + '-' + ssd[0].strip('.') + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h3.text.strip('\n'), 'time_': time_, 'category1_': 'pressemitteilungen', 'images_': [], 'abstract_': i.p.text.strip('\n')}
                yield Request('https://www.bundesgesundheitsministerium.de'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            if 'Page%5D=' not in response.url:
                yield Request('https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen.html?cHash=8a0127e3f719ef9564581343d55d9564&tx_news_pi1%5B%40widget_0%5D%5BcurrentPage%5D=2')
            else:
                yield Request('https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen.html?cHash=8a0127e3f719ef9564581343d55d9564&tx_news_pi1%5B%40widget_0%5D%5BcurrentPage%5D='+str(BmgSpider.page))
            BmgSpider.page += 1

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .c-text').text
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item
