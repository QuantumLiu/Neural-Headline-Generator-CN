#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:27:21 2017

@author: quantumliu
"""
import re,pickle
import jieba
import numpy as np
import h5py
def pad_sequences(sequences, maxlen=None, dtype='int32',
                  padding='pre', truncating='pre', value=0.):
    lengths = [len(s) for s in sequences]

    nb_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((nb_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if not len(s):
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x
def num_sub(text):
    r_date=r'((\d{4}|\d{2})(-|/|.)\d{1,2}\3\d{1,2})|(\d{4}年\d{1,2}月\d{1,2}日)|(\d{1,2}月\d{1,2}日)|(\d{1,2}日)'
    r_time=r'(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?|([1-24]\d时[0-60]\d分)|([1-24]\d时)'
    r_num=r'[-+]?[0-9]*\.?[0-9]+'
    return re.sub(r_num,'FLOAT',re.sub(r_time,'TIME',re.sub(r_date,'DATE',text)))
def get_text(news_list,key):
    return ''.join([re.sub(r'\s','',n.get(key,''))+'EOS\n' for n in news_list])
def cut(text,custom_words=['FLOAT','TIME','DATE','EOS']):
    jieba.enable_parallel(32)
    for word in custom_words:
        jieba.add_word(word)
    words=jieba.lcut(text)
    return words
def get_dic(ulist):
    return {j:i for i,j in enumerate(np.unique(np.array(ulist)))}
def get_inverse(words,udic,sp_ch='\n'):
    sentences=[s.strip('<$>').split('<$>') for s in '<$>'.join(words).strip(sp_ch).split(sp_ch)]
    inverse=[]
    for s in sentences:
        inverse.append([udic.get(w,0) for w in s])
    return pad_sequences(inverse,padding='post')
if __name__ == '__main__':
    with open('sina_news.pkl','rb')as f:
        news=pickle.load(f)
    ct=cut(num_sub(get_text(news,'title')))
    ca=cut(num_sub(get_text(news,'abstract')))
    uwords=ca+ct
    udic=get_dic(uwords)
    print('There are ',len(uwords),' words.\n',len(udic),' unique tokens.')
    aa=get_inverse(ca,udic)
    at=get_inverse(ct,udic)
    with h5py.File('data.h5','w') as f:
        f.create_dataset('y',data=aa)
        f.create_dataset('x',data=at)
    print('There are ',aa.shape[0],' samples.')
