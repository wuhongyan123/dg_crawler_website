# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233
# check:wpf pass
class BundeswahlleiterSpider(BaseSpider):
    name = 'bundeswahlleiter'
    website_id = 1715
    language_id = 1898
    start_urls = [f'https://bundeswahlleiter.de/info/presse/mitteilungen/{i}.html' for i in ['europawahl-2019', 'bundestagswahl-2021', 'bundestagswahl-2017']]  # 这个网站只放了有关大事件的新闻，更新也慢

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .list-news__list .list-news__listitem'):
            ssd = i.select_one(' .list-news__listitemdate').text.strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0].strip('.') + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.a.text.strip('\n'), 'time_': time_, 'category1_': i.select_one(' .list-news__listitemtag').text}
                yield Request('https://bundeswahlleiter.de/info/presse/mitteilungen/'+i.a['href'], callback=self.parse_item, meta=meat)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = '\n'.join([i.text for i in soup.select(' #main p')[1:]])
        item['abstract'] = soup.select(' #main p')[1].text.strip().strip('\n')
        item['pub_time'] = response.meta['time_']
        item['images'] = []
        yield item
