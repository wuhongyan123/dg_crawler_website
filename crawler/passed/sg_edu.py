# encoding: utf-8
import json
from bs4 import BeautifulSoup
import utils.date_util
from crawler.spiders import BaseSpider
from crawler.items import *
from scrapy.http.request import Request


# Author:陈卓玮
# check：凌敏 pass
class edu_sg_spider(BaseSpider):
    name= 'edusg'
    website_id=434
    language_id=1866
    params_news_rows=1
    start_urls = [f'https://search.moe.gov.sg/solr/moe_search_index/select?q=*&app=site_search&fq=content_type_s%3A(%22news%22)&fq=active_b:true&rows=1&start=0&sort=modified_dt%20desc']
    def parse(self,response):
        if len(json.loads(response.text)['response']['docs']) == 1:yield Request(f"https://search.moe.gov.sg/solr/moe_search_index/select?q=*&app=site_search&fq=content_type_s%3A(%22news%22)&fq=active_b:true&rows={int(json.loads(response.text)['response']['numFound'])}&start=0&sort=modified_dt%20desc")
        else:
            for i in json.loads(response.text)['response']['docs']:
                if self.time == None or utils.date_util.DateUtil.formate_time2time_stamp(i['end_dt'].replace("T", " ").replace("Z", "")) >= self.time:yield Request(url = "https://www.moe.gov.sg" + i['link_s'],callback=self.parse_essay,meta={'title':i['name_s'],'category1':i['news_category_s'],'pub_time':i['end_dt'].replace("T", " ").replace("Z", ""),'abstract':BeautifulSoup(i['_content_ngram'],'lxml').text})
    def parse_essay(self,response):
        soup,item = BeautifulSoup(response.text,'lxml'),NewsItem()
        item['title'],item['category1'],item['body'],item['abstract'],item['pub_time'],item['images'] = response.meta['title'],response.meta['category1'],'\n'.join((i.text.replace('\n','') for i in soup.select('p'))),response.meta['abstract'],response.meta['pub_time'],list(k.get('src') for k in soup.select('img'))
        yield item
