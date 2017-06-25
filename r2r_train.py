# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:23:04 2017

@author: Quantum Liu
"""

import pickle
import wechat_utils
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from models import r2r
from generators import data_gen,get_params
wechat=0
load=0
batch_size=32
epochs=50
with open('dic.pkl','rb') as f:
    udic=pickle.load(f)
    dic_len=len(udic)
train_filename='data_train.h5'
val_filename='data_val.h5'
model_name='r2r'
input_length,ouput_length=get_params(train_filename)
train_gen=data_gen(train_filename,dic_len,batch_size=batch_size)
val_gen=data_gen(val_filename,dic_len,batch_size=batch_size)
with tf.device('/gpu:0'):
    model=r2r(dic_len=dic_len,input_length=input_length,output_length=ouput_length,hidden=512)
    model.summary()
    if load:
        model.load_weights(model_name+'.h5')
    if wechat:
        wechat_utils.login()
        model.fit_generator(generator=train_gen,validation_data=val_gen,steps_per_epoch=int(50000/batch_size),validation_steps=int(10000/batch_size),epochs=epochs,callbacks=[ModelCheckpoint(model_name+'.h5',monitor='val_acc',save_best_only=True,save_weights_only=False),wechat_utils.sendmessage(savelog=True,fexten=model_name)])
    else:
        model.fit_generator(generator=train_gen,validation_data=val_gen,steps_per_epoch=int(50000/batch_size),validation_steps=int(10000/batch_size),epochs=epochs,callbacks=[ModelCheckpoint(model_name+'.h5',monitor='val_acc',save_best_only=True,save_weights_only=False)])
