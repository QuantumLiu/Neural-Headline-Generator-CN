# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 05:12:21 2017

@author: Quantum Liu
Reference : https://github.com/harveyaot/DianJing/blob/master/scripts/crawl.py
"""
import requests
import json
import time
import random
import datetime
import multiprocessing
import pickle
import argparse


def process(url,cat,call_nums,sleep_time,timestamp):
    articles=[]
    count=0
    while count<call_nums:
        toutiao_data = requests.get(url.format(cat,timestamp,timestamp)).text
        print("Thread:{0} num:{1} of {2} t:{3}".format(cat,count,call_nums,timestamp))
        data = json.loads(toutiao_data)
        if data.get('message') == 'false':
            print('Got {0} articels'.format(len(articles)))
            return articles
        gap = random.randint(sleep_time-2,sleep_time+2)
        time.sleep(gap)
        articles+= [article for article in data.get('data') if article.get('group_id') and article.get('title') and article.get('abstract')]
        timestamp = data.get('next').get('max_behot_time')
        count+=1
    print('Got {0} articels'.format(len(articles)))
    return articles



def crawl_p(sleep_time,call_nums,cats):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--end_date',
                        )

    parser.add_argument('--asstr',
                        default = 'A155E9A289A2822', 
                        help = 'the as component of data url')
    parser.add_argument('--cpstr',
                        default = '5929E208F282CE1', 
                        help = 'the cp component of data url')

    args = parser.parse_args()

    if args.end_date:
        end_date = args.end_date
        end_timestamp = datetime.datetime.strptime(end_date,'%Y%m%d').strftime('%s')
    else:
        end_timestamp = 0

    url = 'http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1'\
            + '&max_behot_time={1}&max_behot_time={2}&tadrequire=true&'\
            + 'as={0}&cp={1}'.format(args.asstr,args.cpstr)

    pool = multiprocessing.Pool(processes=len(cats))
    results=[]
    for cat in cats:
        results.append(pool.apply_async(process,(url,cat,call_nums,sleep_time,end_timestamp)))
    news=sum([result.get() for result in results],[])
    pool.close()
    pool.join()
    return news
if __name__=='__main__':
#sleep time in secs
    sleep_time = 5
    call_nums = 2000
    cats = ['news_tech','news_society','news_entertainment','news_sports','news_car',
            'news_finance','news_game','news_world','news_military','news_history',
            'news_fashion','news_baby','news_food','news_health','news_story',
            'news_travel','new_home','__all__']
    news=crawl_p(sleep_time,call_nums,cats)
    with open('toutiao_news.pkl','wb') as f:
        pickle.dump(news,f)
