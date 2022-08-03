from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import re

ENGLISH_MONTH = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sept': '09',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

# author : 李玲宝
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
# 网站本来就没有二级标题
# check:凌敏 pass
class BalochistanSpider(BaseSpider):
    name = 'balochistan'
    website_id = 2102
    language_id = 1866
    start_urls = ['https://balochistan.gov.pk/category/chief-minister/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        category1 = soup.select('#menu-item-831>.sub-menu a')
        for i in category1:
            yield scrapy.Request(i['href'], callback=self.parse_page, meta={'category1': i.text.strip()})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('#main>div')
        if self.time is not None:
            t1 = block[-1].select_one('.date').text.split(' ')
            t2 = re.search('uploads/\d{4}', block[-1].select_one('img')['src']).group()[-4:]
            last_time = f'{t1}-{ENGLISH_MONTH[t2[1]]}-{t2[2].zfill(2)}' + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                if i.select_one('img') is not None:
                    tt1 = i.select_one('.date').text.split(' ')
                    tt2 = re.search('uploads/\d{4}', i.select_one('img')['src']).group()[-4:]
                    response.meta['title'] = i.select_one('h4').text.strip()
                    response.meta['pub_time'] = f'{tt2}-{ENGLISH_MONTH[tt1[1]]}-{tt1[2].zfill(2)}' + ' 00:00:00'
                    yield Request(i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)
        self.logger.info("时间截止")  # 网站无法翻页

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        if soup.select_one('.entry-content') is not None:
            item['category1'] = response.meta['category1']
            item['title'] = response.meta['title']
            item['pub_time'] = response.meta['pub_time']
            item['images'] = [img.get('src') for img in soup.select('article img')]
            item['body'] = '\n'.join(i.strip() for i in soup.select_one('.entry-content').text.split('\n') if i.strip() != '')
            item['abstract'] = item['body'].split('\n')[0]
            if item['body']:
                return item
