import scrapy
from tutorial.settings import USER_AGENT_LIST
from tutorial.utils import get_middle_str
import random
import json
from bs4 import BeautifulSoup
from tutorial.items import TutorialItem
class WanSpider(scrapy.Spider):
    name = "wan"

    def start_requests(self):
        urls = [
            'http://eid.csrc.gov.cn/ipo/1010/index_{}_f.html'.format(i) for i in range(1,51)
        ]
        types = ['03','06']
        body = {
            'prodType3':'',
            'prodType4':'',
            'keyWord':'',
            'keyWord2':'关键字',
            'selBoardCode':'types',
            'selCatagory2':'',
            'startDate':'2021-05-27',
            'startDate2':'请输入开始时间',
            'endDate':'',
            'endDate2':'请输入结束时间'
        }
        for t in types:
            body['selBoardCode'] = t
            for url in urls:
                print(url)
                ran = random.randint(0,len(USER_AGENT_LIST)-1)
                yield scrapy.Request(url=url,callback=self.parse,
                                    headers={'User-Agent':USER_AGENT_LIST[ran]},
                                    dont_filter=True,
                                    method='POST',body=json.dumps(body))

    def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        for i in trs:
            attrs = i.attrs
            if attrs.get('onclick'):
                onclick = attrs.get('onclick')
                pdf_url = get_middle_str(onclick,'downloadPdf1\(\'','\',')
                if pdf_url.startswith('http'):
                    ran = random.randint(0,len(USER_AGENT_LIST)-1)
                    yield scrapy.Request(url=pdf_url,callback=self.parse_pdf,
                                    headers={'User-Agent':USER_AGENT_LIST[ran]},
                                    dont_filter=True,
                                    method='GET')
                    
                else:
                    with open('log.txt','a',encoding='utf-8') as f:
                        f.write(onclick+'\n')

    def parse_pdf(self, response):
        pdf = response.body
        url = response.url
        yield TutorialItem(pdf=pdf,url=url)