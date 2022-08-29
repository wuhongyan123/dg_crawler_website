from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from copy import deepcopy

# author:杨洛华
# check：pys
# pass
German_MONTH = {
        'Januar': '01',
        'Februar': '02',
        'März': '03',
        'April': '04',
        'Mai': '05',
        'Juni': '06',
        'Juli': '07',
        'August': '08',
        'September': '09',
        'Oktober': '10',
        'November': '11',
        'Dezember': '12'
}
class DfgSpider(BaseSpider):
    name = 'dfg'
    website_id = 1735
    language_id = 1898
    start_urls = ["https://www.dfg.de/service/presse/pressemitteilungen/2022/",
                  "https://www.dfg.de/service/presse/pressemitteilungen/2021/",
                  "https://www.dfg.de/service/presse/pressemitteilungen/2020/",
                  "https://www.dfg.de/service/presse/pressemitteilungen/2019/",]

    def parse(self, response):
        meta = response.meta
        articles = response.xpath(".//div[@class='pmUebersicht']/ul/li")
        for article in articles:
            ssd = article.xpath("./h3/text()[2]").get().split("|")[1].split(' ')
            time = "{}-{}-{}".format(ssd[3],German_MONTH[ssd[2]],ssd[1].strip('.')) + " 00:00:00"
            title = article.xpath("./h3/a/text()").get()
            if self.time is None or DateUtil.formate_time2time_stamp(time) >= int(self.time):
                meta['time'] = time
                meta['title'] = title
                yield Request(url="https://www.dfg.de/service/presse/pressemitteilungen/" + ssd[3] + '/' + article.xpath("./h3/a/@href").get(), callback=self.parse_item, meta=deepcopy(meta))

    def parse_item(self, response):
            item = NewsItem()
            item['category1'] ='Pressemitteilung'
            item['category2'] = None
            item['title'] = response.meta['title']
            item['body'] = ''.join(response.xpath(".//div[@class='row bab-modul-fliesstext']/div/p//text()").extract())
            item['abstract'] = item['body'].split('\n')[0]
            item['pub_time'] = response.meta['time']
            return item

# from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'dfg'])
# execute(['scrapy', 'crawl', 'bmwk','-a', 'db=00', '-a', 'proxy=00','-a','time=days_ago:10'])
# 没有图片