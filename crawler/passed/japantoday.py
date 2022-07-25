
from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import time


# author : 胡楷
class JapantodaySpider(BaseSpider):
    name = 'japantoday'
    website_id = 1982
    language_id = 1866
    allowed_domains = ['japantoday.com']
    start_urls = ['https://japantoday.com']


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        categories = soup.select('nav.sidenav-list.bg-gray-darker > ul a')[1:]
        del categories[21]
        del categories[15:22]
        del categories[10]
        for category in categories:
            category_url = 'https://japantoday.com' + category.get('href')
            meta = {'category1': category.text}
            yield Request(url=category_url, callback=self.parse_page, meta=meta)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.select('div.media-body > h3 > a')
        flag = True
        if self.time is not None:
            last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:
                article_url = 'https://japantoday.com' + article.get('href')
                yield Request(url=article_url, callback=self.parse_item, meta=response.meta)
        else:
            flag = False
            self.logger.info("时间截止")
        if flag:
            next_ = soup.select_one('nav.text-right.text-strong.mb-40 > a.text-primary.text-italic.font-playfair.space-left')
            if  next_ == None:
                pass
            else:
                next_page = next_.get('href')
                yield Request(url='https://japantoday.com' + next_page, callback=self.parse_page, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('article h1').text.strip()
        tt = soup.select_one('div.text-strong.text-xsmall.text-gray > time')
        item['pub_time'] = tt.get('datetime').replace('T',' ').replace('+09:00','')
        imgs = [img.get('src') for img in soup.select('article > figure > img')]
        if imgs == None:
            item['images'] = None
        else:
            item['images'] = imgs
        item['body'] = '\n'.join([paragraph.text.strip() for paragraph in soup.select('div.text-large.mb-40 > p') if paragraph.text != '' and paragraph.text != ' '])
        item['abstract'] = item['body'].split('\n')[0]
        yield item


