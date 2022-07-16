from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author:李玲宝
# check: 凌敏 pass 此网站语言为英语
# 我爬的是那个“乌尔都语”文档的网站，对接的同学说审核爬虫的人填id,那个id是我乱填的（不填会报错）
# 网站本来就没有二级标题
class PakistaneconomicnetSpider(BaseSpider):
    name = 'pakistaneconomicnet'
    website_id = 2094
    language_id = 1866
    start_urls = ['https://pakistaneconomicnet.com']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        category1 = soup.select('#main-navigation a')[2:-1]
        for i in category1:
            url = i['href'] + 'page/'
            yield scrapy.Request(url + '1/', callback=self.parse_page, meta={'category1': i.text.strip(), 'url': url, 'page': 1})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('.listing-blog article')
        if self.time is not None:
            last_time = block[-1].select_one('.listing-blog article time')['datetime'][:10] + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                response.meta['pub_time'] = soup.select_one('.listing-blog article time')['datetime'][:10] + ' 00:00:00'
                yield Request(i.select_one('a.post-title')['href'], callback=self.parse_item, meta=response.meta)
        if soup.select_one('.col-sm-8 a.btn-bs-pagination') is not None:
            response.meta['page'] += 1
            url = response.meta['url'] + str(response.meta['page']) + '/'  # 页码+1后的url
            yield Request(url, callback=self.parse_page, meta=response.meta)
        else:
            self.logger.info("时间截止")

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['title'] = soup.select_one('h1.single-post-title').text.strip()
        item['pub_time'] = response.meta['pub_time']
        item['images'] = [img.get('data-src') for img in soup.select('article img')]
        item['body'] = '\n'.join(i.text.strip() for i in soup.select('.continue-reading-content p') if i.text.strip() != '')
        item['abstract'] = item['body'].split('\n')[0]
        return item
