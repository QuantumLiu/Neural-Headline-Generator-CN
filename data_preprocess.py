#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:27:21 2017

@author: quantumliu
"""
import jieba
import numpy as np
import h5py
def get_utext(news_list):
    return ''.join(['*&'+n.get('title','').strip()+'&*'+'*$'+n.get('abstract','').strip()+'$*' for n in news_list])
def cut(utext):
    jieba.enable_parallel(32)
    words=jieba.lcut(utext)
    return words
def get_inverse(words):
    return np.unique(aw,return_counts=True,return_index=True,return_inverse=True)