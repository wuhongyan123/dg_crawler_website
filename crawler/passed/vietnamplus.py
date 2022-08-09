from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
import re
import time

# 以下的头文件不要修改
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil

#author:陈麒亦
# check：凌敏 pass
class vietnamplusSpider(BaseSpider):
    name = 'vietnamplus'
    website_id = 240 # 网站的id(必填)
    language_id = 2242 # 所用语言的id
    start_urls = ['https://www.vietnamplus.vn/api/menu.html']


    def parse(self,response):
        catagory=response.xpath("//ul[@class='site-menu']/li/a/@href").extract()
        for i in catagory[2:]:
            if "//" not in i:
                yield Request(url="https://www.vietnamplus.vn"+i,callback=self.parse2)
        pass

    def parse2(self,response):
        articles=response.xpath("//div[@class='clearfix']/article")
        for i in articles:
            if i.xpath(".//time/text()"):
                time0=time.strptime(i.xpath(".//time/text()").extract()[0].strip(),"%d/%m/%Y - %H:%M")
                time1 = time.mktime(time0)
                if self.time is None or int(time1) >= int(self.time):
                    yield Request(url="https://www.vietnamplus.vn"+i.xpath("./a[1]/@href").extract()[0],callback=self.parse3, meta={'date':time0})
        if response.xpath("//span[@id='mainContent_ContentList1_pager']/ul/li[@class='active']/following-sibling::li[1]"):

            yield Request(url="https://www.vietnamplus.vn"+response.xpath("//span[@id='mainContent_ContentList1_pager']/ul/li[@class='active']/following-sibling::li[1]/a/@href").extract()[0],callback=self.parse2)


    def parse3(self,response):
        item = NewsItem()
        if(response.xpath("//h1/text()")):
            item['title']=response.xpath("//h1/text()").extract()[0]
        if(response.xpath("//div[@class='direction']/a[1]/text()")):
            item['category1'] = response.xpath("//div[@class='direction']/a[1]/text()").extract()[0].strip()
        item['category2'] = ''
        item['body'] = "".join(response.xpath("//div[contains(@class,'article-body')]/p").xpath("string(.)").extract())
        if(response.xpath("//div[contains(@class,'details__summary')]/text()")):
            item['abstract'] = response.xpath("//div[contains(@class,'details__summary')]/text()").extract()[0].strip()
        item['pub_time'] = response.meta['date']
        item['images'] = response.xpath("//div[contains(@class,'article-body')]//img/@src").extract()
        yield item

