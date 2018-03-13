#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
dbdevice = db.device
print('connected')

def insert(str):
    dbdevice.insert(str)

def find(condition=None):
    if condition:
        return dbdevice.find(condition)
    else:
        return dbdevice.find()

if __name__ == '__main__':
    condition = {
        "id":1,
        "time":{
            "$gte":'2018-3-13 10:42:40'
        }
    }
    for i in find(condition):
        print(i)
