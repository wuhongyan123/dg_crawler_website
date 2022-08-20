from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup
import re

# author : 李玲宝
# 网站的新闻本来就没有二级标题
# check：凌敏 pass
class CpecSpider(BaseSpider):
    name = 'cpec'
    website_id = 2114
    language_id = 1866
    is_http = 1
    start_urls = ['http://cpec.gov.pk']

    def parse(self, response):
        urls = ['http://cpec.gov.pk/all-events?page=', 'http://cpec.gov.pk/press-releases?page=']  # 只有这2个目录有新闻
        for i in urls:
            yield scrapy.Request(i + '1', callback=self.parse_page, meta={'url': i, 'page': 1})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('#posts .entry')
        if self.time is not None:
            t = re.search('\d{2}-\d{2}-\d{4}', block[-1].select_one('img')['src']).group()
            last_time = f"{t[6:]}-{t[3:5]}-{t[:2]}" + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                tt = re.search('\d{2}-\d{2}-\d{4}', i.select_one('img')['src'])
                if tt:
                    response.meta['pub_time'] = f"{tt.group()[6:]}-{tt.group()[3:5]}-{tt.group()[:2]}" + ' 00:00:00'
                    if i.select_one('.btn-danger') is not None:
                        url = i.select_one('.btn-danger')['href']
                        response.meta['category1'] = 'events'
                    else:
                        url = i.select_one('h5>a')['href']
                        response.meta['category1'] = 'press-releases'
                    if url != '':
                        response.meta['images'] = [i.select_one('img')['src']]
                        yield Request(url, callback=self.parse_item, meta=response.meta)
        if soup.select_one('a[rel="next"]') is not None:
            response.meta['page'] += 1
            yield Request(response.meta['url'] + str(response.meta['page']), callback=self.parse_page, meta=response.meta)
        else:
            self.logger.info("时间截止")

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.select_one('.entry') is not None:
            item = NewsItem()
            item['category1'] = response.meta['category1']
            item['title'] = soup.select_one('h3').text.strip()
            item['pub_time'] = response.meta['pub_time']
            item['images'] = response.meta['images']
            item['body'] = '\n'.join(i.strip() for i in soup.select_one('.entry').text.split('\n') if i.strip() != '')
            item['abstract'] = item['body'].split('\n')[0]
            return item
