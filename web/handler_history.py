
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
class HistoryHandler(pyrestful.rest.RestHandler):

    @get(_path="/history")
    def get_index(self):
        self.render("history/index.html")



