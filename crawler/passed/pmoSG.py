# encoding: utf-8
from bs4 import BeautifulSoup

import common.date
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


#Author:陈卓玮
# check: 凌敏 有id错误，已改 pass
class pmoSGSpider(BaseSpider):
    name = 'pmoSG'
    website_id = 456
    language_id = 1866
    start_urls = ['https://www.pmo.gov.sg/Topics']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        for i in soup.select('#block-system-main > div > div'):
            yield Request(url="https://www.pmo.gov.sg" + i.select_one('a').get('href')
                          ,callback=self.parsepages)
    def parsepages(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        for k in soup.select('.topic-item'):
            title = (k.select_one('.gamma').text)#标题
            time = self.format_time(k.select_one('.ti-date').text)#时间
            category=soup.select_one('title').text.split(' | ')[1]#类别
            try:
                essay_url = ("https://www.pmo.gov.sg" + k.select_one('a').get('href'))#页面
                meta = {'title':title,
                        'time':time,
                        'category':category}
                yield Request(url = essay_url,callback=self.parse_essay,meta=meta)
            except:
                pass

        time_stamp = DateUtil.formate_time2time_stamp(time)
        if(self.time == None or int(time_stamp) >= self.time):
            try:
                yield Request(url = response.url.split('?')[0] + soup.select_one('.next a').get('href')
                              ,callback=self.parsepages)#翻页
            except:
                pass
    def parse_essay(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        meta = response.meta

        body=''
        for i in soup.select('p'):
            body+=i.text + '\n'
        img=[]
        for i in soup.select('img'):
            img.append("https://www.pmo.gov.sg/" + i.get('src'))
        item = NewsItem()
        item['title'] = meta['title']
        item['category1'] = meta['category']
        item['body'] = body.replace(" ",'')
        item['abstract'] = body.replace(" ",'').split('\n')[0]+body.replace(" ",'').split('\n')[1]
        item['pub_time'] = meta['time']
        item['images'] = img
        # print(item)
        yield item


    def format_time(self,raw):
        raw = raw.split(' ')
        day = raw[0]
        month = str(common.date.ENGLISH_MONTH[raw[1]])
        year = raw[2]
        return year+"-"+month+"-"+day+" 00:00:00"