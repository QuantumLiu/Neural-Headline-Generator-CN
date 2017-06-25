# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 21:22:32 2017

@author: Quantum Liu
"""

import numpy as np
def seq2str(seq,dic):
    return ' '.join([dic.get(c,'') for c in list(np.argmax(seq,-1))])
def dic_inv(dic):
    return {v:k for k,v in dic.items()}