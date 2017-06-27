# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:00:01 2017

@author: Quantum Liu
"""
#crawling by search an arabic character 'ا' which has the highest frequency of use.
import re,requests,traceback,pickle,time
from multiprocessing import Pool,cpu_count,freeze_support
def get_maxindex(page,per=12):
    r_total=r'<total>(\d*?)</total>'
    ua={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    res=requests.get(page,headers=ua)
    res.encoding='utf-8'
    total=int(re.findall(r_total,res.text)[0])
    max_index=int(total/per)*per
    print('Max index : '+str(max_index))
    return max_index
def it_page(per=12):
    root='http://search1.aljazeera.net/search.htm?all=%D8%A7&output=xml&hitsPerPage=12&start={start}&exfilter=metatag.site:57258A24E91A42B0B2399DCCF49CF8C1&filter=-id:*learning.aljazeera*&return=content_arabic;url;metatag.publishdt;metatag.title;metatag.site;metatag.channel;metatag.image;metatag.newimage;metatag.newstopics;metatag.description_arabic'
    max_index=get_maxindex(root.format(start=48),per)
    pages=(root.format(start=s) for s in range(0,max_index,per))
    return pages
def l2dl(l):
    keys=['title','description_arabic','image','url']
    img_root='http://www.aljazeera.net/File/GetImageCustom/'
    dl=[dict().fromkeys(keys,'')]
    for k,v in l:
        d=dl[-1]
        if not d.get(k,False):
            d[k]=re.sub(r'</*em>','"',(img_root+v if k=='image' else v))
            dl[-1]=d
        else:
            dn=dict().fromkeys(keys,'')
            dn[k]=re.sub(r'</*em>','"',(img_root+v if k=='image' else v))
            dl.append(dn)
    return dl
def parse(page):
    r_start=r'&start=(\d*?)&'
    start=int(re.findall(r_start,page)[0])
    keys=['title','description_arabic','image','url']
    r_data=r'<(?:metatag\.)*?(?:{p})+?[^>]*?><!\[CDATA\[(.*?)\]\]></(?:metatag\.)*?({p})>'.format(p='|'.join(keys))
    ua={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    res=requests.get(page,headers=ua)
    res.encoding='utf-8'
    datas=[(i[1].replace('metatag.',''),i[0]) for i in re.findall(r_data,res.text)]
    articels=l2dl(datas)
    l=len(articels)
    print('Crawling : {start} to {end}'.format(start=start,end=start+l))
    print('Got {l} articels'.format(l=l))
    if not articels:
        print('Error,no articels got.\nxml text: '+res.text)
    return articels
def crawl_s():
    return [parse(p) for p in it_page()]
def crawl_p():
    results=[]
    freeze_support()
    mp=Pool(min(8,max(cpu_count(),4)))
    for page in it_page():
        results.append(mp.apply_async(parse,(page,)))
    mp.close()
    mp.join()
    articels=sum([result.get() for result in results],[])
    return articels
if __name__=='__main__':
    s=time.time()
    ars=crawl_p()
    print('Crawling finished, got {n} articels, cost :{dur} seconds.'.format(n=len(ars),dur=time.time()-s))
    with open('alj.pkl','wb') as f:
        pickle.dump(ars,f)
