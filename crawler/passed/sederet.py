
from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import time


# author : 胡楷
# check； pys  pass
class SederetSpider(BaseSpider):
    name = 'sederet'
    website_id = 63
    language_id = 1866
    allowed_domains = ['www.sederet.com']
    start_urls = ['https://www.sederet.com']
    # proxy = '02'


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        categories = soup.select('#menu_container > ul > li > a')[2:]
        for category in categories:
            category_url = category.get('href')
            meta = {'category1': category.text}
            yield Request(url=category_url, callback=self.parse_page, meta=meta)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.select('div.article_content > ul > li > a')
        flag = True
        if self.time is not None:
            last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:
                article_url = article.get('href')
                yield Request(url=article_url, callback=self.parse_item, meta=response.meta)
        else:
            flag = False
            self.logger.info("时间截止")
        if flag:
            pass

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('#content_left_container > h1.article_title').text.strip()
        item['pub_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #无pub_time用爬取时间替代
        imgs = [img.get('src') for img in soup.select('#content_left_container img')]
        if imgs == None:
            item['images'] = None
        else:
            item['images'] = imgs
        item['body'] = '\n'.join([paragraph.text.strip() for paragraph in soup.select('div.article_content > p') if paragraph.text != '' and paragraph.text != ' '])
        item['abstract'] = item['body'].split('\n')[0]
        yield item