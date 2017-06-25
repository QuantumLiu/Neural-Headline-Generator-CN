# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 21:20:16 2017

@author: Quantum Liu
"""

import pickle,traceback
from predict import dic_inv,seq2str
import tensorflow as tf
from models import r2r
from generators import data_gen,get_params
batch_size=32
with open('dic.pkl','rb') as f:
    udic=pickle.load(f)
    dic_len=len(udic)
idic=dic_inv(udic)
val_filename='data_val.h5'
model_name='r2r'
input_length,ouput_length=get_params(val_filename)
val_gen=data_gen(val_filename,dic_len,batch_size=batch_size)
with tf.device('/gpu:0'):
    model=r2r(dic_len=dic_len,input_length=input_length,output_length=ouput_length,hidden=512)
    model.load_weights(model_name+'.h5')
    results=model.predict_generator(generator=val_gen,steps=10)
    strings=[seq2str(s,idic) for s in results]
    for s in strings:
        print(s)
