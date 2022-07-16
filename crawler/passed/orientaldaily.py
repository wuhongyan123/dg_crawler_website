# encoding: utf-8

from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from common.header import MOZILLA_HEADER
from common import date
import re

# author: 华上瑛
class OrientaldailySpider(BaseSpider):
    name = 'orientaldaily'
    website_id = 143
    language_id = 2266
    start_urls = ['https://www.orientaldaily.com.my/news/nation',
                  'https://www.orientaldaily.com.my/news/international',
                  'https://www.orientaldaily.com.my/news/business',
                  'https://www.orientaldaily.com.my/news/society',
                  'https://www.orientaldaily.com.my/news/entertainment',
                  'https://www.orientaldaily.com.my/news/local',
                  'https://www.orientaldaily.com.my/news/features',
                  'https://www.orientaldaily.com.my/news/columns',
                  'https://www.orientaldaily.com.my/news/lifestyle',
                  'https://www.orientaldaily.com.my/news/sports',
                  'https://www.orientaldaily.com.my/news/funnews',
                  'https://www.orientaldaily.com.my/news/advertorial',
                  ]
    proxy = '02'

    # custom_settings = {"DEFAULT_REQUEST_HEADERS": MOZILLA_HEADER,"proxy":'02'}

    def parse(self, response):
        for i in self.start_urls:
            flag = True
            category1 = i.split('/')[-1]
            soup = BeautifulSoup(response.text, 'lxml')
            articles = soup.select('div.col-12.col-md-7.col-lg-8 > div.news-item')
            if self.time is not None:
                last_time = articles[-1].select('div.info > span > time')[0].get('datetime')
            if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
                for article in articles:
                    href = article.select('a.link')[0].get('href')
                    yield Request(url=href, callback= self.parse_item, meta={'category1': category1})
            else:
                flag = False
                self.logger.info("时间截止")
            if flag:
                if soup.find_all('a',rel='next')[0].get('href') == None:
                    self.logger.info("no more pages")
                else:
                    next_page = soup.find_all('a',rel='next')[0].get('href')
                    yield Request(url=next_page, callback=self.parse, meta={'category1': category1})

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        content = soup.select('div.col-12.col-md-5.col-lg-8')[0]

        item['title'] = content.select('.article-info.my-3.px-3.px-md-0 > div > h1')[0].text
        try:
            item['images'] = [content.select('.billboard > figure > img')[0].get('src')]
        except:
            item['images'] = []

        time = content.select('.article-info.my-3.px-3.px-md-0 > div > div > span')[0].text.strip()
        pub_time = re.findall(r'[0-9]+', time)
        item['pub_time'] = '{}-{}-{} {}:{}:{}'.format(pub_time[0],pub_time[1],pub_time[2],pub_time[3],pub_time[4],'00')

        # body_ = content.select('.article.article-primary.story > p')
        body_t = content.find_all('div',itemprop='articleBody')[0]
        body_ = body_t.select('p')
        body = ''
        for b in body_:
            body += b.text.strip()

        if body==" ":
            print(response.url)
        item['body'] = body

        item['abstract'] = list(body.split('。'))[0]
        item['category1'] = response.meta['category1']
        item['category2'] = ''
        yield item



