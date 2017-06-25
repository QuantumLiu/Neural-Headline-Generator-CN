# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:41:20 2017

@author: Quantum Liu
"""
import numpy as np
import traceback
import h5py
from keras.utils import to_categorical
def get_params(filename):
    with h5py.File(filename,'r') as f:
        datas,labels=f['x'][:3],f['y'][:3]
    return (datas.shape[1],labels.shape[1])
def data_gen(filename,dic_len,batch_size):
    with h5py.File(filename,'r') as f:
        datas,labels=f['x'][:],f['y'][:]
    nb_samples=datas.shape[0]
    index_max=nb_samples-batch_size
    while 1:
         start=int(np.random.randint(index_max,size=1))
         data=datas[start:start+batch_size]
         label=to_categorical(labels[start:start+batch_size],dic_len)
         label=label.astype('int8').reshape((batch_size,-1,label.shape[-1]))
         yield (data,label)
