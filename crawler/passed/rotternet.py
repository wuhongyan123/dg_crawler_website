# encoding: utf-8
from copy import deepcopy
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
import time

# author：欧炎镁
# check； 彭雨胜
class RotternetSpider(BaseSpider):
    name = 'rotternet'
    allowed_domains = ['rotter.net']
    start_urls = ['https://rotter.net/cgi-bin/forum/dcboard.cgi']

    website_id = 1941
    language_id = 1926
    custom_settings = {'DOWNLOAD_TIMEOUT': 100}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        'cookie': 'creid=1718220608241864491; _sp_v1_uid=1:245:9af32713-fbb9-4520-84c3-a28c985a79e4; _sp_v1_csv=null; _sp_v1_lt=1:; consentUUID=5ff00936-64b3-4ce1-bdce-8ba8a8557f1d_2; _sp_enable_dfp_personalized_ads=true; wteid_981949533494636=4163862287800248686; _sp_v1_opt=1:login|true:last_id|11:; _gcl_au=1.1.119516265.1638622887; aam_uuid=62772577165203383114310930004637011186; AAMC_iqdigital_0=REGION|11; __gads=ID=148f860e9d08979f:T=1638622904:S=ALNI_MbIjQMJCsEW8bZiPWlqRd-6lmP3jA; mako_fpc_id=4cd8626c-7338-4435-be3b-cd4eb88b36e3; OB-USER-TOKEN=1a9d2419-4585-457e-a23e-f103e94f60bd; atbpdid=be0408f5-61f0-415d-aa24-109df9f5933c; _uetvid=2d7f5500566a11ecae174d97591c44cb; _ga_906VDXTVLC=GS1.1.1638777457.1.1.1638777478.0; _ga=GA1.2.1563856665.1638622898; tika=0d5d848ykwvtoamy; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbKKRmbkgRgGtbE6MUqpIGZeaU4OkF0CVlBdi1tCSYd2BkKlRpWNFGWxAAqrBRCeAgAA; euconsent-v2=CPQ4docPQ4docAGABCDEB4CsAP_AAAAAAARoG6gR5DpFTWFAQXxZQuNgGIQUUMAEAGQCBACBAiABAAEQYAQA0kACMASABAACAAAAIBIBAAAEDAAAAAAAAAAEAACgAAAAgAAIIAAAABEAAAIAAAIIAAAAAAAAAAABAAAAmACQAoZCAEAABAAQQAAAACAAAA8JAgAAWABUADIAHAAQAAyABoADyAIgAigBMACeAG8AOYAfgBCACGAFKAMMAZQA1QB7QD8AP0AigBHACUgGKAPQAhsBeYDBgGnAN1CAAwASAJWAZCGgCABcAEMAPwBjAiAEAIYAfggACACQVAFACYAFwAfgBHAF5jIAgATAB-AEcAXmOgUAALAAqABkADgAIAAZAA0AB5AEQARQAmABPAC4AGIAN4AcwA_ACGAEwAKUAWIAwwBlADRAHtAPwA_QCKAEWAI4ASkAuoBigD0AIbAReAvMBgwDGAGWANOAbqOAFAAXABIAF0AMgBCACMgGBAPIAlYBkJCAcAAsADIATAAuABiADeALEAfgBFACOAEpAMUAegBbRAACARklASAAWABkADgAPAAiABMAC4AGIAQwApQBqgD8AI4AXUAxQCLwF5gMsJABAALgBkAIyAlYpAeAAWABUADIAHAAQAAyABoADyAIgAigBMACeAFIAMQAcwA_ACGAFKALEAZQA0QBqwD8AP0AiwBHACUgHoAReAvMBjADdSgAcAC4AJAAyAE7ALqAYoA8gAAA.YAAAAAAAAAAA; _sp_v1_consent=1!1:1:1:0:0:0; zonconsent=2021-12-08T04:07:07.099Z; iom_consent=010fff0fff&1638936430113; wt_fa=lv~1639210003293|1654762003293#cv~7|1654762003294#fv~1638622874781|1654174874781#vf~2|1654762003291#; AMCVS_41833DF75A550B4B0A495DA6@AdobeOrg=1; c1_to_wt=1718220608241864491; _gid=GA1.2.1637018630.1639210007; s_cc=true; wtsid_981949533494636=1; POPUPCHECK=1639296410081; emqsegs=e0,e1yp,e1p,e4,e7o,e3m,e2b0,e2aw,e4d,e33,e1wj,e30,e6b,ea,e67,e3n,e2c,eky,e1r,e6u,e2av,e3w,e1hf,e2h6,e1m,e4y,e3s,e1wt,e9h,e71,e78,e1sj,e4b,e82,e1,e1s,e7n,e7c,e77,e9g,e8,e64,ekt,e4z,e34,e1o,e54,e8b,e1ii,e3o,e4w,e2h7,e7p,e3h,e1gs,e3a,e3u,e1wm,e38,e1wi,e1wr; adp_segs=e0,e1yp,e1p,e4,e7o,e3m,e2b0,e2aw,e4d,e33,e30,e6b,ea,e67,e3n,e2c,eky,e1r,e6u,e2av,e3w,e2h6,e1m,e4y,e3s,e9h,e71,e78,e4b,e1,e1s,e7n,e77,e9g,e8,e64,e4z,e34,e1o,e54,e8b,e3o,e4w,e2h7,e7p,e3h,e3a,e3u,e38; wt3_sid=;981949533494636; AMCV_41833DF75A550B4B0A495DA6@AdobeOrg=-1124106680|MCIDTS|18973|MCMID|63252086840901604454254094686745590344|MCAAMLH-1639843953|11|MCAAMB-1639843953|6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y|MCOPTOUT-1639246353s|NONE|MCSYNCSOP|411-18973|vVersion|5.2.0|MCCIDH|1532739836; id5id.1st= { "created_at": "2021-12-04T13:02:31Z", "id5_consent": true, "original_uid": "ID5*xi-uR1SBI91WOWTQ6BkoIWNjt1nn-lWkUCb5U_0vOokBkR96m3G0uHbdV8sKuLYBAZKnq87y_hQfeE1O6U4xiQGTHCA6afjy8m2opzibvHMBlM3WNV54nQPzdbS7UHxqAZVu6cqk-jS8LmQ1egmF9wGW0SAsijzyLMMtWUZkORgBlx2o42LEMhVe0SYEgUK3AZg6wvsMqq5fVjd1z6JuygGZEd6AL34WAsXedSaCSiQBmvpxV_0ulHEqN2S5mqV7AZudS7PW9omqg_EfXh_7aAGcpGMun337I8_u7-m8ooYBnSQmobKGdDcvb7X4gT1jAZ4g2Hy2GrzCE1AfcIfdTAGfzz3K4Ut3-3_QwpO6ySYBoIHzFYAxyX3DUry8dL3JAaEMzZ5913AZGdOBPhmpSgGixgsVfbkKgKhZXEtd9qQBow8tJ5ABL9rLGyWEJACEAaTanK6ejoRb5pYVxaR_RAGlbMQe3cEv5kGV3vb0AsgBv9a2IK7N41fPptgL93QfAdolhmUNz0zPwax4rUUOAA", "universal_uid": "ID5*srPvqehFrJrsMVhjoleoJIro7jxeLQOrLC1pIXpgtIcBkRPFI-UstGo1OjJwmMhSAZJGfu99VlzpODQFAUj0mgGTyb5HGtaBS4r4hT1lSxcBlDXJ7Vbke3MiHURj5FfoAZWWTlCKK1_e-6Zz55cdRQGW8a08gxgSxNffZMFzxWwBl7OfvkCZ4OfECI2V7YquAZh_OB-yY8UT3-bwVXf4-QGZMUg3yd5IM8CDg5MnNmYBmjp6z6c9Ug6xu5xJcUqoAZtxmJhQlpyh95E7GP5UHgGcWY6gorLXLhwiPN1R93sBndX07QyYRXQEaDsaf4UlAZ5EmPXgNBwRb-Ji0jjE-wGfQom7KabEBbjYFjje3AYBoDSj9qhmKprJD7-NtKPhAaH1YHu5-6hkMJTWbUBTvwGi74DcSj_APNDNTXkzZpsBo6mxrNPq9L8PPWDefdYhAaTlL9OgXtQ7Fof1wTzXVgGl-KtlyG5UtzhZIH69FcsBv3wEYgkGQLzorShgqtk4AdqmMZo2UoPep4ZhEYM-4Q", "signature": "ID5_ARMHNUSbeCFLO81v4-tIMNNBClUKG64VRH4hut4kVRxiHnCuR7wd7PuaNDWlzSFow8_KDqvILgFjWNh6WqzA9NM", "link_type": 2, "cascade_needed": true, "privacy": { "jurisdiction": "gdpr", "id5_consent": true}}; id5id.1st_last=1639239156058; id5id.1st_123_nb=0; wt3_eid=;981949533494636|2163886894889454138#2163924119981604643; _k5a={"u":[{"uid":"vIH8ZtO0JC8DThYH","ts":1639214473},1639304473],"_cl":[{"u":"https://www.zeit.de/thema/index","c":"desktop","ptp":"topic-overview","psn":"gesellschaft","ptl":"Was gerade wichtig ist","par":"","ptg":"","pctg":["online"],"pd":"","tu":"https://www.zeit.de/thema/register/0-9","cr":0,"cp":0,"po":"","ps":"","ct":"31300.8"},1639241320]}; zon_count=eyJvbmxpbmUiOjQzLCJwcmludCI6MjksIm5vbmUiOjB9; _dc_gtm_UA-18122964-8=1; adbprevpage=/thema/register/0-9; s_sq=[[B]]; cto_bundle=d09Vml9FdjE2ZmwwZG1qeUJBeWRENjBwZlhvRDR0RXFXRXozWlhkWVhXRCUyRno0OUdFeU9JREE4MDlaREJlbnZ5RDFrUlJkTFdMamg4Wmd3TmhKOFN4VFBGYjlKQjBxd09PQXZaamZNJTJCbnBpUXNGR0VsblglMkJtTiUyQlpEaGRuUSUyQk13VTY3VzJDdDg4cnlYTTlWdWdObDI3aFdJT05BJTNEJTNE; _gat=1; ioam2018=0019da5a9a84bc25f61ab6692:1666011668910:1638622868910:.zeit.de:312:zeitonl:homepage/bild-text:noevent:1639241439431:s2ihtd; wt_fa_s=start~1|1670777440591#; kickerticker=49zg6knDrOerMMSrMZ5Og5O4nATbIVma; _sp_v1_data=2:415635:1638622872:0:271:0:271:0:0:_:-1; adb_dslv=1639241441555; wt_rla=981949533494636,34,1639240988028;821266747973781,1,1638623976001'
    }
    proxy = '02'

    def parse(self, response):
        td_obj_list = response.css('div[dir=RTL] table td[align=RIGHT][width]')
        for td_obj in td_obj_list:
            page_link = td_obj.css('b a::attr(href)').extract_first()
            meta = {'data': {'category1': td_obj.css('b font').xpath('string(.)').extract_first().strip()},
                    'page': int(1),  # 用于parse_page的翻页
                    'link': page_link
                    }
            yield scrapy.Request(page_link, callback=self.parse_page,meta=deepcopy(meta),headers=self.headers)

    def parse_page(self, response):
        flag = True
        td_obj_list = response.css('table[dir=rtl] tr[bgcolor] td[align=right][valign]')
        if td_obj_list:
            if self.time is None:
                for td_obj in td_obj_list:
                    response.meta['data']['title'] = td_obj.css('a').xpath('string(.)').extract_first().strip()
                    item_link = td_obj.css('a::attr(href)').extract_first()
                    yield scrapy.Request(url=item_link, callback=self.parse_item,meta=deepcopy(response.meta),headers=self.headers)
            else:
                last_pub = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(response.css('table[dir=rtl] tr[bgcolor] td[align=right][valign] + td > font').xpath('string(.)').extract()[-1].strip().split('\n')[0],'%d.%m.%y %H:%M'))
                if self.time < DateUtil.formate_time2time_stamp(last_pub):
                    for td_obj in td_obj_list:
                        response.meta['data']['title'] = td_obj.css('a').xpath('string(.)').extract_first().strip()
                        item_link = td_obj.css('a::attr(href)').extract_first()
                        yield scrapy.Request(url=item_link, callback=self.parse_item, meta=deepcopy(response.meta),headers=self.headers)
                else:
                    self.logger.info("时间截止")
                    flag = False
            if flag:
                response.meta['page'] += 1
                detail_link = response.meta['link'] + '&mm=' + str(response.meta['page']) +'&archive='
                yield scrapy.Request(detail_link, callback=self.parse_page, meta=deepcopy(response.meta),headers=self.headers)

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.meta['data']['title']
        item['pub_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(' '.join(response.css('table tr[bgcolor] td[align=LEFT][valign=top] > font').xpath('string(.)').extract()[0].split()[-2:]),'%H:%M %d.%m.%y'))
        item['category1'] = response.meta['data']['category1']
        item['category2'] = None
        body = response.css('table [bgcolor=\#FDFDFD]')[0].css('font.text15 b::text, font.text15 p::text, font.text15::text, font.text15 font::text, font.text15 font::text').extract()
        if body == None:
            body = response.css('table [bgcolor=\#FDFDFD]')[0].css('font.text15 font').xpath('string(.)').extract()
        item['body'] = '\n'.join([i.strip() for i in body if i.strip() != ''])
        item['images'] = [i if 'http' in i else 'https://rotter.net'+i for i in response.css('table [bgcolor=\#FDFDFD]')[0].css('font.text15 img::attr(src)').extract()]
        item['abstract'] = item['body'].split('\n')[0]
        yield item

