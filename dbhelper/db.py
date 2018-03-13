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
    insert({"name":"zhangsan","age":18})
    for i in find(None):
        print(i)
