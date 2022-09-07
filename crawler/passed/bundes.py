from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from copy import deepcopy

# author:杨洛华
# 这个网站只有100条左右，而且只有一张图片真是离谱
# check：pys
# pass
class bundesSpider(BaseSpider):
    name = 'bundes'
    website_id = 1752
    language_id = 1898
    start_urls = ["https://www.kulturstiftung-des-bundes.de/de/presse/pressemitteilungen.html"]

    def parse(self, response):
        meta = response.meta
        articles = response.xpath("//*[@id='174468-list']/li")
        for article in articles:
            ssd = article.xpath("./div[1]/span/text()").get().split(".")
            time = "{}-{}-{}".format(ssd[2],ssd[1],ssd[0]) + " 00:00:00"
            title = article.xpath("./div[2]/div/h3/a/span[2]/span/text()").get().replace('\xa0','')
            abstract = article.xpath("./div[2]/div/p/text()").get()
            if self.time is None or DateUtil.formate_time2time_stamp(time) >= int(self.time):
                meta['time'] = time
                meta['title'] = title
                meta['abstract'] = abstract
                yield Request(url="https://www.kulturstiftung-des-bundes.de" + article.xpath("./div[2]/div/h3/a/@href").get(), callback=self.parse_item, meta=deepcopy(meta))

    def parse_item(self, response):
            item = NewsItem()
            item['category1'] ='Pressemitteilung'
            item['category2'] = None
            item['title'] = response.meta['title']
            item['body'] = '\n'.join(response.xpath("//*[@id='inhalt']/div[3]/div/div/div[1]/div/p/text()").extract())
            item['abstract'] = response.meta['abstract']
            item['pub_time'] = response.meta['time']
            item['images'] = ["https://www.kulturstiftung-des-bundes.de" + i for i in response.xpath("//*[@id='inhalt']//div//img/@src").extract()]
            return item
#
# from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'bundes'])
# # execute(['scrapy', 'crawl', 'bmwk','-a', 'db=00', '-a', 'proxy=00','-a','time=days_ago:10'])