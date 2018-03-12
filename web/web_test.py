#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import traceback
import urllib
import json
import datetime
import time
import sys
import os


import configparser

cf = configparser.ConfigParser()
cf.read("../app.conf")
ifaliyun = cf.getint("ifaliyun", "ifaliyun")
if ifaliyun == 0:
    node="testlocal"
else:
    node = "testaliyun"
dbhost = cf.get(node, "dbhost")


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            # cookie_secret="SBwKSjz3SCWo04t68f/FOY7fPKZI20JYje1IYPBrxaM=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=False,
            # debug=False,
            # login_url="admin/login",
            # log_function=self.mylog
        )
        handlers=[
            (r"/1.0.0/(\w+)", CommonHandler),
            (r"/fileload/(\w+)", FileHandler),
        ]
        super(Application, self).__init__(handlers,**settings)
class BaseHandler(tornado.web.RequestHandler):
    @property
    def operatorid(self):
        return 123

class CommonHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, word):
        try:
            word = word[0].upper() + word[1:].lower()
            if word in [item for item in dir(common.functions)]:
                method = getattr(common.functions(self.application.db), word)
            elif word in [item for item in dir(trd_data_business.functions)]:
                method = getattr(trd_data_business.functions(self.application.db), word)
            else:
                self.finish("接口不存在")
                return
            response = yield tornado.gen.Task(method, self)
            if not response[1]:
                print(response)
            self.finish(str(response))
        except AttributeError as e:

            self.write("接口不存在")
            self.finish()
            sys.exit(0)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, word):
        try:
            word = word[0].upper() + word[1:].lower()
            if word in [item for item in dir(common.functions)]:
                method = getattr(common.functions(self.application.db), word)
            elif word in [item for item in dir(trd_data_business.functions)]:
                method = getattr(trd_data_business.functions(self.application.db), word)
            else:
                self.finish("接口不存在")
                return
            response = yield tornado.gen.Task(method, self)
            if not response[1]:
                print(word, response)
            self.write(str(response))
        except AttributeError as e:
            self.write("接口不存在")
            print("接口%s不存在" % word)
            sys.exit(0)
        finally:
            self.finish()


# ab -n 1 -c 1 -p Insert_energy_station.txt -T 'application/json' http://localhost:8888/common/Insert_energy_station
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    ioloop = tornado.ioloop.IOLoop.instance()

    app.db = DbHelper()
    app.db.open(ioloop=ioloop, dbname="piot", dbusername="postgres", dbpasswd="tdq$abc123", dbhost=dbhost,
                  dbport=5432)

    future = app.db.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()

    http_server = tornado.httpserver.HTTPServer(app)
    port = 7001
    http_server.listen(port, 'localhost')
    print("dbhost",dbhost)
    print('localhost:%s'%port)
    ioloop.start()