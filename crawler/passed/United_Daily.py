# encoding: utf-8
from bs4 import BeautifulSoup

import common.date
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


#Author:陈卓玮
# check: 凌敏 pass
#debug: 增加翻页限制

class UnitedSpider(BaseSpider):
    name = 'UD_news'
    website_id = 178
    language_id = 2266
    start_urls = ['https://weareunited.com.my/author/wkyong/page/1']

    def parse(self, response):#获取新闻列表
        soup=BeautifulSoup(response.text,'lxml')
        for i in soup.select('#content > div > div.row.gridlove-posts > div'):
            time_stamp = self.time_parser(i.select_one('.updated').text)
            title = i.select_one('h2').text
            essay_url= i.select_one('h2 a').get('href')
            abstract = i.select_one('.entry-content').text
            meta={'time':time_stamp,'title':title,'abstract':abstract}
            # print(DateUtil.time_stamp2formate_time(time_stamp))
            yield Request(url = essay_url,callback=self.parse_essay,meta=meta)

        time_stamp = self.time_parser(soup.select_one('#content > div > div.row.gridlove-posts > div .updated').text)##翻页
        if (time_stamp!=None) and (self.time == None or time_stamp >= self.time):
            if "page" not in response.url:
                # print('next_url=>',response.url+"page/2")
                yield Request(url=response.url+"page/2")
            elif int(response.url.split('/page/')[1].strip('/'))< 3708:
                # print('next_url=>',response.url.split('/page/')[0]+"/page/"+str(int(response.url.split('/page/')[1].strip('/'))+1))
                yield Request(url = response.url.split('/page/')[0]+"/page/"+str(int(response.url.split('/page/')[1].strip('/'))+1))

    def parse_essay(self,response):
        soup = BeautifulSoup(response.text,'lxml')

        item = NewsItem()
        item['title'] = response.meta['title']
        item['category1'] = soup.select_one(".entry-category").text
        item['body'] = soup.select_one('.entry-content').text
        item['abstract'] = response.meta['abstract']
        item['pub_time'] = DateUtil.time_stamp2formate_time(response.meta['time'])
        img=[]
        for i in soup.select('img'):
            img.append(i.get('src'))
        item['images'] = img
        # print(item)
        yield item


    def time_parser(self,raw):
        if raw == None:
            return None

        elif 'ago' in raw:
            stamp = DateUtil.formate_time2time_stamp(DateUtil.time_now_formate())
            return stamp

        else:
            raw = raw.split(' ')
            raw = raw[2]+"-"+str(common.date.ENGLISH_MONTH[raw[1].strip(',')])+"-"+raw[0]+" 00:00:00"
            stamp = DateUtil.formate_time2time_stamp(raw)
            return stamp
