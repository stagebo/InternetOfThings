import os
import tornado.ioloop
import pyrestful.rest
import logging
import pymysql
import configparser
import sys
import datetime
import json
import platform
import re
import traceback
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from tornado.log import access_log, app_log, gen_log
sys.path.append(".")
from handler_showrd import ShowrdHandler
from handler_controller import ControllerHandler
from handler_history import HistoryHandler

from tornado_mysql import pools





class Application(pyrestful.rest.RestService):
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.read_config()
        # 内存数据库


        logging.info("tornado is tring to init...")
        settings= dict(
            #cookie_secret="SBwKSjz3SCWo04t68f/FOY7fPKZI20JYje1IYPBrxaM=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug = False,
            # login_url = "admin/login",
            # log_function = self.mylog
        )
        handlers=[
            MainHadler,
            ShowrdHandler,
            ControllerHandler,
            HistoryHandler,
        ]
        super(Application, self).__init__(handlers, **settings)
        # TODO 取消原始数据库连接工具
        # dbHelper.database=dbHelper.DbHelper(self.mysql_host,self.mysql_uid,self.mysql_pwd,self.mysql_port,self.mysql_db)

        # self.db = syncdb.SyncDb(self.mysql_host, self.mysql_port, self.mysql_uid, self.mysql_pwd, self.mysql_db)
        logging.info("tornado is inited.")

    def read_config(self):

        try:
            self.cf.read("../app.conf")
        except:
            logging.error("not find a config file named webrest.conf")
            sys.exit(1)
        # self.mysql_host = self.cf.get("mysql", "host")
        # self.mysql_uid = self.cf.get("mysql", "uid")
        # self.mysql_pwd = self.cf.get("mysql", "pwd")
        # self.mysql_db = self.cf.get("mysql", "db")
        # self.mysql_port = self.cf.getint("mysql", "port")
        self.web_port = self.cf.getint("web", "port")



#
class MainHadler(pyrestful.rest.RestHandler):
    @get(_path="/")
    def index(self):
        self.render("base.html")





    @get(_path="/love/hastime" ,_produces=mediatypes.APPLICATION_JSON)
    def get_sum_time(self):
        now = datetime.datetime.now()
        tar = datetime.datetime(2017,6,6,21,0,0)
        d = now - tar
        return {
            "days": d.days,
            "seconds": d.seconds
        }






def main():

    try:
        print("Start the service")
        app = Application()
        app.listen(app.web_port)
        print("access port %s" % app.web_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")

if __name__ == '__main__':
    main()
