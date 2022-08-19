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
class vneconomySpider(BaseSpider):
    name = 'vneconomy'
    website_id = 249  # 网站的id(必填)
    language_id = 2242 # 所用语言的id
    start_urls = ['http://vneconomy.vn/']


    def parse(self,response):
        catagory=response.xpath("//ul[@class='nav']/li//a")
        for i in catagory[2:-1]:
            if "//" not in i.xpath("./@href").extract()[0]:
                yield Request(url="https://vneconomy.vn"+i.xpath("./@href").extract()[0]+"?trang=1",callback=self.parse2,meta={"category1":i.xpath("./@title").extract()[0]})
        pass

    def parse2(self, response):
        if response.xpath("//div[@class='col-12 col-lg-9 column-border']/article"):
            articles = response.xpath("//div[@class='col-12 col-lg-9 column-border']/article")
            for i in articles:
                time0 = time.strptime(i.xpath(".//div[@class='story__meta']/time/text()").extract()[0].strip(), "%d/%m/%Y")
                time1 = time.mktime(time0)
                if self.time is None or int(time1) >= int(self.time):
                    yield Request(url="https://vneconomy.vn" + i.xpath("./figure/a[1]/@href").extract()[0],
                                  callback=self.parse3,meta={"date": time0,"category1":response.meta["category1"]})
            yield Request(
                url=response.url.replace("trang=" + str(response.meta['depth']), "trang=" + str(response.meta['depth'] + 1)),
                callback=self.parse2, meta={"category1":response.meta["category1"]})
        else:
            return


    def parse3(self,response):
        # print(response)
        item = NewsItem()
        if(response.xpath("//h1/text()")):
            item['title']=response.xpath("//h1/text()").extract()[0]
        item['category1'] = response.meta['category1']
        item['category2'] = ''
        item['body'] = "".join(response.xpath("//div[@class='detail__content']/p/following-sibling::p").xpath("string(.)").extract())
        if(response.xpath("//div[@class='detail__content']/p[1]")):
            item['abstract'] = response.xpath("//div[@class='detail__content']/p[1]").xpath("string(.)").extract()[0].strip()
        item['pub_time'] = response.meta['date']
        item['images'] = response.xpath("//figure[@class='detail__avatar']/img/@src").extract()
        yield item
