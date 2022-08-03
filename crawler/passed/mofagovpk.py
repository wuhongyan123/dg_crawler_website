import re

from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

ENGLISH_MONTH = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12',
}

# author : 李玲宝
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
# 网站的新闻本来就没有二级标题和图片
# check:凌敏 pass
class MofagovpkSpider(BaseSpider):
    name = 'mofagovpk'
    website_id = 2103
    language_id = 1866
    start_urls = ['https://mofa.gov.pk/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        category1 = soup.select('#menu-item-8296>.sub-menu>li>a')[1:]
        for i in category1:
            url = i['href'] + 'page/'
            yield scrapy.Request(url + '1/', callback=self.parse_page, meta={'category1': i.text.strip(), 'url': url, 'page': 1})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('.blogger>div')
        if self.time is not None:
            t = block[-1].select_one('.categs').text.strip().split(' ')
            last_time = f'{t[-1]}-{ENGLISH_MONTH[t[-3]]}-{t[-2][:-3].zfill(2)}' + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                if i.select_one('.categs') is not None:
                    tt = i.select_one('.categs').text.strip().split(' ')
                    response.meta['pub_time'] = f'{tt[-1]}-{ENGLISH_MONTH[tt[-3]]}-{tt[-2][:-3].zfill(2)}' + ' 00:00:00'
                    yield Request(i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)
        if soup.select_one('.nav-links .next') is not None:
            response.meta['page'] += 1
            yield Request(response.meta['url'] + str(response.meta['page']) + '/', callback=self.parse_page, meta=response.meta)
        else:
            self.logger.info("时间截止")

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('.maintitle').text.strip()
        item['pub_time'] = response.meta['pub_time']
        item['images'] = []
        item['body'] = '\n'.join(i.strip() for i in soup.select_one('.entryfull').text.split('\n') if i.strip() != '')
        item['abstract'] = item['body'].split('\n')[0]
        if item['body']:
            return item
