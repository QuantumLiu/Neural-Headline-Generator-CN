#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:50:46 2017

@author: quantumliu
"""

import re,requests
def get_news(num=10000):
    r_title=r'"title:"([\s\S]*?)"'
    r_url=r'"url:"(.*?)"'
    text=requests.get('http://3g.163.com/touch/article/list/BBM54PGAwangning/0-'+str(num)+'.html').text
    titles=re.findall(r_title,text)
    urls=re.findall(r_url,text)
    return[{'title':t,'url':u} for t,u in zip(titles,urls)]