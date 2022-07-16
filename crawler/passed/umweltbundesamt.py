from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import datetime, json

# author: robot_2233

class UmweltbundesamtSpider(BaseSpider):
    name = 'umweltbundesamt'
    website_id = 1733
    language_id = 1898
    start_urls = ['https://www.umweltbundesamt.de/views/ajax?view_name=overviews&view_display_id=pressinformation&view_args=&view_path=presse%2Fpressemitteilungen&view_base_path=presse%2Fpressemitteilungen&view_dom_id=a588b6e53f0d3dd70e9f6deac48f8e03&pager_element=0&year%5Bvalue%5D%5Byear%5D=']

    def start_requests(self):
        yield Request(self.start_urls[0]+str(datetime.datetime.now().strftime("%Y")))

    def parse(self, response):
        aim_html = json.loads(response.text)
        soup = BeautifulSoup(aim_html[2]['data'], 'html.parser')
        for i in soup.select(' .view-content .box-list-odd-even.document-list li'):
            ssd = str(i.time).strip().split('datetime="')[1].split('"')[0]
            time_ = ssd.replace('T', ' ').split('+')[0]
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meat = {'title_': i.h5.text.strip(), 'time_': time_, 'abstract_': i.select_one(' .span10.article-text p').text.strip(), 'category1_': 'Newsroom'}
                yield Request('https://www.umweltbundesamt.de/'+i.a['href'], callback=self.parse_item, meta=meat)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace('year%5D='+response.url.split('year%5D=')[1], 'year%5D='+str(int(response.url.split('year%5D=')[1])-1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .article-content p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['time_']
        item['images'] = []
        yield item
