#!/usr/bin/env python

import os
import uuid
import toro
import utils
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.concurrent

path = os.path.realpath(__file__)
static_path = os.path.join(path, 'static')
queues = {}


class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/form.html", key=uuid.uuid1().hex[:5])


@tornado.web.stream_request_body
class ShareHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.key = self.request.uri.split('/')[2]
        self.stripper = utils.BoundaryStripper()
        queues[self.key] = toro.Queue(maxsize=1)

    def data_received(self, data):
        print "data received: %s" % len(data)
        return queues[self.key].put(self.stripper.process(data))

    def post(self, uri):
        queues[self.key].put(False)
        self.render("static/success.html")


class FetchHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.key = self.request.uri.split('/')[2]

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, uri):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment')

        item = yield queues[self.key].get()
        while item:
            print "data sent: %s" % len(item)
            self.write(item)
            item = yield queues[self.key].get()

        self.flush()
        del queues[self.key]
        self.finish()



handlers = [
    (r'/', FormHandler),
    (r'/share/(.*)', ShareHandler),
    (r'/fetch/(.*)', FetchHandler),
]


application = tornado.web.Application(handlers, debug=True)
application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
