# -*- coding: utf-8 -*-

from urllib import request
import re
import os

request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}

city_home_pages = []
city_ids = []
dirname = 'mafengwo_notes/'

#布隆过滤器需要更新
download_bf = []

def download_city_notes(id):
    for i in range(1, 2):
    	#遍历城市每个页面
        url = 'http://www.mafengwo.cn/yj/%s/1-0-%d.html' % (id, i)
        if url in download_bf:
            continue
        print('open url %s' % (url))
        #为避免空页加入，即不存在的页面，将以下命令下移
        #download_bf.add(url)
        download_bf.append(url)
       
        #确定每个城市的单页面上存在的游记链接数
        req = request.Request(url, headers = request_headers)
        response = request.urlopen(req)
        htmlcontent = response.read().decode('utf-8')
        city_notes = re.findall('href="/i/\d{7}.html', htmlcontent)
        print(city_notes)
        # 如果导航页错误，该页的游记数为0，则意味着 1-0-xxx.html 已经遍历完，结束这个城市
        if len(city_notes) == 0:
            return


        for city_note in set(city_notes):
            try:
                city_url = 'http://www.mafengwo.cn%s' % (city_note[6:])
                if city_url in download_bf:
                    continue
                print('download %s' % (city_url))
                req = request.Request(city_url, headers=request_headers)
                response = request.urlopen(req)
                html = response.read()

                filename = city_url[7:].replace('/', '_')
                with open("%s%s" % (dirname, filename), 'wb+') as fobj:
                   fobj.write(html)
                # download_bf.add(city_url)
                download_bf.append(url)
            except Exception as Arguments:
                print(Arguments)
                continue

# 检查用于存储网页文件夹是否存在，不存在则创建
if not os.path.exists(dirname):
    os.makedirs(dirname)

try:
    # 下载目的地的首页
    req = request.Request('http://www.mafengwo.cn/mdd/', headers=request_headers)
    response = request.urlopen(req)
    htmlcontent = response.read().decode('utf-8')
    print(htmlcontent)
    # 利用正则表达式，找出所有的城市主页
    city_re = re.compile(r"/travel-scenic-spot/mafengwo/\d{5}.html")
    city_home_pages = re.findall(city_re, htmlcontent)
    print(city_home_pages)
    # 通过循环，依次下载每个城市下的所有游记
    for city in city_home_pages:
        city_ids.append(city[29:34])
        download_city_notes(city[29:34])
        break
except request.HTTPError as Arguments:
    print(Arguments)
except Exception as Arguments:
    print(Arguments)