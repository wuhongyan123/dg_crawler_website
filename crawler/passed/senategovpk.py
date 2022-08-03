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
class SenategovpkSpider(BaseSpider):
    name = 'senategovpk'
    website_id = 2107
    language_id = 1866
    start_urls = ['https://senate.gov.pk/en/press_release.php?id=-1&catid=6&cattitle=Media%20Centre']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('#example tr')[1:]
        if self.time is not None:
            t = block[-1].select_one('td[data-label="Date"]').text.strip().split(' ')
            last_time = f"{t[1][-4:]}-{ENGLISH_MONTH[t[1].split(',')[0]]}-{t[0][:-2].zfill(2)}" + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = i.select_one('td[data-label="Date"]').text.strip().split(' ')
                response.meta['pub_time'] = f"{tt[1][-4:]}-{ENGLISH_MONTH[tt[1].split(',')[0]]}-{tt[0][:-2].zfill(2)}" + ' 00:00:00'
                response.meta['title'] = i.select_one('a').text.strip()
                yield Request('https://senate.gov.pk/en/' + i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = 'press_release'
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        item['images'] = ['https://senate.gov.pk' + img.get('src')[2:] for img in soup.select('.col-xs-12 img')]
        item['body'] = '\n'.join(i.strip() for i in soup.select_one('.col-xs-12>div').text.split('\n') if i.strip() != '')
        item['abstract'] = item['body'].split('\n')[0]
        return item
