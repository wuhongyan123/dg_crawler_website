from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request


# Author:陈卓玮
class ChinaembassySpider(BaseSpider):
    name = 'china-embassy'
    website_id = 215
    language_id = 2266
    allowed_domains = ['china-embassy.org']
    start_urls = ['http://bn.china-embassy.org/chn/']
    e = ''
    is_http = 1

    def parse(self, response):
        list_pages = ["zgxws", "zwgxs", "zytz", "fyrth", "sgxss"]
        for i in list_pages:
            self.e = i
            meta = {'e': i}
            yield Request(url=self.start_urls[0] + i, callback=self.next_page, meta=meta)

    # 列表翻页
    def next_page(self, response):
        meta = response.meta
        soup = BeautifulSoup(response.text, 'html.parser')
        # max_page = soup.select_one('#pages > script').text
        # max = int(max_page.split('\n')[4].split('//')[0].replace(' ', '').split('=')[1])
        for i in range(0, 28):
            if i == 0:
                n_url = 'http://bn.china-embassy.org/chn/' + response.meta['e'] + '/index.htm'
            else:
                l = soup.select('#right > div.center_content > ul > li')
                t = l[0].text.split('(')[1].strip(')')
                try:
                    int(t.replace('/', ''))
                except:
                    t = 0
                if self.time == None or t >= int(self.time):
                    n_url = 'http://bn.china-embassy.org/chn/' + response.meta['e'] + '/index_' + str(i) + '.htm'
                    yield Request(url=n_url, callback=self.sub_parse, meta=response.meta)

    def sub_parse(self, response):

        soup = BeautifulSoup(response.text, 'html.parser')
        l = soup.select('#right > div.center_content > ul > li')

        for i in l:
            t = i.text.split('(')[1].strip(')')
            int(t.replace('/', ''))
            if self.time == None or t >= int(self.time):
                u = i.select_one('a').get('href').strip('.').strip('/')
                ur = 'http://bn.china-embassy.org/chn/' + response.meta['e'] + '/' + u
                yield Request(url=ur, callback=self.get_pages)

    def get_pages(self, response):

        items = NewsItem()
        # response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        items['category1'] = 'news'
        try:
            items['title'] = soup.select_one('#News_Body_Title').text
        except:
            items['title'] = ''

        try:
            items['pub_time'] = soup.select_one('#News_Body_Time').text
        except:
            items['pub_time'] = ''

        News_Content = ''
        # text = soup.select('#News_Body_Txt_A > div > p')
        text = soup.select('#News_Body_Txt_A ')

        for t in text:
            News_Content = News_Content + t.text.strip() + '\n'

        items['body'] = News_Content

        img_url = []
        try:
            img = soup.select('img')
            for i in img:
                img_url.append(str(response.url.split('/t')[0] + i.get('src').strip('.')))
            items['images'] = list(img_url)
        except:
            img = None
        items['abstract'] = items['body'].split('\n')[0]
        yield items
