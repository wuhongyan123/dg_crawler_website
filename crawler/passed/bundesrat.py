from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
# check:wpf pass
class BundesratSpider(BaseSpider):  # author：田宇甲
    name = 'bundesrat'  # 有点慢
    website_id = 1693
    language_id = 1898
    start_urls = ['https://www.bundesrat.de/SiteGlobals/Forms/Suche/Archiv/Pressemitteilungen/Archiv-Pressemitteilungen-Formular.html?input_=4969072&a_search=Suchbegriff&submit=%E5%AF%BB%E6%89%BE&resourceId=4732152&pageLocale=de&gtp=4732264_list%253D1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .result-list li'):
            sssd = i.h2.em.extract()
            ssd = sssd.text.strip().split('|')[1].strip().split('.')
            time_ = ssd[-1] + '-' + ssd[1] + '-' + ssd[0] + ' 00:00:00'
            if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
                meta = {'pub_time_': time_, 'title_': i.h2.text.strip().strip('\n'), 'category1_': 'Pressemitteilungen', 'images_': [], 'abstract_': i.p.text.strip().strip('\n')}
                yield Request(i.a['href'], callback=self.parse_item, meta=meta)
        if self.time is None or DateUtil.formate_time2time_stamp(time_) >= int(self.time):
            yield Request(response.url.replace('%253D' + response.url.split('%253D')[1], '%253D' + str(int(response.url.split('%253D')[1]) + 1)))

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['title'] = response.meta['title_']
        item['category1'] = response.meta['category1_']
        item['category2'] = None
        item['body'] = ''.join([i.text for i in soup.select(' .body-text p')])
        item['abstract'] = response.meta['abstract_']
        item['pub_time'] = response.meta['pub_time_']
        item['images'] = response.meta['images_']
        yield item
