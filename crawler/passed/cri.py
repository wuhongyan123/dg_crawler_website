# encoding: utf-8
from time import sleep

from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request

# author : 钟钧仰
class CriSpider(BaseSpider):
    name = 'cri'
    website_id = 2117
    language_id = 1813
    start_urls = ['http://www.cri.cn/']
    is_http = 1

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        menu_list_cate1 = ['讲习所', '讲习所',
                           '国际锐评', '国际锐评',
                           '外媒看中国', '外媒看中国',
                           '国际三分钟','国际三分钟',
                           '国际微访谈', '国际微访谈',
                           '老外在中国','老外在中国',
                           '国际漫评滚动', '国际漫评', '国际漫评',
                           '环创', '环创', '环创', '环创', '环创',
                           '企业', '企业', '企业', '企业', '企业', '企业', '企业', '企业', '企业', '企业',
                           '城市', '城市', '城市', '城市', '城市', '城市', '城市', '城市', '城市', '城市',
                           '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建', '城建','城建', '城建', '城建',
                           '财智', '财智', '财智', '财智', '财智', '财智', '财智', '财智', '财智',
                           '教育', '教育', '教育', '教育', '教育', '教育', '教育', '教育', '教育',
                           '科技', '科技', '科技', '科技', '科技', '科技', '科技', '科技',
                           '汽车', '汽车', '汽车', '汽车',
                           '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱', '文娱',
                           '体育','体育','体育','体育','体育','体育','体育','体育']
        menu_list_cate2 = ['讲习所', '讲习所',
                           '国际锐评', '国际锐评',
                           '外媒看中国', '外媒看中国',
                           '国际三分钟','国际三分钟',
                           '国际微访谈','国际微访谈',
                           '老外在中国','老外在中国',
                           '滚动', '国际漫评', '国际漫评',
                           '环球快讯', '环球专访', '政策解读', '创业图解', '活动直击',
                           '新闻资讯', '全息视点', '企业扶贫', '文旅映话', '环球视野', '社会责任', '人物', '公益', '健康', '专题',
                           '旅游', '文化', '经贸', '创新', '我是中国控', '名城会客厅', '一带一路', '专题', '滚动', '原创',
                           '滚动', '权威专题', '要闻', '书记市长话城建', '城建•可观', '企业动态', '短视频展映', '城建•决策者', '城建•全纪录', '城视在线', '美丽新城',
                           '城建•全媒体', '依法治城', '招商引智', '扶贫第一线', '宜居•养生', '质量•监督', '地产楼市',
                           '资讯', '聚焦', '见解', '资本', '园区', '企业', '财智约', '财智家', '财智荟',
                           '滚动', '党建学园', '会客厅', '国际教育', '产教融合', '商学院.招生访谈', '商学院.热点资讯', '商学院.活动', '商学院.聚焦商学',
                           '业界资讯', '数据专栏', '前沿动态', '科技园', '网络安全', '智能硬件', '科技商务', '热点围观',
                           '焦点', '资讯', '头条', '人物',
                           'CRI文娱专稿','文娱现场播报','电视剧','电影','综艺','时尚','星途','影评','往期采访','图库','图库','演出','演出',
                           '滚动', '篮球', '足球', '击剑', '冰雪', '综合', '独家', '产业']
        news = ['http://news.cri.cn/inc/4fc9c0a3-771b-478d-bce2-9a7c59325194-2.inc', 'http://news.cri.cn/gjjxs',  # 讲习所
                'http://news.cri.cn/inc/08b152bb-56a6-4ba4-9b60-8761fa1a1568-2.inc', 'http://news.cri.cn/guojiruiping',# 锐评
                'http://news.cri.cn/inc/cd6e5c28-5049-4232-9b27-d8efbe647bf3-2.inc', 'http://news.cri.cn/wmkzg',# 外媒看中国
                'http://news.cri.cn/inc/3c5aa38f-81db-4fb7-bead-cc09e9755a71-2.inc', 'http://news.cri.cn/knowntheworld',#国际三分钟
                'http://news.cri.cn/inc/ae15b5c9-8f43-4931-9a68-ec2100a80f24-2.inc', 'http://news.cri.cn/gjwft',#国际微访谈
                'http://news.cri.cn/inc/c0d55f64-a80a-44fd-b99c-4c04a3257b58-2.inc', 'http://news.cri.cn/lwzzg',#老外在中国
                'http://news.cri.cn/roll', 'http://news.cri.cn/list/gjmp', 'http://news.cri.cn/data/list/gjmp-2',# 国际漫评滚动,国际漫评静态,国际漫评动态
                'http://ge.cri.cn/globalnews', 'http://ge.cri.cn/global-interview', 'http://ge.cri.cn/policy','http://ge.cri.cn/graphic', 'http://ge.cri.cn/activity',  # 环创
                'http://ce.cri.cn/news', 'http://ce.cri.cn/multimedia', 'http://ce.cri.cn/businessaid','http://ce.cri.cn/culture', 'http://ce.cri.cn/global', 'http://ce.cri.cn/responsibility','http://ce.cri.cn/character', 'http://ce.cri.cn/service', 'http://ce.cri.cn/health','http://ce.cri.cn/special',
                'http://city.cri.cn/tourism', 'http://city.cri.cn/culture', 'http://city.cri.cn/economyandtrade','http://city.cri.cn/innovate', 'http://city.cri.cn/chinesestories', 'http://city.cri.cn/interview','http://city.cri.cn/theBeltandRoadInitiatives', 'http://city.cri.cn/special','http://city.cri.cn/rollingnews', 'http://city.cri.cn/CRIoriginal',
                'http://cj.cri.cn/headlines', 'http://cj.cri.cn/special', 'http://cj.cri.cn/news', 'http://cj.cri.cn/zixun', 'http://cj.cri.cn/modelcity', 'http://cj.cri.cn/companynews','http://cj.cri.cn/shotvideo', 'http://cj.cri.cn/interview', 'http://cj.cri.cn/documentary','http://cj.cri.cn/video', 'http://cj.cri.cn/environment', 'http://cj.cri.cn/omnimedia','http://cj.cri.cn/judicialnews', 'http://cj.cri.cn/investment', 'http://cj.cri.cn/povertyalleviation','http://cj.cri.cn/healthnews', 'http://cj.cri.cn/marketsupervision', 'http://cj.cri.cn/realestate',
                'http://gr.crionline.cn/news', 'http://gr.crionline.cn/focus', 'http://gr.crionline.cn/opinion', 'http://gr.crionline.cn/capital', 'http://gr.crionline.cn/park', 'http://gr.crionline.cn/enterprise','http://gr.crionline.cn/talks', 'http://gr.crionline.cn/story', 'http://gr.crionline.cn/forum',
                'http://edu.cri.cn/Rolling', 'http://edu.cri.cn/CPC', 'http://edu.cri.cn/Interview', 'http://edu.cri.cn/INT.EDU', 'http://edu.cri.cn/Integration', 'http://edu.cri.cn/zsft','http://edu.cri.cn/rdzx', 'http://edu.cri.cn/hd', 'http://edu.cri.cn/jjsx',
                'http://it.cri.cn/industry', 'http://it.cri.cn/Data', 'http://it.cri.cn/latest', 'http://it.cri.cn/technicalpark', 'http://it.cri.cn/safety', 'http://it.cri.cn/hardware','http://it.cri.cn/business', 'http://it.cri.cn/topic',
                'http://auto.cri.cn/News', 'http://auto.cri.cn/Information', 'http://auto.cri.cn/Headlines', 'http://auto.cri.cn/Personage',
                'http://ent.cri.cn/roll/cri', 'http://ent.cri.cn/roll/bb', 'http://ent.cri.cn/tv', 'http://ent.cri.cn/movie','http://ent.cri.cn/variety','http://ent.cri.cn/fashion','http://ent.cri.cn/star','http://ent.cri.cn/11/llk','http://ent.cri.cn/starshow/wqcf','http://ent.cri.cn/photo','http://ent.cri.cn/inc/e8b81ee2-2698-4d65-9b8e-d40e6c889652-2.inc','http://ent.cri.cn/drama','http://ent.cri.cn/inc/9601789d-824e-40ff-96fd-5cd30fa08cea-2.inc',
                'http://sports.cri.cn/roll', 'http://sports.cri.cn/basketball', 'http://sports.cri.cn/football', 'http://sports.cri.cn/fencing', 'http://sports.cri.cn/bingxue', 'http://sports.cri.cn/others','http://sports.cri.cn/cri','http://sports.cri.cn/economy'
                ]
        for i in range(0, 109):
            response.meta['category2'] = menu_list_cate2[i]
            response.meta['category1'] = menu_list_cate1[i]
            response.meta['url'] = news[i]
            yield Request(url=news[i], callback=self.parse_category, meta=response.meta)
            print(news[i])


    def parse_category(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # print(response)
        last_time = ''
        menu_list = ['讲习所', '国际锐评', '外媒看中国','国际三分钟','国际微访谈','老外在中国']
        company_list = ['环创','企业','城建','财智','教育','科技','汽车']
        city_menu = ['旅游', '文化', '经贸', '创新', '我是中国控', '名城会客厅', '一带一路', '专题', '滚动', '原创']
        if response.meta['category1'] in menu_list:  # 处理'讲习所','外媒看中国','国际锐评'的新闻
            memu = soup.select('#sanfentianxia > div.content > div.sftx-list.more-list > ul > li')  # 处理静态页面
            if len(memu) == 0:
                memu = soup.select('body > div > ul > li')  # 处理动态页面
            for i in memu:
                response.meta['title'] = (i.select_one('div.sftx-list-text > a').text)
                news_url1 = ('http://news.cri.cn' + i.select_one('div.sftx-list-text > a').get('href').replace('//news.cri.cn',''))
                t = i.select_one('div.sftx-list-time').text
                last_time = response.meta['pub_time'] = (t.replace('年', '-').replace('月', '-').replace('日', '') + ':00')
                sleep(10)
                if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                    yield Request(url=news_url1, callback=self.parse_item, meta=response.meta)
            if len(memu) > 0 and response.meta['url'].find('.inc') != -1:
                if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                    tmp = response.meta['url'].strip('.inc').split('-')
                    tmp[5] = (str(int(tmp[5]) + 1))
                    next_url = '-'.join(tmp) + '.inc'
                    response.meta['url'] = next_url
                    # sleep(10)
                    yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1']=='体育':
            menu = soup.select('body > div.box-wrap > div > div.left-center.list-box > div.pic-list-bg > ul > li ')
            if response.meta['category2'] == '综合' or  response.meta['category2'] == '足球' or response.meta['category2'] == '击剑' or response.meta['category2'] == '产业' or  response.meta['category2'] == '冰雪':

                for i in menu:
                    news_url = (i.select_one('div.text > p.title-p > a').get('href'))
                    # print(news_url)
                    response.meta['title'] =(i.select_one('div.text > p.title-p > a').text)
                    if news_url[1] == '/':
                        urls = 'http:' + news_url
                    else:
                        urls = 'http://sports.cri.cn' + news_url
                    if news_url.find('.cri.cn') != -1:
                        news_url = news_url[news_url.find('.cri.cn') + 7:]
                    last_time = response.meta['pub_time'] = news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 环创翻页
                    if len(menu) != 0:
                        next_url=response.meta['url']
                        if next_url.find('.html') == -1:
                            next_url = next_url + '/index-2.html'
                        else:
                            tmp = next_url[:next_url.find('.html')].split('-')
                            tmp[1] = (str(int(tmp[1]) + 1))
                            next_url = '-'.join(tmp) + '.html'
                        response.meta['url']=next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category2'] == '滚动' or response.meta['category2'] == '独家' :
                for i in menu:
                    news_url = (i.select_one('p.title-list > a').get('href'))
                    # print(news_url)
                    response.meta['title'] = (i.select_one('p.title-list > a').text)
                    if news_url[1] == '/':
                        urls = 'http:' + news_url
                    else:
                        urls = 'http://sports.cri.cn' + news_url
                    if news_url.find('.cri.cn') != -1:
                        news_url = news_url[news_url.find('.cri.cn') + 7:]
                    last_time = response.meta['pub_time'] = news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1'] in company_list:
            if response.meta['category1'] == '环创':
                menu = soup.select('body > div.content.details.listText.clearfix > div > div.content-leftWrap01.padTop30.list > div.list-box > ul > li')
                for i in menu:
                    response.meta['title']=i.select_one('h4 > a').text
                    new_url = i.select_one('h4 > a').get('href')
                    if (new_url[1] == '/'):
                        urls = 'http:' + new_url
                    else:
                        urls = 'http://ge.cri.cn' + new_url
                    # new_url = new_url.replace('//news.cri.cn', '')
                    if new_url.find('.cri.cn')!=-1:
                        new_url=new_url[new_url.find('.cri.cn') + 7:]
                    last_time = response.meta['pub_time']=new_url[1:5] + '-' + new_url[5:7] + '-' + new_url[7:9] + ' 00:00:00'
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=urls,callback=self.parse_item,meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 环创翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = (response.meta['url'].split('-'))
                        if response.meta['url'].find('http://ge.cri.cn/global-interview')==-1:
                            if len(changeurl) == 1:
                                next_url = ''.join(changeurl) + '-2'
                            else:
                                changeurl[1] = str(int(changeurl[1]) + 1)
                                next_url = '-'.join(changeurl)
                        else :
                            if len(changeurl) == 2:
                                next_url = '-'.join(changeurl) + '-2'
                            else:
                                changeurl[2] = str(int(changeurl[2]) + 1)
                                next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '企业':
                memu = soup.select('body > div.secondIndex-wrap > div.w1200 > div.w860.left.mgB20 > div > div.secondPage-box-1.list-box > ul > li')
                for i in memu:
                    response.meta['title']=(i.select_one('div > div.list-title > a').text)
                    news_url = i.select_one('div > div.list-title > a').get('href')
                    if news_url.find('.cri.cn') == -1:
                        news_url=('http://ce.cri.cn' + news_url)
                    else:
                        news_url=('http:' + news_url)
                    last_time =response.meta['pub_time']=i.select_one('div > div.list-time').text
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(memu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '财智':
                gr_list=[ '财智约', '财智家', '财智荟']
                memu = soup.select(
                    'body > div.w1200> div.content-bjtBox > div.content-bjt-center > div.w902.list-box > ul > li')
                if response.meta['category2'] in gr_list:
                    for i in memu:
                        response.meta['title']=(i.select_one('p > a').text)
                        news_time = news_url = (i.select_one('p > a').get('href'))
                        if news_url.find('.cn/') == -1:
                            last_time =response.meta['pub_time']=(news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00')
                            news_url='http://gr.crionline.cn'+news_url
                        else:
                            news_url='http:' + news_url
                            news_time = news_url[news_url.find('.cn/') + 3:]
                            last_time =response.meta['pub_time']=(news_time[1:5] + '-' + news_time[5:7] + '-' + news_time[7:9] + ' 00:00:00')
                        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                            yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                else :
                    memu = soup.select(
                        'body > div.w1200> div.w765.left.marginTop10 > div.marginTop10.more-list > div.left-ul.list-wrap > ul > li')
                    for i in memu:
                        response.meta['title']=(i.select_one('p > a').text)
                        last_time =response.meta['pub_time']=(i.select_one('div > div.right.w575 > p.marginTop37 > span').text.strip())
                        response.meta['abstract']=(i.select_one('div > div.right.w575 > p.marginTop5.liBrief').text)  # abstract
                        news_url = i.select_one('p > a').get('href')
                        if news_url.find('.cri.cn') == -1:
                            news_url = ('http://gr.crionline.cn' + news_url)
                        else:
                            news_url = ('http:' + news_url)
                        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                            yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                    if len(memu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '汽车':
                menu = soup.select('body > div.w1200.marginTop35 > div.w750.left > div.left-ul.list-box.marginTop45.list-common > ul > li')
                for i in menu:
                    new_url=news_url = i.select_one('a').get('href')
                    if news_url.find('.cn/') == -1:
                        news_url =('http://auto.cri.cn' + news_url)
                    else:
                        news_url =('http:' + news_url)
                    response.meta['title']=(i.select_one('a').text)
                    if news_url.find('.cri.cn')!=-1:
                        new_url=news_url[news_url.find('.cri.cn') + 7:]
                    last_time = response.meta['pub_time']=new_url[1:5] + '-' + new_url[5:7] + '-' + new_url[7:9] + ' 00:00:00'
                    # last_time =response.meta['pub_time']=(i.select_one('div > div.left.briefBox > span').text)
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=news_url, callback=self.parse_item,meta=response.meta)
                if self.time is None or (
                        last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '科技':
                menu = soup.select('body > div.content.details.clearfix > div.list1200.clearfix > div.content-leftWrap.list.marginTop10 > div.list-box.marTop10 > div > ul > li')
                for i in menu:
                    news_url = i.select_one('h4 > a').get('href')
                    if news_url.find('.cn/') == -1:
                        news_url=('http://it.cri.cn' + news_url)
                    else:
                        news_url=('http:' + news_url)
                    response.meta['title']=(i.select_one('h4 > a').text)
                    last_time =response.meta['pub_time']=(i.select_one('h4 > i').text)
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=news_url, callback=self.parse_item,meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '城建':
                memu = soup.select(
                    'body > div.secondIndex-wrap > div.w1200 > div.w860.left.mgB20 > div > div.secondPage-box-1.list-box > ul > li')
                for i in memu:
                    response.meta['title']=(i.select_one('div > div.list-title > a').text)
                    news_url = i.select_one('div > div.list-title > a').get('href')
                    if news_url.find('.cri.cn') == -1:
                        news_url=('http://cj.cri.cn' + news_url)
                    else:
                        news_url=('http:' + news_url)
                    last_time =response.meta['pub_time']=(i.select_one('div > div.list-time').text)
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(memu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category1']== '教育':
                menu = soup.select('body > div.secondIndex-wrap > div.w1200 > div.w860.left.mgB20 > div > div.secondPage-box-1.list-box > ul > li')
                for i in menu:
                    news_url = i.select_one('div > div.list-title > a').get('href')
                    if news_url.find('.cn/') == -1:
                        news_url=('http://edu.cri.cn' + news_url)
                    else:
                        news_url=('http:' + news_url)
                    response.meta['title']=(i.select_one('div > div.list-title > a').text)
                    last_time =response.meta['pub_time']=(i.select_one('div > div.list-time').text)
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1'] =='城市':  # 处理城市专题
            memu = soup.select('body > div.content.details.listText.clearfix > div > div.content-leftWrap03.padTop30.list > ''div.list-box > div:nth-child(1) > ul > li')
            for i in memu:
                last_time = response.meta['pub_time'] = i.select_one('h4 > i').text
                if i.select_one('h4 > a').get('href').find('.cn/') == -1:
                    news_url = ('http://city.cri.cn' + i.select_one('h4 > a').get('href'))
                else :
                    news_url= 'http:'+ i.select_one('h4 > a').get('href')
                response.meta['title'] = i.select_one('h4 > a').text
                if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                    yield Request(url=news_url, callback=self.parse_item, meta=response.meta)
            if self.time is None or (
                    last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                if len(memu) != 0:
                    next_url = ''
                    changeurl = response.meta['url'].split('-')
                    if len(changeurl) == 1:
                        next_url = ''.join(changeurl) + '-2'
                    else:
                        changeurl[1] = str(int(changeurl[1]) + 1)
                        next_url = '-'.join(changeurl)
                    response.meta['url'] = next_url
                    yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1']== '国际漫评滚动':
            memu = soup.select('body > div.secondIndex-wrap > div > div.w860.left.mgB20 > div > div.secondPage-box-1.list-box > ul > li')
            for i in memu:
                response.meta['title']=i.select_one('div > div.list-title > a').text
                news_url='http://news.cri.cn' + i.select_one('div > div.list-title > a').get('href')
                last_time =response.meta['pub_time']=i.select_one('div > div.list-time').text + ':00'
                if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                    yield Request(url=news_url,callback=self.parse_item,meta=response.meta)
            if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                if len(memu) != 0:
                    next_url = ''
                    changeurl = response.meta['url'].split('-')
                    if len(changeurl) == 1:
                        next_url = ''.join(changeurl) + '-2'
                    else:
                        changeurl[1] = str(int(changeurl[1]) + 1)
                        next_url = '-'.join(changeurl)
                    response.meta['url'] = next_url
                    yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1']== '国际漫评':
            menu = soup.select('body > div.w1200 > div.w850.left > div.list-a > div.more-list.more-list-clear > div > ul > li')
            if len(menu)==0:
                menu = soup.select('body > li')
            for i in menu:
                last_time =response.meta['pub_time']=(i.select_one('h6 > span').text.replace('年', '-').replace('月', '-').replace('日', '-').strip())
                response.meta['title']=(i.select_one('p > a').text)
                response.meta['image']=('http:' + i.select_one('a > img').get('src'))
                if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                    yield Request(url='http://news.cri.cn' + i.select_one('p > a').get('href'), callback=self.parse_item, meta=response.meta)
            if response.meta['url'].find('data')!=-1 and (self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time))):  # 国际漫评翻页
                if len(menu) != 0:
                    next_url = ''
                    changeurl = response.meta['url'].split('-')
                    changeurl[1] = str(int(changeurl[1]) + 1)
                    next_url = '-'.join(changeurl)
                    response.meta['url'] = next_url
                    yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
        elif response.meta['category1']== '文娱':
            if response.meta['category2']== '影评':
                menu = soup.select('body > div.wrap > div.main > div > div.tit-list.tit-list02.list-col01 > ul > li')
                for i in menu:
                    response.meta['title']=(i.select_one('div > h4 > a').text)
                    news_url = (i.select_one('div > h4 > a').get('href'))
                    if news_url.find('html')!=-1:
                        if (news_url[1] == '/'):
                            urls = 'http:' + news_url
                        else:
                            urls = 'http://ent.cri.cn' + news_url
                        if news_url.find('.cri.cn') != -1:
                            news_url = news_url[news_url.find('.cri.cn') + 7:]
                        last_time =response.meta['pub_time']=news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                            yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                if self.time is None or ( last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category2']== '往期采访':
                menu = soup.select('#ent > div.w1200.connr > div.left.w860 > div > div.secondPage-box-1.list-box > ul > li')
                for i in menu:
                    response.meta['title']=(i.select_one('div > div.list-title > a').text)
                    news_url = (i.select_one('div > div.list-title > a').get('href'))
                    if (news_url[1] == '/'):
                        urls = 'http:' + news_url
                    else:
                        urls = 'http://ent.cri.cn' + news_url
                    last_time = response.meta['pub_time'] = i.select_one('div > div.list-time').text
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category2'] == '电视剧'or response.meta['category2'] == '星途' or response.meta['category2'] == '时尚' or response.meta['category2'] == '综艺' or response.meta['category2'] == '电影':
                menu = soup.select('#ent > div.w1200.connr > div.left.w860 > div > div.ent19-card-wrap > div > ul > li')
                for i in menu:
                    response.meta['title']=(i.select_one('div.eff-title > a').text.strip())
                    news_url = (i.select_one('div.eff-title > a').get('href'))
                    if (news_url[1] == '/'):
                        urls = 'http:' + news_url
                    else:
                        urls = 'http://ent.cri.cn' + news_url
                    last_time = response.meta['pub_time'] = i.select_one('div.eff-mes > i').text
                    if last_time != '' and (self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                        yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                if self.time is None or (last_time != '' and int(self.time) < DateUtil.formate_time2time_stamp(last_time)):  # 城市翻页
                    if len(menu) != 0:
                        next_url = ''
                        changeurl = response.meta['url'].split('-')
                        if len(changeurl) == 1:
                            next_url = ''.join(changeurl) + '-2'
                        else:
                            changeurl[1] = str(int(changeurl[1]) + 1)
                            next_url = '-'.join(changeurl)
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category2'] == '演出':
                if response.meta['url'].find('.inc')==-1:
                    menu = soup.select('#ent > div.show-content > div > div.show-list-yczx > div.show-list-yczx-list > ul > li')
                    for i in menu:
                        response.meta['title']=i.select_one('div.show-list-yczx-list-title-box > div.show-list-yczx-list-title > a').text.strip()
                        news_url = i.select_one('div.show-list-yczx-list-title-box > div.show-list-yczx-list-title > a').get('href')
                        if news_url[1] == '/':
                            urls = 'http:' + news_url
                        else:
                            urls = 'http://ent.cri.cn' + news_url
                        last_time = response.meta['pub_time'] = i.select_one('div.show-list-yczx-list-title-box > div.show-list-yczx-list-timeBox > span').text
                        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                            yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                else :
                    menu = soup.select('body > div > ul > li')
                    for i in menu:
                        response.meta['title'] =(i.select_one('div.show-list-yczx-list-title-box > div.show-list-yczx-list-title > a').text.strip())
                        news_url = (i.select_one('div.show-list-yczx-list-title-box > div.show-list-yczx-list-title > a').get('href'))
                        if news_url[1] == '/':
                            urls = 'http:' + news_url
                        else:
                            urls = 'http://ent.cri.cn' + news_url
                        if news_url.find('.cri.cn') != -1:
                            news_url = news_url[news_url.find('.cri.cn') + 7:]
                        last_time = response.meta['pub_time'] = news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                        if last_time != '' and (self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                            yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                    if len(menu) > 0 and response.meta['url'].find('.inc') != -1:
                        if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                            tmp = response.meta['url'].strip('.inc').split('-')
                            tmp[5] = (str(int(tmp[5]) + 1))
                            next_url = '-'.join(tmp) + '.inc'
                            response.meta['url'] = next_url
                            yield Request(url=next_url, callback=self.parse_category, meta=response.meta)
            elif response.meta['category2'] == '图库':
                menu = soup.select('#ent > div.content.w1200 > div.content-wrap > div > ul > li')
                if len(menu) > 0 and response.meta['url'].find('.inc') == -1:
                    for i in menu:
                        response.meta['title'] = (i.select_one('div.list-title > div.lable-title.lf > a').text.strip())
                        news_url = (i.select_one('div.list-title > div.lable-title.lf > a').get('href'))
                        if news_url[1] == '/':
                            urls = 'http:' + news_url
                        else:
                            urls = 'http://ent.cri.cn' + news_url
                        if news_url.find('.cri.cn') != -1:
                            news_url = news_url[news_url.find('.cri.cn') + 7:]
                        last_time = response.meta['pub_time'] = news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                        if last_time != '' and (self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                            yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                else:
                    menu=soup.select('body > ul > li')
                    for i in menu:
                        response.meta['title'] = (i.select_one('div.list-title > div.lable-title.lf > a').text.strip())
                        news_url = (i.select_one('div.list-title > div.lable-title.lf > a').get('href'))
                        if news_url[1] == '/':
                            urls = 'http:' + news_url
                        else:
                            urls = 'http://ent.cri.cn' + news_url
                        if news_url.find('.cri.cn') != -1:
                            news_url = news_url[news_url.find('.cri.cn') + 7:]
                        last_time = response.meta['pub_time'] = news_url[1:5] + '-' + news_url[5:7] + '-' + news_url[7:9] + ' 00:00:00'
                        if last_time != '' and (self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time)):
                            yield Request(url=urls, callback=self.parse_item, meta=response.meta)
                    if self.time is None or int(self.time) < DateUtil.formate_time2time_stamp(last_time):
                        tmp = response.meta['url'].strip('.inc').split('-')
                        tmp[5] = (str(int(tmp[5]) + 1))
                        next_url = '-'.join(tmp) + '.inc'
                        response.meta['url'] = next_url
                        yield Request(url=next_url, callback=self.parse_category, meta=response.meta)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'lxml')
        item['title'] = response.meta['title']
        item['category1'] = response.meta['category1']
        item['category2'] =  response.meta['category2']
        image = []
        p_list = []
        menu_list = ['外媒看中国', '国际锐评','国际微访谈','老外在中国','国际三分钟']
        city_menu = ['旅游', '文化', '经贸', '创新', '我是中国控', '名城会客厅', '一带一路', '专题', '滚动', '原创']
        item['abstract']=''
        item['pub_time'] = response.meta['pub_time']
        if response.meta['category1'] in menu_list:
            all_p = soup.select('#abody > p')
            for i in all_p:
                try:
                    image.append('http:' + i.select_one('img').get('src'))
                except:
                    pass
                p_list.append(i.text.strip())
            if len(p_list) > 0:
                item['abstract'] = p_list[0]
        elif response.meta['category1'] == '讲习所':
            try:
                item['abstract'] = soup.select_one('body > div.newPcbg > div > div > h3 > span').text
            except:
                item['abstract'] =''
            all_p = soup.select('body > div.newPcbg > div > div > div.newTime > div > div > div.banner-img > ul > li')
            p_list.append(item['abstract'])
            for i in all_p:
                try:
                    image.append('http:' + i.select_one('img').get('src'))
                except:
                    pass
                try:
                    p_list.append(i.select_one('h4').text.strip('') + i.select_one('p').text.strip(''))
                except:
                    pass
            try:
                image.append('http:' + soup.select_one('#abody > p:nth-child(1) > img').get('src'))
            except:
                pass
        elif response.meta['category1'] == '体育' or response.meta['category2'] == '图库' or response.meta['category2'] == '演出' or response.meta['category2'] == '电视剧'or response.meta['category2'] == '电影' or response.meta['category2'] == '综艺' or response.meta['category2'] == '时尚'or response.meta['category2'] == '星途' or response.meta['category2']== '影评' or response.meta['category1']== '国际漫评' or response.meta['category1']== '国际漫评滚动' or response.meta['category1'] == '城市' or response.meta['category1'] == '环创' or response.meta['category1'] == '企业' or response.meta['category1'] == '城建'or response.meta['category1'] == '财智'or response.meta['category1'] == '教育' or response.meta['category1']== '科技'or response.meta['category1']== '汽车' :
            all_p = soup.select('#abody > p')
            for i in all_p:
                try:
                    image.append('http:' + i.select_one('img').get('src'))
                except:
                    pass
                p_list.append(i.text.strip())
            if len(p_list)>0:
                item['abstract'] = p_list[0]
        elif response.meta['category2']== '往期采访' :
            all_p = soup.select('body > div > div.all-container > div > div > div.right > div > div.starshow03-text > p')
            for i in all_p:
                p_list.append(i.text)
            if len(p_list) > 0:
                item['abstract'] = p_list[0]
        if response.meta['category1'] == '城市':
            all_p = soup.select('#abody > div:nth-child(2) > p')
            for i in all_p:
                try:
                    image.append('http:' + i.select_one('img').get('src'))
                except:
                    pass
                p_list.append(i.text.strip())
        item['body'] = '\n'.join(p_list)
        item['images'] = image
        if len(item['abstract']) != 0 or len(item['body']) != 0 or len(item['images']) != 0:
            yield item
