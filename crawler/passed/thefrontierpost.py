import re

from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author : 李玲宝
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
# 新闻量小（20左右），网站本来就没有二级标题
# check:凌敏 pass
class ThefrontierpostSpider(BaseSpider):
    name = 'thefrontierpost'
    website_id = 2105
    language_id = 1866
    start_urls = ['https://thefrontierpost.com/category/global/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        category1 = soup.select('#categories-3>ul a')
        for i in category1:
            url = i['href'] + 'page/'
            yield scrapy.Request(url + '1/', callback=self.parse_page, meta={'category1': i.text.strip(), 'url': url, 'page': 1})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('.vce-loop-wrap article')
        t = re.search('loads/\d{4}/\d{2}', block[-1].select_one('img')['src'])
        if self.time is not None and t:
            last_time = t.group().replace('/', '-') + '-01 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                yield Request(i.select_one('a')['href'], callback=self.parse_item, meta=response.meta)
        if soup.select_one('#vce-pagination') is not None:
            response.meta['page'] += 1
            yield Request(response.meta['url'] + str(response.meta['page']) + '/', callback=self.parse_page, meta=response.meta)
        else:
            self.logger.info("时间截止")

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.select_one('.entry-content') is not None:
            item = NewsItem()
            item['category1'] = response.meta['category1']
            item['title'] = soup.select_one('h1').text.strip()
            item['pub_time'] = soup.select_one("meta[property='article:published_time']")['content'][:10] + ' 00:00:00'
            item['images'] = [img.get('src') for img in soup.select('#main>article img')]
            item['body'] = '\n'.join(i.strip() for i in soup.select_one('.entry-content').text.split('\n') if i.strip() != '')
            item['abstract'] = item['body'].split('\n')[0]
            return item
