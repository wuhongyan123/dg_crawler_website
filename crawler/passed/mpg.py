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

class MpgSpider(BaseSpider):  # author：田宇甲
    name = 'mpg'
    website_id = 1740
    language_id = 1898
    start_urls = ['https://www.mpg.de/newsroom_items/2191/more_items?category=&year=&context=all&limit=10&offset=0']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' #page_content .teaser.teaser-horizontal.noindex'):
            ssd = i.select_one(' .date').text.strip().split(' ')
            time_ = ssd[-1] + '-' + German_month[ssd[1]] + '-' + (ssd[0].strip('.') if int(ssd[0].strip('.')) > 9 else '0' + ssd[0].strip('.')) + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_': time_, 'title_': i.select_one(' .meta-information h3').text.strip().strip('\n'), 'category1_': 'newsroom_items', 'abstract_': i.select_one(' .text-box p').text.strip().strip('\n'), 'images_': ['https://www.mpg.de'+i.img['data-src']]}
                yield Request('https://www.mpg.de'+i.a['href'], callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request(response.url.replace('&offset=' + response.url.split('&offset=')[1], '&offset=' + str(int(response.url.split('&offset=')[1]) + 10)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .content p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = response.meta['images_']
        yield item
