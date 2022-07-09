# encoding: utf-8
from bs4 import BeautifulSoup
from utils.util_old import Util
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

#author:钟钧仰
class RakyatkalbarSpider(BaseSpider):
    name = 'rakyatkalbar'
    website_id = 40
    language_id = 1952
    start_urls = ['https://rakyatkalbar.com/']

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        last_time=''
        memu=soup.select('body > div.jeg_viewport > div.jeg_main > div > div.jeg_content > div.container > div > div > div.jeg_main_content.col-sm-8 > div > div.jeg_posts.jeg_block_container > div.jeg_posts.jeg_load_more_flag > article')

        for i in memu:
            try:
                response.meta['image']=(i.select_one('img').get('data-src'))
            except:
                response.meta['image']=[]
            page_url=(i.select_one('a').get('href'))
            response.meta['title']=(i.select('a')[1].text)
            response.meta['abstract']=(i.select_one('div.jeg_postblock_content > div.jeg_post_excerpt > p').text)  # abstract
            t = (i.select_one('div.jeg_postblock_content > div.jeg_post_meta > div.jeg_meta_date > a').text).replace(',', '').split(' ')
            last_time= ((t[3] + '-' + str(Util.month[t[1]]).rjust(2,'0')+'-'+t[2]).rjust(2,'0'))+' 00:00:00'
            time = ((t[3] + '-' + str(Util.month[t[1]]).rjust(2, '0') + '-' + t[2]).rjust(2, '0'))
            response.meta['pub_time']=time+' 00:00:00'
            yield Request(url=page_url,callback=self.parse_item,meta=response.meta)
        if  self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
            try:
                next_url=soup.select_one('body > div.jeg_viewport > div.jeg_main > div > div.jeg_content > div.container > div > div > div.jeg_main_content.col-sm-8 > div > div.jeg_block_navigation > div.jeg_navigation.jeg_pagination.jeg_pagenav_1.jeg_alignleft.no_navtext.no_pageinfo > a.page_nav.next').get('href')
                # print(next_url)
                yield Request(url=next_url,callback=self.parse,meta=response.meta)
            except:
                pass

    def parse_item(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        all_p = soup.select(' body > div.jeg_viewport > div.post-wrapper > div:nth-child(1) > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-content.no-share > div.content-inner > p')
        item = NewsItem()
        try:
            item['category1'] =  soup.select_one('#breadcrumbs > span.breadcrumb_last_link > a').text
        except:
            item['category1'] =None
        p_list = []
        for i in all_p:
            p_list.append(i.text)
        item['title'] = response.meta['title']
        item['category2'] = None
        item['body'] = '\n'.join(p_list)
        item['abstract'] = response.meta['abstract']
        item['pub_time'] = response.meta['pub_time']
        item['images'] = response.meta['image']
        yield item