#-*- coding:utf-8 -*-
from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import sys
import collections
import os
import time
import random
import userAgent

class download_images(object):
	def __init__(self, target, uAgent):
		self.__target_url = target
		self.__user_agent = uAgent

	#获取每个页面的图片地址
	def getManyGirlurls(self):
		#建立请求
		target_req = request.Request(url = self.__target_url, headers = self.__user_agent)
		#响应
		target_response = request.urlopen(target_req)
		#获取html信息
		target_html = target_response.read().decode('gbk', 'ignore')
		#创建BeautifulSoup对象,还原html格式
		target_soup = BeautifulSoup(target_html, 'lxml')
		#搜索文档树，即寻找target_soupb包含的所有子树，本阶段是目录即div class="listmain"
		listmain_trees = target_soup.find_all('ul', attrs = {'class':'product01'})
		listmain_newtrees = BeautifulSoup(str(listmain_trees), 'lxml')
		listmain_urls = listmain_newtrees.find_all('a', attrs = {'target':'_Blank'})
		getimageUrlDIct = collections.OrderedDict()
		for each in listmain_urls:
			each = BeautifulSoup(str(each),'lxml')
			getimageUrlDIct[each.a['alt']] = each.a['href']
		# listmain_bstrees = BeautifulSoup(str(listmain_trees), 'lxml')
		return getimageUrlDIct

	#获取每个章节中的内容，传入参数为url,返回值为处理后的文档
	def getSinglegirlUrls(self, url):
		#创建请求
		getContents_req = request.Request(url = url, headers = self.__user_agent)
		getContents_response = request.urlopen(getContents_req)
		#读取内容
		getContents_html = getContents_response.read().decode('gbk', 'ignore')
		#创建BeautifulSoup对象
		getContents_soup = BeautifulSoup(getContents_html, 'lxml')
		getContents_texts = getContents_soup.find_all('img')
		getimgeSurls = []
		for url in getContents_texts:
			getimgeSurls.append(url.attrs['src'])
		return getimgeSurls

	#确定要爬的页数
	def want_pages(self, num):
		pass

	#写文档
	def writeDocument(self, suburl, user):
		html = request.Request(suburl, headers = user)
		gethtml = request.urlopen(html)
		with open('images/' + key + suburl.split('/')[-1], 'wb') as fobj:
			fobj.write(gethtml.read())
		time.sleep(1)

if __name__ == '__main__':
	num = 2
	for i in range(1, num + 1): 
		target = 'http://www.169tp.com/guoneimeinv/list_5_%d.html'%i
		uIndex = random.randint(1, len(userAgent.UserAgents))
		newuser = {'User-Agent':userAgent.UserAgents[uIndex]}

		classImage = download_images(target, newuser)
		mUrls = classImage.getManyGirlurls()
		if 'images' not in os.listdir():
			os.makedirs('images')

		for key, value in mUrls.items():
			time.sleep(1)
			Surls = classImage.getSinglegirlUrls(value)
			for suburl in Surls:
				print(suburl)
				print(key+ suburl.split('/')[-1])
				classImage.writeDocument(suburl, newuser)
	print('Done!')