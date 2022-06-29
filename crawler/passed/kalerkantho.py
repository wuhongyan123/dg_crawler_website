from bs4 import BeautifulSoup
from crawler.items import *
from crawler.spiders import BaseSpider
from scrapy.http.request import Request
from utils.date_util import DateUtil
import re


ENGLISH_MONTH = {
        'জানুয়ারি': '01',
        'ফেব্রুয়ারি': '02',
        'মার্চ': '03',
        'এপ্রিল': '04',
        'মে': '05',
        'জুন': '06',
        'জুলাই': '07',
        'আগস্ট': '08',
        'সেপ্টেম্বর': '09',
        'অক্টোবর': '10',
        'নভেম্বর': '11',
        'ডিসেম্বর': '12'}



#author:黄锦荣
# check：凌敏 会报403
class kalerkanthoSpider(BaseSpider):
    name = 'kalerkantho'
    website_id = 1924
    language_id = 1799
    start_urls = [
        'https://www.kalerkantho.com/online/national/1',
        'https://www.kalerkantho.com/online/country-news/1',
        'https://www.kalerkantho.com/online/world/1',
        'https://www.kalerkantho.com/online/entertainment/1',
        'https://www.kalerkantho.com/online/sport/1',

                  ]
    page = 0
    # is_http = 1

    def parse(self, response):
        # for i in soup.select('  section div article'):
        article_list = response.xpath('/html/body/div/div/div/div[@class="col-xs-12 col-sm-6 col-md-6 n_row"]')
        for i in article_list:
            year = i.xpath('./a/@href').get().split('/')[3]
            month= i.xpath('./a/@href').get().split('/')[4]
            day=i.xpath('./a/@href').get().split('/')[5]
            time_= year+'-'+month+'-'+day+' 00:00:00'
            title_ =i.xpath('./a/text()').get()
            # print(time_)
            abstract_=i.xpath('.//p/text()').get()
            # print(abstract_)
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_':time_,'title_':title_,'category1_':response.url.split('online/')[1].split('/')[0],
                        'abstract':abstract_}
                # print(response.url)
                yield Request(url="https://www.kalerkantho.com/" + i.xpath('.//a/@href').get()[1:], callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            if 'national' not in response.url:
                yield Request(response.url + '/page/2', callback=self.parse, meta=meta)
            else:
                # print(response.url)
                yield Request(response.url.replace(response.url.split('national/')[1],
                                               str(int(response.url.split('national/')[1]) + 18)),
                                 callback=self.parse, meta=response.meta)


    def parse_item(self, response):

        item = NewsItem()
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = response.xpath('/html/body/div/div/div/p/text()').get()
        item['abstract'] = response.meta['abstract']
        item['pub_time'] = response.meta['pub_time_']
        try:
            img = response.xpath('//body/div/div/div/img/@src').get()
            item['images'] = img
        except:
            item['images'] = []
        yield item