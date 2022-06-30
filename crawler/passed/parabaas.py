from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import time

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
    'December': '12'
}

# author : 李玲宝
# check: 凌敏 pass
class ParabaasSpider(BaseSpider):
    name = 'parabaas'
    website_id = 1892
    language_id = 1779
    start_urls = ['https://www.parabaas.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select('li.bg-warning')[1].select('a'):
            url = 'https://www.parabaas.com/' + i['href'].replace('?', '?&') + '&p='
            yield scrapy.Request(url + '1', callback=self.parse_page, meta={'category1': i.text.strip(), 'page': 1, 'url': url})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        if (soup.select_one('.col-md-8 ul>a') is None):  # 没有文章了，爬虫结束，退出函数
            self.logger.info("时间截止")
            return 1
        block = soup.select('.col-md-8 ul>a')
        if self.time is not None:
            t = block[-1].select_one('span.text-info').text.strip().split(' ')
            if (t[-1]) == '-0001':
                t[-1] = '2022'  # 新闻没有时间时，网站年份会显示'-0001'，我给个今年的年份
            last_time = f"{t[-1]}-{ENGLISH_MONTH[t[-2]]}-01" + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = i.select_one('span.text-info').text.strip().split(' ')
                if (tt[-1]) == '-0001':
                    tt[-1] = '2022'  # 新闻没有时间时，网站年份会显示'-0001'，我给个今年的年份
                url = 'https://www.parabaas.com/' + i['href']
                response.meta['pub_time'] = f"{tt[-1]}-{ENGLISH_MONTH[tt[-2]]}-01" + ' 00:00:00'
                yield Request(url, callback=self.parse_item, meta=response.meta)
        response.meta['page'] += 1
        yield Request(response.meta['url'] + str(response.meta['page']), callback=self.parse_page, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select('center>h5')[1].text.strip()
        content = soup.select('.col-print-12 .list-group-item')[2]
        item['abstract'] = content.text.strip().split('\n')[0]
        item['body'] = '\n'.join(i.strip() for i in content.text.strip().split('\n') if (i.strip() != ''))
        item['pub_time'] = response.meta['pub_time']
        item['images'] = []
        for img in content.select('img'):
            if (img.get('src').startswith('http')):
                item['images'].append(img.get('src'))
            else:
                item['images'].append('https://www.parabaas.com/' + img.get('src'))
        return item
