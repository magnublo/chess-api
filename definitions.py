import os

from tornado_sqlalchemy import declarative_base

Base = declarative_base()
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_ENGINE_URL = "sqlite:///" + ROOT_DIR + "/sessions.db"
DB_CLIENT_ENCODING = "utf8"
ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD = 0.9
TOTAL_NR_OF_INJECTIONS_THRESHOLD = 10

FLAG = "CTF{some_chess_flag}"

ILLEGAL_MOVE_MESSAGE = "You tried cheating! Board is reset, let's play from the beginning."
COMPUTER_HAS_WON_MESSAGE = "Computer won."
HUMAN_HAS_WON_MESSAGE = f"You won! Congratulations. Flag is {FLAG}"
HUMAN_HAS_WON_BUT_CHEATED_MESSAGE = "You have either cheated by soliciting a chess engine, or you're just too good a " \
                                    "chess player to get this flag. Sorry!"

COOKIE_NAME = "chess-session"

ONE_MOVE_AFTER_START_FENS = ['rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1',
                             'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq a1 1 1',
                             'rnbqkbnr/pppppppp/8/8/8/5P2/PPPPP1PP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/7P/PPPPPPP1/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/7P/PPPPPPP1/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b KQkq a1 1 1',
                             'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq f3 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
                             'rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq a1 1 1',
                             'rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq - 1 1',
                             'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b KQkq - 1 1',
                             'rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/5P2/PPPPP1PP/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1',
                             'rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq a1 1 1',
                             'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1',
                             'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b KQkq h3 0 1',
                             'rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq g3 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b KQkq - 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq b3 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq a1 0 1',
                             'rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq a1 0 1']

ONE_MOVE_AFTER_START_FENS_UNSANITIZED_DICT = {
    'rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b KQkq a1 1 1': 'rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b '
                                                                  'KQkq - 1 1',
    'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq a1 1 1': 'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b '
                                                                   'KQkq - 1 1',
    'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq a1 1 1': 'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b '
                                                                   'KQkq - 1 1',
    'rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq a1 1 1': 'rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b '
                                                                  'KQkq - 1 1',
    'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b '
                                                                  'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/5P2/PPPPP1PP/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/5P2/PPPPP1PP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/8/7P/PPPPPPP1/RNBQKBNR b KQkq a1 0 1': 'rnbqkbnr/pppppppp/8/8/8/7P/PPPPPPP1/RNBQKBNR b '
                                                                  'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1': 'rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b '
                                                                  'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq b3 0 1': 'rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 1': 'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1': 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1': 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq f3 0 1': 'rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq g3 0 1': 'rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b '
                                                                   'KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b KQkq h3 0 1': 'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b '
                                                                  'KQkq - 0 1'}