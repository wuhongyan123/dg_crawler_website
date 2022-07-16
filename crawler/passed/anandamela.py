from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

ENGLISH_MONTH = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

# author : 李玲宝
# check: 凌敏 pass
class AnandamelaSpider(BaseSpider):
    name = 'anandamela'
    website_id = 1897
    language_id = 1779
    proxy = '02'
    start_urls = ['https://api.anandamela.in/api/jsonws/contentservice.content/navigation']

    def parse(self, response):
        menu = response.json()
        for i in menu:
            for j in i.get('childMenus'):
                url = 'https://api.anandamela.in/api/jsonws/contentservice.content/Section-other-stories/category-id/' + j.get('categoryId') + '/start/0/end/100000'
                yield scrapy.Request(url, callback=self.parse_page, meta={'category1': i['nameCurrentValue'], 'category2': j['nameCurrentValue']})

    def parse_page(self, response):
        article = response.json()
        if self.time is not None:
            t = article[-1].get('dateString').split(' ')
            last_time = f'{t[-1]}-{ENGLISH_MONTH[t[1]]}-{t[2][:-1]}' + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in article:
                tt = i.get('dateString').split(' ')
                response.meta['pub_time'] = f'{tt[-1]}-{ENGLISH_MONTH[tt[1]]}-{tt[2][:-1]}' + ' 00:00:00'
                yield scrapy.Request('https://api.anandamela.in/api/jsonws/contentservice.content/get-story/article-id/' + i['link'], callback=self.parse_item, meta=response.meta)

    def parse_item(self, response):
        article = response.json()
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['category2'] = response.meta['category2']
        item['title'] = article['title']
        item['pub_time'] =  response.meta['pub_time']
        item['images'] = ['https://api.sananda.in/image/journal/article?img_id=' + article['imageId']] if article['image'] else []
        soup = BeautifulSoup(article['body'], 'html.parser')
        item['body'] = '\n'.join(i.text.strip() for i in soup.select('p') if i.text.strip() != '')
        item['abstract'] = item['body'].split('\n')[0]
        return item
