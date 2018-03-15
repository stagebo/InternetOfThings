
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
    def get_fivemin_data(self):
        try:
            time_mark = self.get_argument("time",None)
            if not time_mark:
                time_mark = datetime.datetime.now().strftime("%Y-%m-%d %H")
            time_stamp = time.strptime(time_mark,"%Y-%m-%d %H")
            timestart = int(time.mktime(time_stamp))*1000
            timeend = timestart + 60*60*1000
            device_id = int(self.get_argument("id",None))
            if not device_id:
                return {"ret":0,"msg":"id不能为空"}



            condition = {
                'id':device_id,
                'time':{
                    "$gte":str(timestart),
                    "$lte":str(timeend)
                }
            }
            # print(condition)

            ret = db.db.device.find(condition)
            retdata = []
            for row in ret:
                del row["_id"]
                retdata.append(row)
            # print(retdata)
            return retdata
        except:

            traceback.print_exc()

