from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import time

# author : 胡楷
# chekc: pys
class eksisozlukSpider(BaseSpider):
    name = 'eksisozluk'
    website_id = 1812
    language_id = 2227
    allowed_domains = ['eksisozluk.com']
    start_urls = ['https://eksisozluk.com']
    proxy = "02"

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        categories = soup.select('#sub-navigation a')[0:17]
        del categories[6]
        del categories[2]
        for category in categories:
            category_url = 'https://eksisozluk.com' + category.get('href')
            meta = {'category1': category.text}
            yield Request(url=category_url, callback=self.parse_page, meta=meta)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.select('ul.topic-list.partial > li > a')
        flag = True
        if self.time is not None:
            last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:
                article_url = 'https://eksisozluk.com' + article.get('href')
                yield Request(url=article_url, callback=self.parse_item, meta=response.meta)
        else:
            flag = False
            self.logger.info("时间截止")
        if flag:
            next_page = 'https://japantoday.com' + soup.select_one('div.quick-index-continue-link-container > a').get('href')
            yield Request(url=next_page, callback=self.parse_page, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('#topic > #title > a > span').text.strip()
        item['pub_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['images'] = None
        item['body'] = '\n'.join([paragraph.text.strip() for paragraph in soup.select('div.content') if paragraph.text != '' and paragraph.text != ' '])
        item['abstract'] = item['body'].split('\n')[0]
        yield item
