
import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import os
import datetime
sys.path.append("..")

import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes

import traceback

import hashlib  # 导入md5加密模块
import time  # 导入时间模块
import sys
import re
import requests
from dbhelper import db
class ShowrdHandler(pyrestful.rest.RestHandler):

    @get(_path="/showrd")
    def get_index(self):
        self.render("showrd/index.html")


    @get(_path="/showrd/get_fivemin_data",_produces=mediatypes.APPLICATION_JSON)
    def get_fivemin_data(self):
        try:
            device_id = int(self.get_argument("id",None))
            if not device_id:
                return {"ret":0,"msg":"id不能为空"}
            now = int(round(time.time() * 1000))
            target = now - 5*1000*60
            str_target =str(target)
            condition = {
                'id':device_id,
                'time':{
                    "$gte":str_target
                }
            }
            print(str_target)

            ret = db.db.device.find(condition)
            retdata = []
            for row in ret:
                del row["_id"]
                retdata.append(row)
            return retdata
        except:
            traceback.print_exc()

