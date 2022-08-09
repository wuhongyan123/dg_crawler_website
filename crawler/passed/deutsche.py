# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233

class DeutscheSpider(BaseSpider):  # 一个简单的静态爬虫，但是这个图书馆新闻比较少
    name = 'deutsche'
    website_id = 1756
    language_id = 1898
    start_urls = ['https://www.deutsche-digitale-bibliothek.de/content/journal/entdecken?client=DDB-NEXT&page=0']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .view-content .views-row'):
            ssd = i.select_one(' .field.field--name-node-post-date.field--type-ds.field--label-hidden.field--item').text.strip().split('.')
            time_ = ssd[-1].strip() + '-' + ssd[1].strip() + '-' + ssd[0].strip() + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.select_one(' .title').text.strip('\n'),
                        'time_': time_,
                        'category1_': 'Article',
                        'abstract_': i.p.text.strip(),
                        'images_': [i.select_one(' .field.field--name-field-image-media.field--type-image.field--label-hidden.field--item picture img')['src']]}
                yield Request('https://www.deutsche-digitale-bibliothek.de'+i.select_one(' .title a')['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('page=' + response.url.split('page=')[1], 'page=' + str(int(response.url.split('page=')[1].strip('=')) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .field.field--name-body.field--type-text-with-summary.field--label-hidden.field--item').text.strip().strip('\n')
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = response.meta['images_']
        yield item


#时间
