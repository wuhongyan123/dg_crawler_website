# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import time

# author: robot_2233
# check:wpf pass
class SachsendeSpider(BaseSpider):
    name = 'sachsende'
    website_id = 1707
    language_id = 1898
    start_urls = [f'https://www.medienservice.sachsen.de/medien/news/search.json?utf8=%E2%9C%93&search%5Bfirst_searched%5D={str(time.strftime("%Y-%m-%d", time.localtime()))}+12%3A25%3A36+UTC&search%5Bquery%5D=&search%5Bfrom%5D=&search%5Bto%5D=&search%5Bfilter%5D%5B%5D=&search%5Bfilter%5D%5B%5D=press_releases&ie-polyfill=&page=1']

    def parse(self, response):
        for i in response.json()['teaser']:
            iii = BeautifulSoup(i, 'html.parser')
            ssd = iii.select_one(' .time').text.strip().split(',')[0].split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0] + ' 00:00:00'
            iii.select_one(' .time').extract()
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': iii.select_one(' .teaser-text').text.strip(),
                        'time_': time_,
                        'category1_': 'medien',
                        'images_': 'https://www.medienservice.sachsen.de/'+iii.img['src']}
                yield Request('https://www.medienservice.sachsen.de/'+iii.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('&page=' + response.url.split('&page=')[1], '&page=' + str(int(response.url.split('&page=')[1]) + 1)), meta=meat)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .col p')])
        item['abstract'] = soup.select_one(' .col p').text
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item


