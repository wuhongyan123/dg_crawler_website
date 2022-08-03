# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check:wpf pass

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

class BundSpider(BaseSpider):
    name = 'bund'
    website_id = 1718
    language_id = 1898
    start_urls = ['https://www.bund.net/service/presse/pressemitteilungen/news-page/1/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .m-layout-grid.m-layout-grid__newsList article'):
            ssd = i.select_one(' .rte-paragraph.rte-paragraph__caption').text.strip().split(' ') if '|' not in i.select_one(' .rte-paragraph.rte-paragraph__caption').text else i.select_one(' .rte-paragraph.rte-paragraph__caption').text.split('|')[0].strip().split(' ')
            time_ = ssd[-1] + '-' + German_month[ssd[1]] + '-' + ssd[0].strip('.') + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h1.text.strip('\n'), 'time_': time_, 'category1_': 'news'}
                yield Request('https://www.bund.net/'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request(response.url.replace('news-page/' + response.url.split('news-page/')[1], 'news-page/' + str(int(response.url.split('news-page/')[1].strip('/')) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .das-hier-ist-column-main').text.replace('\n','').replace('      ', '\n')
        item['abstract'] = soup.select_one(' .das-hier-ist-column-main p').text.replace('\n','').replace('      ', '\n')
        item['pub_time'] = response.meta['time_']
        item['images'] = []
        yield item
