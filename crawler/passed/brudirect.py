# encoding: utf-8
from bs4 import BeautifulSoup
from crawler.items import *
from crawler.spiders import BaseSpider
from scrapy.http.request import Request
from utils.date_util import DateUtil
from copy import deepcopy
# author:ishejialea/robot-2233
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
    'December': '12'}

ENGLISH_DAY = {
    '1st': '01',
    '2nd': '02',
    '3rd': '03',
    '4th': '04',
    '5th': '05',
    '6th': '06',
    '7th': '07',
    '8th': '08',
    '9th': '09',
    '10th':'10',
    '11th':'11',
    '12th':'12',
    '13th':'13',
    '14th':'14',
    '15th':'15',
    '16th':'16',
    '17th':'17',
    '18th':'18',
    '19th':'19',
    '20th':'20',
    '21st':'21',
    '22nd':'22',
    '23rd':'23',
    '24th':'24',
    '25th':'25',
    '26th':'26',
    '27th':'27',
    '28th':'28',
    '29th':'29',
    '30th':'30',
    '31st':'31'

}

class BrudirectSpiderSpider(BaseSpider):
    name = 'brudirect'
    website_id = 218
    language_id = 1866
    start_urls = ['https://www.brudirect.com/viewall_national-headline.php']


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.select(' .toogle tr'):
            yield Request(url='https://www.brudirect.com/' +i.a.get('href'), callback=self.parse2)
        yield Request(url='https://www.brudirect.com/'+soup.select(' .toogle .paginate')[-1].a.get('href'), callback=self.parse)


    def parse2(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        ssd = soup.find_all(align='justify')[19].text.strip().split('|')[0].split('  ')[0].split(' ')
        time_ = ssd[-1] + '-' + ENGLISH_MONTH[ssd[0]] + '-' + ENGLISH_DAY[ssd[1].split(',')[0]] + ' 00:00:00'
        meta={'pub_time_':time_}
        if self.time is None or DateUtil.formate_time2time_stamp(int(time_)) >= int(self.time):
            yield Request(url=response.url, callback=self.parse_item,meta=meta)


    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = NewsItem()
        item['title'] = soup.select_one(" .cont.span_2_of_3 .sky-form").find_all(align='center')[0].text
        item['category1'] = 'ALL'
        item['category2'] = None
        item['body'] = '\n'.join([i.text.strip() for i in soup.select_one(" .cont.span_2_of_3 .sky-form").find_all(style="text-align: justify;")])
        item['abstract'] = soup.select_one(" .cont.span_2_of_3 .sky-form").find_all(style="text-align: justify;")[0].select_one(' p').text
        item['pub_time'] = response.meta['pub_time_']
        try:
            item['images'] = 'https://www.brudirect.com/'+str(soup.select_one(" .cont.span_2_of_3 .sky-form").find_all(align='center')[1]).split('src=')[-1].split('/></')[0]
        except:
            item['images'] = None
        yield item