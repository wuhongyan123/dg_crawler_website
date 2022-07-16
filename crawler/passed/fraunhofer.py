from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

German_month = {
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

class FraunhoferSpider(BaseSpider):  # author：田宇甲
    name = 'fraunhofer'
    website_id = 1740 # 这个id里有很多个网站
    language_id = 1898
    start_urls = ['https://www.fraunhofer.de/de/presse-newsroom/jcr:content/contentPar/sectioncomponent/sectionParsys/newsroom.items.html?ipp=15&cp=1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .filterpage-results.articles-list .fhg-article-in-list'):
            ssd = i.select_one(' p .date').text.strip().split(' ')
            time_ = ssd[-1] + '-' + German_month[ssd[1]] + '-' + ssd[0].strip('.') + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_': time_, 'title_': i.h3.text.strip().strip('\n'), 'category1_': 'newsroom', 'abstract_': i.select_one(' .text p').text.strip().strip('\n'), 'images_': ('https://www.fraunhofer.de'+i.img['src'] if 'figure' in str(i) else '')}
                yield Request('https://www.fraunhofer.de'+i.a['href'], callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request(response.url.replace('&cp=' + response.url.split('&cp=')[1], '&cp=' + str(int(response.url.split('&cp=')[1]) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .fhg-content.fhg-richtext p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = [response.meta['images_']]
        yield item
