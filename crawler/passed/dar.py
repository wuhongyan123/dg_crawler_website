from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import json

# check: 魏芃枫
class darSpider(BaseSpider):  # author：田宇甲 我喂自己袋盐 这个爬虫用时25分42秒，打破自己速通记录
    name = 'dar'
    website_id = 1273
    language_id = 1866
    start_urls = ['https://www.dar.gov.ph/articles/news/index.json?p=1']
    proxy = '02'

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in json.loads(soup.text)['articles']:
            if self.time is None or DateUtil.formate_time2time_stamp(i['publishedOn']['timeStamp']['iso']) >= int(self.time):
                meta = {'pub_time_': i['publishedOn']['timeStamp']['iso'], 'title_': i['contents'][0]['title'], 'abstract_': i['contents'][0]['excerpt'], 'images_': i['metadata']['featured-image'], 'category1_': 'News'}
                yield Request('https://www.dar.gov.ph/articles/news/'+str(i['contents'][0]['articleId']), callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(i['publishedOn']['timeStamp']['iso']) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            yield Request(response.url.replace(response.url.split('p=')[1], str(int(response.url.split('p=')[1])+1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = soup.select_one(' .article-content').text.strip().strip('\n')
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = response.meta['images_']
        yield item
