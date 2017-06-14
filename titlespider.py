# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:18:30 2017

@author: Quantum Liu
"""

import re
import requests
from multiprocessing import Pool,cpu_count,freeze_support
import traceback
import os
import time
def get_num_page():
    return int(re.findall(r'<p class="f"><span class="c3"> \[\d*?/(.*?)\]</span>',requests.get('http://m.sohu.com/cr/2/?_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2').text)[0])
def get_titles(page=1,root=['http://m.sohu.com/cr/2/?page=','&_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2']):
    root=(['http://m.sohu.com/cr/2/?page=','&_smuid=BKCjjYm5FlosZV5aowq5Ze&mv=2'] if not root else root)
    try:
        text='\n'.join(re.findall(r'<p><i class="s">·</i><a href=".*?">(.*?)</a></p>',requests.get(str(page).join(root),headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}).text))+'\n'
        print('Crawling page '+str(page)+' successfully..')
    except:
        text='error'
        traceback.print_exc()
    return text
def crawl_p(num_page=100,root=[]):
    freeze_support()
    pool=Pool(max(cpu_count(),4))
    results=[]
    for page in range(1,num_page+1):
        results.append(pool.apply_async(get_titles,(page,root)))
    return ''.join([result.get() for result in results])
if __name__ == '__main__':
    st=time.time()
    utext=crawl_p(num_page=get_num_page())
    dur=time.time()-st
    num=len(utext.split('\n'))
    print('Crawled '+str(num)+' title in '+str(dur)+' seconds.\nAverage cost: '+str(num/dur)+'title/s.')
    with open('sohu_title.txt','w') as f:
        f.write(utext)
