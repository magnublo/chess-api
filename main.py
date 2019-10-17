import os
import platform

import tornado.httpserver
import tornado.ioloop
from sqlalchemy import create_engine
from tornado.options import define, options

from definitions import DB_ENGINE_URL, Base


def setup():
    db_engine = create_engine(DB_ENGINE_URL)
    Base.metadata.create_all(db_engine)
    system = platform.system()
    engine_path = os.path.dirname(__file__)
    engine_paths = dict([
        ('Darwin', 'engines/stockfish/Mac/stockfish-7-64'),
        ('Linux', 'engines/stockfish/Linux/stockfish-7-x64'),
        ('Linux2', 'engines/stockfish/Linux/stockfish-7-x64'),
    ])

    if not system in engine_paths:
        raise Exception('No engine for OS')

    engine_path = os.path.join(engine_path, engine_paths[system])
    environment = os.environ['ENVIRONMENT'] if 'ENVIRONMENT' in os.environ else 'PRODUCTION'
    port = 5000
    debug = True

    if environment != 'development':
        port = os.environ.get('PORT', 5000)
        debug = False

    define('port', default=port, help='run on the given port', type=int)
    define('debug', default=debug, help='run in debug mode')
    define('path-to-engine', default=engine_path, help='the location of the chess engine')

if __name__ == '__main__':
    setup()
    from app import Application
    from tornado_sqlalchemy import make_session_factory
    factory = make_session_factory(DB_ENGINE_URL)

    http_server = tornado.httpserver.HTTPServer(Application(session_factory=factory))
    http_server.listen(options.port)
    print('Listening on port %s' % options.port)
    tornado.ioloop.IOLoop.current().start()
