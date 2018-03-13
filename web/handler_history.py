
import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import os
import datetime
sys.path.append("..")
from dbhelper import db
import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes

import traceback

import hashlib  # 导入md5加密模块
import time  # 导入时间模块
import sys
import re
import requests
class HistoryHandler(pyrestful.rest.RestHandler):

    @get(_path="/history")
    def get_index(self):
        self.render("history/index.html")

    @get(_path="/history/get_fivemin_data",_produces=mediatypes.APPLICATION_JSON)
    def get_index(self):
        try:
            device_id = self.get_argument("id",None)
            if not device_id:
                return {"ret":0,"msg":"id不能为空"}
            now = datetime.datetime.now()
            target = now - datetime.timedelta(minutes=5)
            str_target = target.strftime("%Y-%m-%d %H:%M:%S")
            condition = {
                id:device_id,
                time:{
                    "$gte":str_target
                }
            }
            ret = db.find(condition)
            return ret
        except:
            traceback.print_exc()

