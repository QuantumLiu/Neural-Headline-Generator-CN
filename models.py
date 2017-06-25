# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 15:57:18 2017

@author: Quantum Liu
"""

from keras.layers import Input,Embedding,TimeDistributed,LSTM,GlobalMaxPooling1D,GlobalAveragePooling1D,Dense,Bidirectional,Dropout,MaxPooling1D,AveragePooling1D,Conv1D,RepeatVector,BatchNormalization
from keras.models import Sequential,Model
def r2r(dic_len,input_length,output_length,emb_dim=128,hidden=512,deepth=(1,1)):
    model = Sequential()
    model.add(Embedding(input_dim=dic_len, mask_zero=True, output_dim=emb_dim, input_length=input_length))
    for l in range(deepth[0]):
        model.add(LSTM(output_dim=hidden, return_sequences=(False if l==deepth[0]-1 else True)))
    model.add(RepeatVector(output_length))
    model.add(Dropout(0.5))
    for l in range(deepth[0]):
        model.add(LSTM(hidden, return_sequences=True))
    model.add(TimeDistributed(Dense(units=dic_len, activation='softmax')))
    model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['acc'])
    return model
def c2r(dic_len,input_length,output_length,emb_dim=128,hidden=512,nb_filter=64,deepth=(1,1),stride=3):
    model = Sequential()
    model.add(Embedding(input_dim=dic_len, output_dim=emb_dim, input_length=input_length))
    for l in range(deepth[0]):
        model.add(Conv1D(nb_filter,3,activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dropout(0.5))
    model.add(RepeatVector(output_length))
    for l in range(deepth[0]):
        model.add(LSTM(hidden, return_sequences=True))
    model.add(TimeDistributed(Dense(units=dic_len, activation='softmax')))
    model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['acc'])
    return model
