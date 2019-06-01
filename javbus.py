import re
import requests #need install
from pyquery import PyQuery as pq#need install
from lxml import etree#need install
import os
import os.path
import shutil
from bs4 import BeautifulSoup#need install
from PIL import Image#need install
import time
import json

def get_html(url):#网页请求核心
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    getweb = requests.get(str(url),timeout=5,headers=headers).text
    try:
        return getweb
    except:
        print("[-]Connect Failed! Please check your Proxy.")

def getTitle(htmlcode):  #获取标题
    doc = pq(htmlcode)
    title=str(doc('div.container h3').text()).replace(' ','-')
    return title
def getStudio(htmlcode): #获取厂商
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/a/text()')).strip(" ['']")
    return result
def getYear(htmlcode):   #获取年份
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    result2 = str(re.search('\d{4}', result).group(0))
    return result2
def getCover(htmlcode):  #获取封面链接
    doc = pq(htmlcode)
    image = doc('a.bigImage')
    return image.attr('href')
    print(image.attr('href'))
def getRelease(htmlcode): #获取出版日期
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result
def getRuntime(htmlcode): #获取分钟
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find(text=re.compile('分鐘'))
    return a
def getActor(htmlcode):   #获取女优
    b=[]
    soup=BeautifulSoup(htmlcode,'lxml')
    a=soup.find_all(attrs={'class':'star-name'})
    for i in a:
        b.append(i.text)
    return ",".join(b)
def getNum(htmlcode):     #获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
    return result
def getDirector(htmlcode): #获取导演
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/a/text()')).strip(" ['']")
    return result
def getOutline(htmlcode):  #获取演员
    doc = pq(htmlcode)
    result = str(doc('tr td div.mg-b20.lh4 p.mg-b20').text())
    return result

def main(number):
    htmlcode=get_html('https://www.javbus.com/'+number)
    dww_htmlcode=get_html("https://www.dmm.co.jp/mono/dvd/-/detail/=/cid=" + number.replace("-", ''))
    dic = {
        'title': getTitle(htmlcode),
        'studio': getStudio(htmlcode),
        'year': getYear(htmlcode),
        'outline': getOutline(dww_htmlcode),
        'runtime': getRuntime(htmlcode),
        'director': getDirector(htmlcode),
        'actor': getActor(htmlcode),
        'release': getRelease(htmlcode),
        'number': getNum(htmlcode),
        'cover': getCover(htmlcode),
        'imagecut': 1,
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'),)#.encode('UTF-8')
    return js

def main_uncensored(number):
    htmlcode=get_html('https://www.javbus.com/'+number)
    dww_htmlcode=get_html("https://www.dmm.co.jp/mono/dvd/-/detail/=/cid=" + number.replace("-", ''))
    dic = {
        'title': getTitle(htmlcode),
        'studio': getStudio(htmlcode),
        'year': getYear(htmlcode),
        'outline': getOutline(dww_htmlcode),
        'runtime': getRuntime(htmlcode),
        'director': getDirector(htmlcode),
        'actor': getActor(htmlcode),
        'release': getRelease(htmlcode),
        'number': getNum(htmlcode),
        'cover': getCover(htmlcode),
        'imagecut': 0,
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'),)#.encode('UTF-8')
    return js

# def return1():
#     json_data=json.loads(main('ipx-292'))
#
#     title = str(json_data['title'])
#     studio = str(json_data['studio'])
#     year = str(json_data['year'])
#     outline = str(json_data['outline'])
#     runtime = str(json_data['runtime'])
#     director = str(json_data['director'])
#     actor = str(json_data['actor'])
#     release = str(json_data['release'])
#     number = str(json_data['number'])
#     cover = str(json_data['cover'])
#
#     # print(title)
#     # print(studio)
#     # print(year)
#     # print(outline)
#     # print(runtime)
#     # print(director)
#     # print(actor)
#     # print(release)
#     # print(number)
#     # print(cover)
# return1()