import os
import tornado.web
from tornado.options import options

from app.handlers import IndexHandler, GameHandler
from app.handlers.image import ImageHandler
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from definitions import DB_ENGINE_URL, DB_CLIENT_ENCODING

engine = create_engine(DB_ENGINE_URL, encoding=DB_CLIENT_ENCODING)
Session = sessionmaker(bind=engine)
Base = declarative_base()
db_session = Session()

class Application(tornado.web.Application):

    def __init__(self):


        handlers = [
            (r'/game', GameHandler),
            (r'/img\/chesspieces\/wikipedia\/[a-zA-Z]{2}\.png', ImageHandler),
            (r'/(.*)', IndexHandler)
        ]

        settings = dict(
            engine=options.path_to_engine,
            debug=options.debug,
            template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )

        super(Application, self).__init__(handlers, **settings)
