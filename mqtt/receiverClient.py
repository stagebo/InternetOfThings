#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''


'''
import paho.mqtt.client as mqtt
import traceback
import configparser
import datetime
import json
import sys
import logging
sys.path.append("..")
from dbhelper import db

cf = configparser.ConfigParser()
cf.read("../app.conf")
password = cf.get("mqttServer", "password")
username = cf.get("mqttServer", "username")
hostname = cf.get("mqttServer", "hostname")
port = cf.getint("mqttServer", "port")
qos = cf.getint("mqttServer", "qos")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def log(strs):
    logging.info("time:%s "% datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +str(strs))




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log("connect to mqtt server return code: "+str(rc))

    print("connected!")

    topics = []

    topic = "zhangjing/device/#"
    topics.append((topic,qos))
    log("subscribe topic:%s"%topic)

    client.subscribe(topics)

success = 0
fail = 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #在这里处理业务逻辑
    topic = msg.topic
    ms = str(msg.payload, "utf-8")
    try:
        business(client,userdata,msg)
    except:
        print("business faild")

def business(client,userdata,msg):
    topic = msg.topic
    topic_info = topic.split('/')
    device_id = topic_info[2]
    if not device_id.isdigit():
        return
    ms = json.loads(str(msg.payload, "utf-8"))
    # db.insert(ms)
    print(topic,ms)


if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username,password)
    client.connect(hostname, port)

    client.loop_forever()

