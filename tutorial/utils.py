import re
import io
from pdfminer.high_level import extract_text,extract_pages
import requests
import random
from tutorial.settings import USER_AGENT_LIST
from pdfminer.layout import LTChar, LTText
import asyncio

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped
def get_middle_str(content, startStr, endStr):
    #patternStr = r'"ip":"(.*?)","urls"'
    patternStr = r'%s(.*?)%s' %(startStr,endStr)
    p = re.compile(patternStr, re.IGNORECASE)
    m = re.findall(p, content)
    if m:
        return m[0]

def verify_proxy():
    ran = random.randint(0,len(USER_AGENT_LIST)-1)

    proxy = requests.get('http://localhost:5555/random').text
    try:
        r = requests.get('http://weibo.cn',headers={'User-Agent':USER_AGENT_LIST[ran]},proxies={'http':'http://'+proxy})
        if r.status_code == 200:
            return proxy
        else:
            return None
    except:
        return None

def getpdf_content(content):
    # url = 'https://www.apc-paris.com/system/files/file_fields/2022/04/14/apc-trophees-coachcopro-vf.pdf'
    # ran = random.randint(0,len(USER_AGENT_LIST)-1)
    # proxy = verify_proxy()
    # if proxy:
    #     r = requests.get(url,headers={'User-Agent':USER_AGENT_LIST[ran]},proxies={'http':'http://'+proxy})
    # else:
    #     r = requests.get(url,headers={'User-Agent':USER_AGENT_LIST[ran]})
    with io.BytesIO(content) as pdf_file:
        count = 0
        for page_layout in extract_pages(pdf_file):
            count += 1
            for element in page_layout:
                if isinstance(element, (LTChar, LTText)):
                    text = element.get_text().strip()
                    if '系统离职' in text:
                        return count
    return False
