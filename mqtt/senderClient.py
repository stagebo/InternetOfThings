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

    topic = "zhangjing/device/1"

    itemList = []
    now = datetime.datetime.now()
    item = {
        "id": random.randint(1, 10),
        "data":123123

    }

    msg = {
        "time": str(now),
        "data": item}
    msg = json.dumps(msg)

    msgItem = {'topic': topic, 'payload': msg, 'qos': qos}
    # msgItem = (topic,msg)
    msgs = []
    msgs.append(msgItem)
    print(msgItem)
    publish.multiple(msgs,
                     auth={
                         'username': username,
                         'password': password
                     },
                     port=port,
                     protocol=mqtt.MQTTv311,
                     hostname=hostname)
    print("message is sent.")
    time.sleep(1)
if __name__ == "__main__":
    while True:
        try:
            sendMsg()
        except:
            print('连接mqtt服务器失败！')
            traceback.print_exc()
