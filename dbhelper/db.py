#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time


# conn = MongoClient('127.0.0.1', 27017)
conn = MongoClient('www.stagebo.xyz', 27017)
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
    now = int(round(time.time() * 1000))
    target = now - 5 * 1000
    str_target = str(target)
    condition = {
        'id': 1,
        'time': {
            "$gte": str_target
        }
    }
    print(str_target)
    print(condition)
    ret = find(condition) #db.db.device.find()
    retdata = []
    for row in ret:
        print(row)


