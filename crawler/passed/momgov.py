from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
from common import date
import re

# author : 华上瑛
time_dict = {
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
        'December': '12',
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sept': 9,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }


class MomgovSpider(BaseSpider):
    name = 'momgov'
    website_id = 464
    language_id = 1866
    start_urls = ['https://www.mom.gov.sg/newsroom/fact-checks',
        'https://www.mom.gov.sg/newsroom/announcements',
                  'https://www.mom.gov.sg/newsroom/press-replies',# 'https://www.mom.gov.sg/newsroom/parliament-questions-and-replies',
                  'https://www.mom.gov.sg/newsroom/mom-statements'] #http://www.utusan.com.my/


    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i,callback=self.parse_page)


    def parse_page(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        flag = True
        articles = soup.select('section.item-listing > article')
        # category1 = response.url.split("/")[4]
        category1 = re.split(r'[?/]', response.url)[4] # %Y-%m-%d %H:%M:%S

        if self.time is not None:
            last_time = (articles[-1].select('div > time')[0].get('datetime')) + " 00:00:00"
        if self.time is None or DateUtil.formate_time2time_stamp(last_time) >= self.time:
            for article in articles:

                pub_time = (article.select('div > time')[0].get('datetime')) + " 00:00:00"
                href = 'https://www.mom.gov.sg' + article.select('h3 > a')[0].get('href')
                title = article.select('h3 > a')[0].text.strip()

                yield Request(url=href, callback=self.parse_item, meta={'pub_time':pub_time,'category1':category1,'title':title})
        else:
            flag = False
            self.logger.info("时间截止")
        if flag:
            try:
                next_page_link = 'https://www.mom.gov.sg' + soup.select('a.page-next')[0].get('href')
                yield Request(url=next_page_link, callback=self.parse_page, meta=response.meta)
            except:
                self.logger.info("no more pages")


    def parse_item(self, response):#点进文章里面的内容
        soup = BeautifulSoup(response.text, 'lxml')

        fcselect = ['div #pagecontent_0_documentcontent_0_DivCode > p','div #pagecontent_0_documentcontent_0_DivCode > p > span','div #pagecontent_0_documentcontent_0_DivCode']

        if response.url.split('/')[4]=='fact-checks':
            for i in fcselect:
                article = soup.select(i)
                if len(article)==0 or len(article)==1:
                    continue
                else:
                    break
        else:
            article = soup.select('div #pagecontent_0_documentcontent_0_DivCode > p')

        if len(article) == 0 or len(article)==1 :
            if  response.url.split('/')[4]!='fact-checks':
                article = soup.select('div #pagecontent_0_documentcontent_0_DivCode > ol > li')
                if len(article)==0:
                    article = soup.select('div #pagecontent_0_documentcontent_0_DivCode')

            else:
                article = soup.select('div #pagecontent_0_documentcontent_0_DivCode')

        body = " "
        for b in article:
            body += b.text.strip()

        abstract =  body.split('.')[0]

        item = NewsItem()
        item['title'] = response.meta['title']
        item['abstract'] = abstract
        item['body'] = body # response.mata['body']
        item['pub_time'] = response.meta['pub_time']
        item['category1'] = response.meta['category1']
        item['category2'] = None
        item['images'] = []  # response.meta['category2']

        yield item


