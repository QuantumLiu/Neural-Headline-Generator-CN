# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:18:30 2017

@author: Quantum Liu
"""

import re
import requests
from multiprocessing import Pool,cpu_count,freeze_support
import traceback
import time
#爬取搜狐新闻的全部标题约20w条
def get_num_page():
    #获取最大页数
    return int(re.findall(r'<p class="f"><span class="c3"> \[\d*?/(.*?)\]</span>',requests.get('http://m.sohu.com/cr/2/?_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2').text)[0])
def get_titles(page=1,root=['http://m.sohu.com/cr/2/?page=','&_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2']):
    #提取某一页面的标题列表
    root=(['http://m.sohu.com/cr/2/?page=','&_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2'] if not root else root)
    dic_re={}
    dic_re['title']=r'<p><i class="s">·</i><a href=".*?">(.*?)</a></p>'
    dic_re['url']=r'<p><i class="s">·</i><a href="(.*?)">.*?</a></p>'
    headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    text=requests.get(str(page).join(root),headers=headers).text
    dic_news={k:re.findall(v,text) for k,v in dic_re.items()}
    print('Crawling page '+str(page)+' successfully..')
    news_list=[dict(zip(dic_news.keys(),a)) for a in zip(*list(dic_news.values()))]
    return news_list
def crawl_p(num_page=100,root=[]):
    #多线程爬取
    freeze_support()
    pool=Pool(max(cpu_count(),4))
    results=[]
    for page in range(1,num_page+1):
        results.append(pool.apply_async(get_titles,(page,root)))
    news=sum([result.get() for result in results],[])
    pool.close()
    pool.join()
    return news
if __name__ == '__main__':
    st=time.time()
    utext=crawl_p(num_page=get_num_page())
    dur=time.time()-st
    num=len(utext.split('\n'))
    print('Crawled '+str(num)+' title in '+str(dur)+' seconds.\nAverage cost: '+str(num/dur)+'title/s.')
    with open('sohu_title.txt','w') as f:
        f.write(utext)
