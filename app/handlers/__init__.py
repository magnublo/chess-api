from chess import uci
from tornado.options import options

from utils import InfoHandlerWithPrintableMoves

engine = uci.popen_engine(options.path_to_engine)
info_handler = InfoHandlerWithPrintableMoves()
engine.info_handlers.append(info_handler)
engine.uci()

from .base import BaseHandler
from .index import IndexHandler
from .game import GameHandler