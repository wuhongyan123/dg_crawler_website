from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from common import date
from copy import deepcopy


# author : 彭雨胜  review: 凌敏 id问题，已修改
class AcnSpider(BaseSpider):
    name = 'acn'
    website_id = 2088
    language_id = 2181
    start_urls = ['http://www.acn.cu/']
    is_http = 1

    def parse(self, response):
        meta = response.meta
        categories = response.xpath('//li[@class="dropdown mega"]/a')
        for category in categories:
            page_link = 'http://www.acn.cu' + category.xpath('./@href').get()
            category1 = category.xpath('./text()').get().strip()
            meta['data'] = {
                'category1': category1
            }
            yield Request(url=page_link, callback=self.parse_page, meta=deepcopy(meta))

    def parse_page(self, response):
        flag = True
        articles = response.xpath('//div[@class="col-sm-6"]/div/article')
        meta = response.meta
        if self.time is not None:
            last_time = articles[-1].xpath('.//time/@datetime').get().replace('T', ' ')[0:19]
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:
                pub_time = article.xpath('.//time/@datetime').get().replace('T', ' ')[0:19]
                article_url = article.xpath('.//h2[@class="article-title"]/a/@href').get()
                title = article.xpath('.//h2[@class="article-title"]/a/@title').get()
                meta['data']['pub_time'] = pub_time
                meta['data']['title'] = title
                yield Request(url='http://www.acn.cu'+article_url, callback=self.parse_item, meta=deepcopy(meta))
        else:
            flag = False
            self.logger.info("时间截止")
        # 翻页
        if flag:
            if response.xpath('//a[@title="Siguiente"]/@href').get() is None:
                self.logger.info("到达最后一页")
            else:
                next_page = 'http://www.acn.cu' + response.xpath('//a[@title="Siguiente"]/@href').get()
                yield Request(url=next_page, callback=self.parse_page, meta=deepcopy(meta))

    def parse_item(self, response):
        item = NewsItem()
        meta = response.meta
        item['category1'] = meta['data']['category1']
        item['category2'] = None
        item['title'] = meta['data']['title']
        item['pub_time'] = meta['data']['pub_time']
        item['body'] = '\n'.join(
            [paragraph.strip() for paragraph in ["".join(text.xpath('.//text()').getall()) for text in response.xpath(
                '//section[@class="article-content"]/p')] if paragraph.strip() != '' and paragraph.strip() != '\xa0']
        )
        item['abstract'] = item['body'].split('\n')[0]
        item['images'] = ['http://www.acn.cu'+i for i in response.xpath('//section[@class="article-content"]//img/@src').getall()]
        return item
