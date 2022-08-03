# encoding: utf-8
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author: robot_2233

class EuropaeuSpider(BaseSpider):
    name = 'europaeu'
    website_id = 1719
    language_id = 1898
    start_urls = ['https://europa.eu/newsroom/press-releases/last-thirty-days_de']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' #block-system-main .view-content .views-row'):
            time_ = str(i.select_one(' .day')).split('content="')[1].split('">')[0].split('+')[0].replace('T',' ')
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                ddd=i.a['href']
                meat = {'title_': i.h4.text.strip('\n'), 'time_': time_, 'category1_': 'press-releases', 'abstract_': i.select_one(' .field-content').text.strip()}
                if 'consilium' in i.a['href']:
                    yield Request(i.a['href'], callback=self.parse_item, meta=meat)
                elif '_22_' in i.a['href']:
                    if '/de/' in i.a['href']:
                        yield Request('https://ec.europa.eu/commission/presscorner/api/documents?reference='+i.a['href'].split('/de/')[1].replace('_','/')+'&language=en', callback=self.api_item, meta=meat)
                    elif '/en/' in i.a['href']:
                        yield Request('https://ec.europa.eu/commission/presscorner/api/documents?reference='+i.a['href'].split('/en/')[1].replace('_','/')+'&language=en', callback=self.api_item, meta=meat)
                else:
                    pass
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):  # 这里的time_为上面for循环的最后一个时间戳，用于下面翻页检索
            if 'page' not in response.url:
                yield Request('https://europa.eu/newsroom/press-releases/last-thirty-days_de?page=1')
            else:
                yield Request(response.url.replace('?page=' + response.url.split('?page=')[1], '?page=' + str(int(response.url.split('?page=')[1]) + 1)))

    def parse_item(self, response):
        try:
            item = NewsItem()
            soup = BeautifulSoup(response.text, 'html.parser')
            item['title'] = response.meta['title_']
            item['category1'] = response.meta['category1_']
            item['category2'] = None
            item['body'] = '\n'.join([i.text for i in soup.select(' .row.council-flexify p')])
            item['abstract'] = soup.select_one(' .row.council-flexify p').text
            item['pub_time'] = response.meta['time_']
            item['images'] = []
            yield item
        except:  # 有的挂羊头卖狗肉
            pass

    def api_item(self, response):
        try:
            item = NewsItem()
            soup = BeautifulSoup(response.json()['docuLanguageResource']['htmlContent'], 'html.parser')
            item['title'] = response.meta['title_']
            item['category1'] = response.meta['category1_']
            item['category2'] = None
            item['body'] = '\n'.join([i.text for i in soup.select('p')])
            item['abstract'] = soup.select_one(' p').text
            item['pub_time'] = response.meta['time_']
            item['images'] = []
            yield item
            yield item
        except:  # 有的挂羊头卖狗肉
            pass
