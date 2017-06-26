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
def pad(l,m=12):
    if len(l)<m:
        l+=[(l if l else [''])[-1]]*(m-len(l))
    return l
def parse(page):
    r_start=r'&start=(\d*?)&'
    start=int(re.findall(r_start,page)[0])
    keys=['image','title','description_arabic']
    img_root='http://www.aljazeera.net/File/GetImageCustom/'
    r_root=r'<metatag.{key} type=[^>]*?><!\[CDATA\[(.*?)\]\]></metatag.{key}>'
    r_url=r'<url type=\'\'><!\[CDATA\[(.*?)\]\]></url>'
    r_dic={k:r_root.format(key=k) for k in keys}
    r_dic['url']=r_url
    ua={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    res=requests.get(page,headers=ua)
    res.encoding='utf-8'
    data={k:re.findall(v,res.text) for k,v in r_dic.items()}
    data['image']=[img_root+n for n in data.get('image')]
    keys=list(data.keys())
    datas=[data.get(key) for key in keys]
    m=max(map(lambda x:len(x),datas))
    print('Crawling : {start} to {end}'.format(start=start,end=start+m))
    datas=[pad(l,m) for l in datas]
    z=zip(*datas)
    articels=[dict(zip(keys,d)) for d in z]
    print('Got {l} articels'.format(l=len(articels)))
    if not articels:
        print('Error,no articels got.\nxml text: '+res.text)
        print(''.join([data.get(key) for key in keys]))
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
    ars=crawl_s()
    print('Crawling finished, got {n} articels, cost :{dur} seconds.'.format(n=len(ars),dur=time.time()-s))
    with open('alj.pkl','wb') as f:
        pickle.dump(ars,f)
