# encoding: utf-8
from bs4 import BeautifulSoup

import common.date
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


#Author:陈卓玮
# check；凌敏 pass
class CHNSGSpider(BaseSpider):
    name = 'CHNSG'
    website_id = 438
    language_id = 2266
    start_urls = ['http://www.chinaembassy.org.sg/chn/','http://sg.china-embassy.gov.cn/chn']
    is_http = 1

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.select('.nbox_more a'):
            yield Request(url="http://sg.china-embassy.gov.cn/chn" + i.get('href') +"index.htm",
                          callback=self.parselist)

    def parselist(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.select('#docMore li'):

            if "http" not in i.select_one('a').get('href').strip('.'):
                url = response.url.split('/index')[0]+i.select_one('a').get('href').strip('.')
                # print("PAGES=>URL=>",url)
            else:
                url=i.select_one('a').get('href').strip('.')

            time = i.text.replace(i.select_one('a').text, '')+" 00:00:00"

            if len(time) < 10:
                time = DateUtil.time_now_formate()
            time_stamp = DateUtil.formate_time2time_stamp(time.replace("（",'').replace("）",''))

            title = i.select_one('a').text
            meta={'time':time.replace("（",'').replace("）",''),'title':title,'category':soup.select_one('title').text.split(' — ')[0]}
            yield Request(url=url,callback=self.parse_essay,meta=meta)

        count_page = int(soup.select_one('#pages script').text.split("//共多少页")[0].split('var ')[-1].split('= ')[-1])#总页数
        current_page =int(soup.select_one('#pages script').text.split("//共多少页")[0].split('var ')[1].split(';')[0].split('= ')[1])



        if (current_page < count_page) and (self.time == None or int(time_stamp) >= self.time):
            # print("正在翻页,url=>",response.url.split('/index')[0]+"/index_"+str(current_page+1)+".htm")
            yield Request(url=response.url.split('/index')[0]+"/index_"+str(current_page+1)+".htm",callback=self.parselist)


    def parse_essay(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        meta=response.meta

        body=''
        img=[]

        for i in soup.select('#article p'):
            body+=i.text
        for i in soup.select('#article img'):
            img.append(str(response.url.split('/t')[0] + i.get('src').strip('.')))

        time = soup.select_one('#News_Body_Time').text+":00"
        if len(time)<4:
            time = DateUtil.time_now_formate()

        item = NewsItem()
        item['title'] = str(meta['title'])
        item['category1'] = str(meta['category'])
        item['body'] = str(body)
        item['abstract'] = str(body.split('\n')[0])
        item['pub_time'] = time
        item['images'] = img
        yield item
