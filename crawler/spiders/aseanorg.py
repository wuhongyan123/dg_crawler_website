import requests
from bs4 import BeautifulSoup
from scrapy.http import headers
from crawler.spiders import BaseSpider
from crawler.items import *
from scrapy.http.request import Request
import execjs
import re
import copy

from common.date import ENGLISH_MONTH as month
from common.header import MOZILLA_HEADER


class AseanorgSpider(BaseSpider):
    name = 'aseanorg'
    website_id = 1802
    language_id = 1866
    start_urls = [
        'https://asean.org/category/news/',
        'https://asean.org/category/statements-meetings/',
        'https://asean.org/category/speeches/',
        'https://asean.org/category/news-events/'
    ]
    custom_settings = {"DEFAULT_REQUEST_HEADERS": MOZILLA_HEADER}

    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i,meta={'Headers':MOZILLA_HEADER})

    def getCookie(self, response):
        # 用re把js代码扣下来
        js = re.findall(r'<script>(.*)</script>', response.text)[0]
        # 因为execjs是函数驱动的，所以得用函数包装一下，获取r的值
        ctx = execjs.compile(('function fun(){' + js + '}').replace('e(r)', 'return r'))
        js = ctx.call('fun')
        # 同上
        ctx = execjs.compile(
            ('function fun(){' + js + '}').replace('document.cookie', 'out').replace('location.reload()', 'return out'))
        # 添加cookie
        cookie = ctx.call('fun')
        return cookie

    def parse(self, response):
        if (re.findall(r'<title>(.*)</title>', response.text)[0] == 'You are being redirected...'):
            header = copy.deepcopy(MOZILLA_HEADER)
            header["cookie"] = self.getCookie(response)
            # 往request传请求头的方式是直接给meta的Headers传个列表，里面是要修改的请求头字段
            # 如果Headers里没有user-agent字段会刷新ua，传了就不会刷新而是用你传进去的那个
            yield Request(url=response.url,meta={'Headers':header},dont_filter=True)
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('div.elementor-widget-container > article > a')
            for article in articles:
                article_url = article.get('href')
                # 后面这些也是一样
                yield Request(url=article_url, callback=self.parse_item)
            next_page = soup.select_one('.page-numbers.next').get('href')
        # yield Request(url=next_page, meta=response.meta, callback=self.parse_page, headers=hd,dont_filter=True)

    def parse_page(self, response):
        print("parseeeeeeeeeeeeeeeeee")
        print(response.text)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     articles = soup.select('div.elementor-widget-container > article > a')
    #     hd = self.headers
    #     hd['referer'] = response.url
    #     for article in articles:
    #         article_url = article.get('href')
    #         yield Request(url=article_url, callback=self.parse_item,headers=hd,dont_filter=True)
    #     next_page = soup.select_one('.page-numbers.next').get('href')
    #     print(next_page)
    #     yield Request(url=next_page, meta=response.meta, callback=self.parse_page, headers=hd,dont_filter=True)
    #
    def parse_item(self, response):
        print(response.text)
        # if (re.findall(r'<title>(.*)</title>', response.text)[0] == 'You are being redirected...'):
        #     print("parse_itemmmmmmmmmmmmmmmmmmmmm")
        #     cookie = self.getCookie(response)
        #     hd = self.headers
        #     hd['cookie'] = cookie
        #     yield Request(url=response.url, headers=hd, callback=self.parse_items,dont_filter=True)
    #
    # def parse_items(self, response):
    #     print("parse_itemmmmmmmmmmmmmmmmmmmmm")
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     item = NewsItem()
    #     item['category1'] = soup.select_one(
    #         '.esoup.selecrlementor-widget-container div.breadcrumb > a:nth-child(3)').text
    #     item['title'] = soup.select_one(
    #         'div.elementor-element.elementor-element-b369dd8.elementor-widget.elementor-widget-theme-post-title.elementor-page-title.elementor-widget-heading > div > h2').text.strip()
    #     tt = soup.select_one(
    #         'div.elementor-element.elementor-element-f86aebc.elementor-widget.elementor-widget-post-info > div > ul > li > a > span').text.strip().replace(
    #         ',', ' ').split(' ')
    #     item['pub_time'] = "{}-{}-{}".format(tt[2], month[tt[2]], tt[0]) + ' 00:00:00'
    #     item['images'] = [img.get('src') for img in
    #                       soup.select(' div.elementor-container.elementor-column-gap-wide .elementor-image img')]
    #     item['body'] = '\n'.join([paragraph.text.strip()
    #                               for paragraph in soup.select(
    #             'section.elementor-section.elementor-top-section.elementor-element.elementor-element-8e4d6ae.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-1113e65 > div > div > div > div > div > div > div > section > div > div > div > div > div > div > div.elementor-widget-container > div.elementor-text-editor elementor-clearfix p')
    #                               if
    #                               paragraph.text != '' and paragraph.text != ' '])
    #     item['abstract'] = item['body'].split('\n')[0]
    #     yield item
