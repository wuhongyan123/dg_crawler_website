from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import time

ENGLISH_MONTH = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

# author : 李玲宝
# check: 凌敏 pass
class KaliokalamSpider(BaseSpider):
    name = 'kaliokalam'
    website_id = 1891
    language_id = 1779
    start_urls = ['https://www.kaliokalam.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select('#menu-item-8705>ul>li'):
            for j in i.select('.depth1>li'):  # 存放二级标题
                url = j.select_one('a')['href'] + 'page/'
                yield scrapy.Request(url + '1/', callback=self.parse_page, meta={'category1': i.select_one('a')['title'], 'category2': j.select_one('a')['title'], 'page': 1, 'url': url})
            if (i.select_one('.depth1>li')) is None:  # 如果没有二级标题，i.select('.depth1>li')为空
                url = i.select_one('a')['href'] + 'page/'
                yield scrapy.Request(url + '1/', callback=self.parse_page, meta={'category1': i.select_one('a')['title'],'category2': None, 'page': 1, 'url': url})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('main.order-lg-last article')
        if self.time is not None:
            t = block[-1].select_one('.meta-content').text.strip().split(' ')
            last_time = time.strftime('%Y-%m-%d', time.strptime(f"{t[2]}.{ENGLISH_MONTH[t[0]]}.{t[1][:-1]}", '%Y.%m.%d')) + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = i.select_one('.meta-content').text.strip().split(' ')
                response.meta['pub_time'] = time.strftime('%Y-%m-%d', time.strptime(f"{tt[2]}.{ENGLISH_MONTH[tt[0]]}.{tt[1][:-1]}", '%Y.%m.%d')) + ' 00:00:00'
                yield Request(i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)
        if soup.select_one('div.navigation .next') is not None:
            response.meta['page'] += 1
            yield Request(response.meta['url'] + str(response.meta['page']) + '/', callback=self.parse_page, meta=response.meta)
        else:
            self.logger.info("时间截止")

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['category2'] = response.meta['category2']
        item['title'] = soup.select_one('h1.entry-title').text.strip()
        for i in soup.select('.entry-content>p'):
            if (i.text.strip() != ''):
                item['abstract'] = i.text.strip()
                break
        item['pub_time'] = response.meta['pub_time']
        item['images'] = [img.get('src') for img in soup.select('.entry-wrapper img')]
        item['body'] = '\n'.join(i.text.strip() for i in soup.select('.entry-content>p') if (i.text.strip() != ''))
        return item
