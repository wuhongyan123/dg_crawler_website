from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

# check:wpf pass
class DosbSpider(BaseSpider):  # author：田宇甲
    name = 'dosb'  # 这个网站主要是用于体育的，里面新闻的板块非常小，而且没有时间也没有图片，非常离谱，但是新闻质量还可以
    website_id = 1759
    language_id = 1898
    start_urls = ['https://www.dosb.de/medien-service/presse-mitteilungen']  # 全在一页

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .akkordeonBlock a'):
            if 'href' in str(i):
                meta = {'title_': i.text.strip(), 'category1_': 'News'}
                yield Request(i['href'], callback=self.check_check, meta=meta)

    def check_check(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .w580').text.strip().strip('\n')
        item['abstract'] = soup.select_one(' .w580 p:nth-child(2)').text.strip().strip('\n')
        item['pub_time'] = DateUtil.time_now_formate()
        item['images'] = []
        yield item
