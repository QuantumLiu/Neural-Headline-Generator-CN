#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:27:21 2017

@author: quantumliu
"""
import jieba
import numpy as np
import h5py
def num_sub(text):
    r_date=r'((\d{4}|\d{2})(-|/|.)\d{1,2}\3\d{1,2})|(\d{4}年\d{1,2}月\d{1,2}日)|(\d{1,2}月\d{1,2}日)|(\d{1,2}日)'
    r_num=r'
    def get_utext(news_list):
    return ''.join([n.get('title','')+n.get('abstract','') for n in news_list])
def cut(utext):
    jieba.enable_parallel(32)
    words=jieba.lcut(utext)
    return words
def get_inverse(words):
    return np.unique(np.array(words),return_counts=True,return_inverse=True)