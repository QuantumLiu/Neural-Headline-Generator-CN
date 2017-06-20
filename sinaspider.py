#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 19:52:03 2017

@author: quantumliu
"""

import requests,re
import os,time,traceback
import pickle
from multiprocessing import Pool,cpu_count,freeze_support
def get_page(num):
    return ("http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1""||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&""format=json&page={}&callback=newsloadercallback").format(str(num))
def parse_page(num):
    page_url=get_page(num)
    news={}
    page=requests.get(page_url)
    print('Crawling page :',num)
    text=page.text.encode().decode('unicode-escape')
    rs={}
    rs['title']=r'"title":"(.*?)",'
    rs['url']=r'"url":"(.*?)"'
    rs['keywords']=r'"keywords":"(.*?)",'
    rs['abstract']=r'"ext5":"([\s\S]*?)",'
    for r in rs.keys():
        news[r]=re.findall(rs[r],text)
    news['url']='*&*'.join(news['url']).replace('\\','').split('*&*')
    news_list=[{'title':t,'url':u,'keywords':k,'abstract':a} for t,u,k,a in zip(news['title'],news['url'],news['keywords'],news['abstract'])]
    print('Number of news:',len(news_list))
    return news_list
def max_page(start=2500,stride=10):
    r_count=r'"count":"(.*?)",'
    for num in list(range(0,start,stride))[::-1]:
        text=requests.get(get_page(num)).text.encode().decode('unicode-escape')
        l=re.findall(r_count,text)
        count=(int(l[0]) if l else 0)
        if count:
            print('Max page :',num)
            return num
    raise 'Eorror:No max page found!'
    return 0
def crawl_p(num_page=0):
    if not num_page:
        num_page=max_page()
    results=[]
    freeze_support()
    mp=Pool(min(8,max(cpu_count(),4)))
    for num in range(1,num_page+1):
        results.append(mp.apply_async(parse_page,(num,)))
    mp.close()
    mp.join()
    news=sum([result.get() for result in results],[])
    return news
if __name__=='__main__':
    news=crawl_p()
    with open('sina_news.pkl','wb') as f:
        pickle.dump(news,f)
    