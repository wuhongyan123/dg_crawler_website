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
# check: 凌敏 pass
# author : 李玲宝
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
# 文章都没有图片、二级目录
class PmogovpkSpider(BaseSpider):
    name = 'pmogovpk'
    website_id = 2108
    language_id = 1866
    proxy = '02'
    start_urls = ['https://pmo.gov.pk']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        menu = soup.select('#navigation li>a')[1::4]
        for i in menu:
            yield scrapy.Request('https://pmo.gov.pk/' + i['href'], callback=self.parse_page, meta={'category1': i.text.strip()})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('table[width="95%"] tr')[1:]
        if self.time is not None:
            t = block[-1].select_one('td').text.strip().split(' ')
            last_time = f"{t[2]}-{ENGLISH_MONTH[t[0]]}-{t[1][:-1].zfill(2)}" + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = i.select_one('td').text.strip().split(' ')
                response.meta['pub_time'] = f"{tt[2]}-{ENGLISH_MONTH[tt[0]]}-{tt[1][:-1].zfill(2)}" + ' 00:00:00'
                yield Request('https://pmo.gov.pk/' + i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('#right-header-title').text.strip()
        item['pub_time'] = response.meta['pub_time']
        item['images'] = []
        item['body'] = '\n'.join(i.strip() for i in soup.select_one('#right-content-body').text.split('\n') if i.strip() != '')
        item['abstract'] = item['body'].split('\n')[0]
        return item
