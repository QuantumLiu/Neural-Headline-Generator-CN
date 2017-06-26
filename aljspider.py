# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 23:34:07 2017

@author: Quantum Liu
"""

import re,requests,traceback,pickle
from multiprocessing import Pool,cpu_count,freeze_support
class category():
    def __init__(self,name,url):
        self.name=name
        self.url=url
        self.ua={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        try:
            self.res=requests.get(self.url,self.ua)
        except:
            traceback.print_exc()
        self.params,self.max_page=get_params(self.res)
        self.lm_root='http://www.aljazeera.net/Services/GetLoadMoreArticlesFromNewsSite?SectionID={sectionId}&EntityID={eId}&ResourceID={oId}'.format(**self.params)+'&PageNo={n}&PageSize=11&layout=~/Views/Shared/News/shared/areas/services/LoadMoreNews.cshtml'
        self.lms=[self.lm_root.format(n=n) for n in range(self.max_page)]
        self.articels=[]
        self.log=''
    def cur_no(self,lm):
        return int(re.findall(r'&PageNo=(\d*?)&PageSize',lm)[0])
    def process(self,lm):
        r_title=r'<h2><a href="/news.*?">(.*?)</a></h2>'
        r_url=r'<h2><a href="/news(.*?)">.*?</a></h2>'
        r_ab=r'<p class="greta">(.*?)</p>'
        r_img=r'<img src="(.*?)" alt="[\s\S]*?">'
        news_root='http://www.aljazeera.net/news'
        img_root='http://www.aljazeera.net'
        print('Crawling category : {cat},page {cur} of {m} .'.format(cat=self.name,cur=self.cur_no(lm),m=self.max_page))
        try:
            text=requests.get(lm,headers=self.ua).text
            titles,abstracts=([s.replace('&quot;','"').strip() for s in re.findall(r,text)] for r in [r_title,r_ab])
            urls=[news_root+s.replace('&quot;','"').strip() for s in re.findall(r_url,text)]
            imgs=[img_root+s.replace('&quot;','"').strip() for s in re.findall(r_img,text)]
            return [{'title':t,'abstract':ab,'url':u,'img':i} for t,ab,u,i in zip(titles,abstracts,urls,imgs)]
        except TypeError:
            log=traceback.format_exc()
            self.log+=log
            print(log)
            return []
    def crawl_s(self):
        self.articels+=[self.process(lm) for lm in self.lms]
        return self.articels
    def crawl_p(self):
        results=[]
        freeze_support()
        mp=Pool(min(8,max(cpu_count(),4)))
        for lm in self.lms:
            results.append(mp.apply_async(self.process,(lm,)))
        mp.close()
        mp.join()
        self.articels+=sum([result.get() for result in results],[])
        return self.articels
    def update(self):
        new_lm=self.lm_root.format(n=1)
        new_articels=self.process(new_lm)
        self.articels=new_articels+self.articels
        return new_articels
class aljazeera():
    def __init__(self):
        self.categories={name:category(name,url) for name,url in get_cats().items()}
        self.articels=[]
    def crawl(self,mode=0):
        if mode==0:#parallel in cats
            freeze_support()
            mp=Pool(min(8,max(cpu_count(),4)))
            for cat in self.categories.values():
                mp.apply_async(cat.crawl_s,())
            mp.close()
            mp.join()
        elif mode==1:#serial in cats
            for cat in self.categories.values():
                cat.crawl_p()
        elif mode==2:#serial
            for cat in self.categories.values():
                cat.crawl_s()
    def update(self,mode):
        if mode==0:#parallel in cats
            freeze_support()
            mp=Pool(min(8,max(cpu_count(),4)))
            for cat in self.categories.values():
                mp.apply_async(cat.update,())
            mp.close()
            mp.join()
        elif mode==1:#serial
            for cat in self.categories.values():
                cat.update()
    def get_articels(self):
        self.articels=sum([cat.articels for cat in self.categories],[])+self.articels
        return self.articels
    def save(self,path='aljweb.pkl',dump_all=True):
        with open(path,'wb') as f :
            if dump_all:
                print('Dumping aljazeera web site object...')
                pickle.dump(self,f)
            else:
                print('Dumping aljazeera web site object...')
                pickle.dump(self.categories,f)
def get_cats(portal='http://www.aljazeera.net/portal',root='http://www.aljazeera.net'):
    headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    r_sec=r'<a href="/news">([\s\S]*?)<div class="rightMenu borderedRight">'
    r_cat_u=r'<li><a href="(/news/.*?)">.*?</a></li>\r\n'
    r_cat_n=r'<li><a href="/news/(.*?)">.*?</a></li>\r\n'
    res=requests.get(portal,headers=headers)
    t=''.join(re.findall(r_sec,res.text))
    cats_dic=dict(zip(re.findall(r_cat_n,t),[root+u for u in re.findall(r_cat_u,t)]))
    print('There are :'+str(len(cats_dic))+' categories.\n',cats_dic)
    return cats_dic
def get_params(cat_res):
    p_l=['eId','oId','sectionId']
    r_root=r'<input id="{param}" type="hidden" value="(.*?)"'
    params={p:re.findall(r_root.format(param=p),cat_res.text)[0].strip() for p in p_l}
    tm=dict(cat_res.headers.items()).get('Cache-Control')[8:]
    max_page=int(tm if tm else 0)
    return params,max_page
if __name__=='__main__':
    alj=aljazeera()
    alj.crawl()
    alj.save()