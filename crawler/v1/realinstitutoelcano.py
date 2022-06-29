from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from copy import deepcopy


# v1Author: 曾嘉祥
# v2Author: 彭雨胜
class RealinstitutoelcanoSpider(BaseSpider):
    name = 'realinstitutoelcano'
    website_id = 792
    language_id = 2181
    start_urls = ['https://www.realinstitutoelcano.org']

    def parse(self, response):
        meta = response.meta
        categories = response.xpath('//*[@id="secondary-menu"]/li[1]/div/ul/li/a')

        for category in categories:
            page_link = category.xpath('./@href').get()
            category1 = category.xpath('./text()').get()
            meta['data'] = {
                'category1': category1
            }
            yield Request(url=page_link, callback=self.parse_page, meta=deepcopy(meta))

    def parse_page(self, response):
        flag = True
        meta = response.meta
        articles = response.xpath('//*[@class="the-archive the-archive--category maincol maincol--medium"]/article')

        if self.time is not None:
            t = articles[-1].xpath('.//time[@class="entry-date published"]/@datetime').get()
            last_time = t.replace('T', ' ').replace('Z', '').split('+')[0]

        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:
                tt = article.xpath('.//time[@class="entry-date published"]/@datetime').get()
                pub_time = tt.replace('T', ' ').replace('Z', '').split('+')[0]
                article_url = article.xpath('.//h2[@class="entry-title"]/a/@href').get()
                title = article.xpath('.//h2[@class="entry-title"]/a/text()').get()
                meta['data']['category2'] = article.xpath('.//div[@class="post-type"]/text()').get()
                meta['data']['title'] = title
                meta['data']['pub_time'] = pub_time
                meta['data']['article_url'] = article_url
                yield Request(url=article_url, callback=self.parse_item, meta=deepcopy(meta))
        else:
            flag = False
            self.logger.info("时间截止")

        if flag:
            if response.xpath('//a[@class="next page-numbers"]/@href').get() is None:
                self.logger.info("到达最后一页")
            else:
                next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
                yield Request(url=next_page, callback=self.parse_page, meta=deepcopy(meta))

    def parse_item(self, response):
        if response.xpath('//iframe[@class="code-iframe"]').get() is not None:
            return
        else:
            item = NewsItem()
            meta = response.meta
            item['category1'] = meta['data']['category1']
            item['category2'] = meta['data']['category2']
            item['title'] = meta['data']['title']
            item['pub_time'] = meta['data']['pub_time']

            item['body'] = '\n'.join(
                [paragraph.strip() for paragraph in ["".join(text.xpath('.//text()').getall()) for text in response.xpath(
                    '//div[@class="columns"]/div//p | //main[@class="site-main"]/article/div//p | //div[@class="mj-column-per-100 outlook-group-fix"]//p | //ol[@dir="ltr"]//li')]]
            )

            item['abstract'] = item['body'].split('\n')[0]
            item['images'] = response.xpath('//main[@class="site-main"]/article//img/@src').getall()
            return item
