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
# check: 凌敏 pass
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
class MoitgovpkSpider(BaseSpider):
    name = 'moitgovpk'
    website_id = 2111
    language_id = 1866
    is_http = 1
    start_urls = ['http://www.moit.gov.pk/LatestNews']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('.col-md-12>.upcoming-events')[:-1]
        if self.time is not None:
            t = block[-1].select_one('.bg-lightest').text.strip().split(' ')
            last_time = f"{t[2]}-{ENGLISH_MONTH[t[0]]}-{t[1][:-1].zfill(2)}" + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = i.select_one('.bg-lightest').text.strip().split(' ')
                response.meta['pub_time'] = f"{tt[2]}-{ENGLISH_MONTH[tt[0]]}-{tt[1][:-1].zfill(2)}" + ' 00:00:00'
                yield Request('http://www.moit.gov.pk' + i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = 'LatestNews'
        item['title'] = soup.select_one('#ContentPlaceHolder1_lblHeading').text.strip()
        item['pub_time'] = response.meta['pub_time']
        item['images'] = ['http://www.moit.gov.pk' + img.get('src') for img in soup.select('.col-sm-12 img')]
        item['body'] = '\n'.join(i.strip() for i in soup.select('p big')[-1].text.split('\n') if i.strip() != '')
        if not item['body']:
            item['body'] = item['title']
        item['abstract'] = item['body'].split('\n')[0]
        return item
