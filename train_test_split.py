# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 23:37:51 2020

@author: siddh
"""

import os, sys
import shutil

path = r"C:\Users\siddh\Desktop\Training-Data"
train = r"C:\Users\siddh\Desktop\Train_data"
test = r"C:\Users\siddh\Desktop\Test_data"
dirs = os.listdir( path )
train_var = 1
test_var = 1
counter = 1
for root, dirs, files in os.walk(path):
    for name in files:
        fullpath = os.path.join(root,name)
        #print(fullpath)
        if(counter%10==0):
            test_file = test+"\\"+str(test_var)+".jpg"
            test_var+=1
            print("test_var:",test_var)
            #print(test_file)
            shutil.move(fullpath,test_file)
        else:
            train_file = train+"\\"+str(train_var)+".jpg"
            print("train_var",train_var)
            #print(train_file)
            shutil.move(fullpath,train_file)
            train_var+=1
        counter+=1
