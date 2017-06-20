#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 19:52:03 2017

@author: quantumliu
"""

import requests,re
import pickle
from multiprocessing import Pool,cpu_count,freeze_support
#爬取新浪新闻的标题、摘要、网址，约5w条
def get_page(num):
    #helper函数，格局页数生成固定格式的页面地址
    return ("http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1""||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&""format=json&page={}&callback=newsloadercallback").format(str(num))
def parse_page(num):
    #分析、爬取信息，返回一个字典的列表，字典的key是title，url，keywords，abstract
    page_url=get_page(num)
    news={}
    page=requests.get(page_url)
    print('Crawling page :',num)
    text=page.text.encode().decode('unicode-escape')
    dic_re={}
    dic_re['title']=r'"title":"(.*?)",'
    dic_re['url']=r'"url":"(.*?)"'
    dic_re['keywords']=r'"keywords":"(.*?)",'
    dic_re['abstract']=r'"ext5":"([\s\S]*?)",'
    news={k:re.findall(v,text) for k,v in dic_re.items()}
    news['url']='*&*'.join(news['url']).replace('\\','').split('*&*')#去掉html中的\/字符
    news_list=[dict(zip(news.keys(),a)) for a in zip(*list(news.values()))]
    print('Number of news:',len(news_list))
    return news_list
def max_page(start=2500,stride=10):
    #寻找最大页数，从start按stride递减
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
    #多线程爬取
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
    news=crawl_p(2490)
    with open('sina_news.pkl','wb') as f:
        pickle.dump(news,f)
    