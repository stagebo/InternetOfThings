#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import random
import json
import time
import traceback

import sys
sys.path.append("..")

import logging
import datetime
import configparser

cf = configparser.ConfigParser()
cf.read("../app.conf")
password = cf.get("mqttServer", "password")
username = cf.get("mqttServer", "username")
hostname = cf.get("mqttServer", "hostname")
port = cf.getint("mqttServer", "port")
qos = cf.getint("mqttServer", "qos")


idx = 1
now = datetime.datetime.now() + datetime.timedelta(days=0)

def log(strs):
    logging.info("time:%s "% datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +str(strs))


def toLength(s, l):
    s = str(s)
    if len(s) >= l:
        return str[-l:]
    while len(s) < l:
        s = "0" + s
    return s


def sendMsg():



    itemList = []
    now = datetime.datetime.now()
    zero = datetime.datetime(now.year,now.month,now.day,0,0,0)
    timedel = now - zero
    seconds = timedel.seconds
    if seconds%5 != 0:
        return

    msgs = []
    timemark = now.strftime("%Y-%m-%d %H:%M:%S")
    for i in range(1,11):
        topic = "zhangjing/device/%s"%i
        msg = {
            "id":i,
            "time":timemark,

            "1001": random.randint(5,9), # 温度
            "1002": random.randint(210, 250), # 电压
            "1003": random.randint(500, 600)/1000, # 电流
            "1004": random.randint(100, 200),# 属性1
            "1005": random.randint(100, 200),# 属性2
            "1006": random.randint(100, 200),# 属性3
            "1007": random.randint(100, 200),# 属性4
            "1008": random.randint(100, 200),# 属性5
            "1009": random.randint(100, 200),# 属性6
            "1010": random.randint(100, 200),# 属性7
        }
        msg = json.dumps(msg)

        msgItem = {'topic': topic, 'payload': msg, 'qos': qos}
        # msgItem = (topic,msg)
        print(msgItem)
        msgs.append(msgItem)
    publish.multiple(msgs,
                     auth={
                         'username': username,
                         'password': password
                     },
                     port=port,
                     protocol=mqtt.MQTTv311,
                     hostname=hostname)
    print("message is sent.")

if __name__ == "__main__":
    while True:
        try:
            sendMsg()
            time.sleep(1)
        except:
            print('连接mqtt服务器失败！')
            traceback.print_exc()
