# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


# author: 张珍珍
class HaniSpider(BaseSpider):
    name = 'hani'
    start_urls = ['https://www.hani.co.kr/arti/list.html']

    website_id = 902
    language_id = 1991

    def parse(self, response):
        flag = True
        if self.time is not None:
            last_time = response.xpath('//div[@class="article-area"]/p/span/text()').get() +':00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= int(self.time):
            article_list = response.xpath('//div[@class="article-area"]')
            for i in article_list:
                url = 'https://www.hani.co.kr' + i.xpath('./h4/a/@href').get()
                category1 = i.xpath('./strong/a/text()').get()
                if category1 == "English Edition":
                    continue
                title = i.xpath('./h4/a/text()').get()
                abstract = i.xpath('./p/a/text()').get()
                pub_time = i.xpath('./p/span/text()').get()
                response.meta['category1'] = category1
                response.meta['title'] = title
                response.meta['abstract'] = abstract
                response.meta['pub_time'] = pub_time
                yield Request(url, callback=self.parse_item, meta=response.meta)
        else:
            self.logger.info("时间截止")
        if flag:
            try:
                next_page = 'https://www.hani.co.kr' + response.xpath('//a[@class="next"]/@href').get()
                yield Request(url=next_page, callback=self.parse, meta=response.meta)
            except:
                self.logger.info("no more pages")

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.meta['title']
        item['abstract'] = response.meta['abstract']
        item['pub_time'] = response.meta['pub_time']
        item['category1'] = response.meta['category1']
        item['category2'] = None
        item['body'] = '\n'.join(['%s' % i.xpath('normalize-space(string(.))').get() for i in
                                  response.xpath('//div[@class="subtitle"] | //div[@class="text"]')])
        try:
            item['images'] = ['https:' + i.xpath('./@src').get() for i in response.xpath('//div[@class="image"]/img')]
        except:
            item['images'] = ''
        yield item