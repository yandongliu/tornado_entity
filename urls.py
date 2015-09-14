from time import sleep

import tornado
from tornado.gen import coroutine, Return

from handlers.foo import FooHandler

@coroutine
def slow_func():
    print 'i am working.'
    sleep(3)
    print 'i am done.'
    raise Return(42)


def foo():
    print config.get('hi')
    e = Entity()

class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        # resp = yield slow_func()
        # print resp
        # self.write("Hello, world")
        items = ['hi', 'world']
        self.render('base.html', title='hi', items=items)

url_patterns = [
    (r"/", MainHandler),
    (r"/foo", FooHandler),
]
