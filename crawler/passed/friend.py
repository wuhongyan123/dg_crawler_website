from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from bs4 import BeautifulSoup

# author : 李玲宝
class FriendSpider(BaseSpider):
    name = 'friend'
    website_id = 2033
    language_id = 1866
    start_urls = ['http://friend.com.kp/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        category1 = soup.select('div.hor-menu>ul>li')[2].select('a')[1:]
        for i in category1:
            url = 'http://friend.com.kp' + i['href'] + '/'
            yield scrapy.Request(url + '1', callback=self.parse_page, meta={'category1': i.text.strip(), 'url': url, 'page': 1})

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        block = soup.select('.articles .list-table>li')
        flag = True
        if self.time is not None:
            last_time = block[-1].select_one('.list-td-rec-date').text.strip() + ' 00:00:00'
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for i in block:
                url = 'http://friend.com.kp/index.php/articles/view/' + i['idx'] + '/' + i['page']
                response.meta['pub_time'] = i.select_one('.list-td-rec-date').text.strip() + ' 00:00:00'
                yield Request(url, callback=self.parse_item, meta=response.meta)
        else:
            flag = False
            self.logger.info("时间截止")
        if flag:
            response.meta['page'] += 1
            yield Request(response.meta['url'] + str(response.meta['page']), callback=self.parse_page, meta=response.meta)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = NewsItem()
        item['category1'] = response.meta['category1']
        item['pub_time'] = response.meta['pub_time']
        item['images'] = ['http://friend.com.kp' + img.get('src') for img in soup.select('.detail-td-content img')]
        item['body'] = '\n'.join(i.text.strip() for i in soup.select('.detail-td-content>div') if (i.text.strip() != ''))
        for i in soup.select('.detail-td-content>p'):
            text = i.text.strip()
            if (text != ''):
                item['title'] = text
                break
        for i in soup.select('.detail-td-content>div'):
            text = i.text.strip()
            if not (text == '' or text == item['title']):
                item['abstract'] = text
                break
        return item
