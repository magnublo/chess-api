import os

import tornado.web
from tornado.options import options

from app.handlers import IndexHandler, GameHandler
from app.handlers.static import StaticFileHandler
from main import engine, Base


class Application(tornado.web.Application):

    def __init__(self):
        Base.metadata.create_all(engine)

        handlers = [
            (r'/game', GameHandler),
            (r'/img\/chesspieces\/wikipedia\/[a-zA-Z]{2}\.png', StaticFileHandler),
            (r'/js\/(.+)\.js', StaticFileHandler),
            (r'/(.*)', IndexHandler)
        ]

        settings = dict(
            engine=options.path_to_engine,
            debug=options.debug,
            template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )

        super(Application, self).__init__(handlers, **settings)
