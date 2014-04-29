#!/usr/bin/env python

import os
import toro
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.concurrent

path = os.path.realpath(__file__)
static_path = os.path.join(path, 'static')
queues = {}


class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/form.html")


@tornado.web.stream_request_body
class ShareHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.key = self.request.uri.split('/')[2]
        queues[self.key] = toro.JoinableQueue(maxsize=3)
        pass

    #@tornado.web.asynchronous
    #@tornado.gen.engine
    def data_received(self, data):
        #print "data received:" + data
        return queues[self.key].put(data)
        pass

    def post(self, uri):
        #print "Finished post"
        pass


class FetchHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.key = self.request.uri.split('/')[2]

    #@tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, uri):
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment')

        while True:
            item = yield queues[self.key].get()
            print "data sent:" + item
            self.write(item)
        queues[self.key].task_done()
        del queues[self.key]


handlers = [
    (r'/', FormHandler),
    (r'/share/(.*)', ShareHandler),
    (r'/fetch/(.*)', FetchHandler),
]


application = tornado.web.Application(handlers, debug=True)
application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
