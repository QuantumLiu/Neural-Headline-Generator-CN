#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:50:46 2017

@author: quantumliu
"""

import re,requests,pickle
#爬取网易新闻，直接指定数量
def get_news(num=10000):
    dic_re={}
    dic_news={}
    dic_re['title']=r'"title":"([\s\S]*?)","'
    dic_re['url']=r'"url":"(.*?)"'
    dic_re['digest']=r'"digest":"([\s\S]*?)",'
    text=requests.get('http://3g.163.com/touch/article/list/BBM54PGAwangning/0-'+str(num)+'.html').text.replace('\\"','"')
    dic_news={k:re.findall(v,text) for k,v in dic_re.items()}
    return [dict(zip(dic_news.keys(),a)) for a in zip(*list(dic_news.values()))]
if __name__=='__main__':
    news=get_news(10000)
    with open('163_news.pkl','wb') as f:
        pickle.dump(news,f)
    