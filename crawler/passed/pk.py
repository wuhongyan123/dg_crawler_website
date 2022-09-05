from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from copy import deepcopy
# 完成
# author:杨洛华
class PkSpider(BaseSpider):
    name = 'pk'
    website_id = 1942
    language_id = 1813
    start_urls = ["http://pk.chineseembassy.org/chn/"]
    is_http = 1

    def parse(self, response):
        meta = response.meta
        categories = response.xpath(".//div[@class='Text_Center']/div[@class='Center_Top']/div[@class='Top_Title']")
        for category in categories:
            category1 = category.xpath("./a/text()").get()
            url = "http://pk.chineseembassy.org/chn" + category.xpath("./a/@href").get().strip('.')
            meta['category1'] = category1
            meta['url'] = url
            yield Request(url=url,callback=self.parse_page, meta=deepcopy(meta))

    def parse_page(self, response):
        meta = response.meta
        url = response.meta['url']
        articles = response.xpath(".//div[@class='Text_Center']/ul/li")
        for article in articles:
            ssd = article.xpath("./text()").get().replace('"','').replace('(','').replace(')','').split('-')
            time = "{}-{}-{}".format(ssd[0],ssd[1],ssd[2]) + " 00:00:00"
            title = article.xpath("./a/text()").get()
            if self.time is None or DateUtil.formate_time2time_stamp(time) >= int(self.time):
                meta['time'] = time
                meta['title'] = title
                yield Request(url=url + article.xpath("./a/@href").get().strip('.'), callback=self.parse_item, meta=deepcopy(meta))
        try:
            for i in range(1,40):
                new_href = 'index_' + str(i) + '.htm'
                yield Request(url=url + new_href, callback=self.parse_page, meta=deepcopy(meta))
        except:
            pass

    def parse_item(self, response):
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['category2'] = None
        item['title'] = response.meta['title']
        item['body'] = ''.join(response.xpath("//*[@id='News_Body_Txt_A']//p/text()").extract())
        item['abstract'] = item['body'].split('\n')[0].strip()
        item['pub_time'] = response.meta['time']
        item['images'] = ["http://pk.chineseembassy.org/chn" + i for i in response.xpath("//*[@id='News_Body_Txt_A']//p//@src").extract()]
        return item

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'pk'])
# execute(['scrapy', 'crawl', 'bmwk','-a', 'db=00', '-a', 'proxy=00','-a','time=days_ago:10'])