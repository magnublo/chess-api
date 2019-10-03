import hashlib
import time
from collections import OrderedDict
from random import random

import chess

from app.handlers import BaseHandler, engine
from app.models.chess_session import ChessSession
from definitions import COOKIE_NAME, ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD, TOTAL_NR_OF_INJECTIONS_THRESHOLD
from main import db_session


def _replace_oldest_chess_session_with_new(cookie_val):
    chess_session_row = db_session.query(ChessSession).order_by(ChessSession.time_updated.asc()).first()
    chess_session_row.cookie = cookie_val
    chess_session_row.fen = chess.STARTING_FEN
    chess_session_row.injected_argument_counter = 0
    chess_session_row.time_updated = time.time()
    db_session.commit()
    return chess_session_row


class GameHandler(BaseHandler):

    def post(self):

        """
        Write out all of the board information for a given FEN.
        If no fen is provided, then it writes out the board in starting position.
        """

        if not self.get_cookie(COOKIE_NAME):
            cookie_val = hashlib.md5((str(time.time()+random())).encode('utf-8')).hexdigest()
            self.set_cookie(COOKIE_NAME, cookie_val)
            chess_session_row = _replace_oldest_chess_session_with_new(cookie_val)
        else:
            chess_session_row = db_session.query(ChessSession).filter_by(cookie=self.get_cookie(COOKIE_NAME)).first()
            if not chess_session_row:
                chess_session_row = _replace_oldest_chess_session_with_new(self.get_cookie(COOKIE_NAME))

        self._check_if_move_is_legal(chess_session_row.fen)
        chess_session_row.nr_of_player_moves += 1
        chess_session_row.injected_argument_counter += self._has_injected_argument()
        self._check_if_player_has_won(chess_session_row)
        received_board = chess.Board(self.get_argument("position"))
        best_move = self.get_best_move(received_board)
        self.finish({"bestMove": best_move})

        # Check cookie, retrieve last FEN board
        # if there is no cookie, make FEN board in starting position and set new cookie value
        # get list of all legal moves from this position and find out of received board is legal
        # if received board is illegal, send player_tried_cheating=True and have frontend reset board
        # if request has a depth parameter, increment nr of requests received with depth parameter
        # if computer is check mate, see if depth parameter request counter is 10 or => 90 %
        # calculate best move and return


    def write_board(self, board:chess.Board):

        """
        Writes out all of the board information in requested format (defaults to json)
        """

        format = self.get_argument('format', 'json')

        if format == 'json':
            self.write_json(board)

        elif format  == 'ascii':
            self.write_ascii(board)

    def get_best_move(self, board: chess.Board):

        """
        Retrieves the best move from the engine for the current board
        """

        search_moves = self.get_argument('searchMoves', None)
        ponder = self.get_argument('ponder', None)
        wtime = self.get_argument('wtime', None)
        btime = self.get_argument('btime', None)
        winc = self.get_argument('winc', None)
        binc = self.get_argument('binc', None)
        movestogo = self.get_argument('movestogo', None)
        depth = self.get_argument('depth', None)
        nodes = self.get_argument('nodes', None)
        mate = self.get_argument('mate', None)

        if board.is_game_over():
            return None

        engine.isready()
        engine.ucinewgame()
        engine.position(board)

        best_move, ponder_move = engine.go(searchmoves=search_moves, ponder=ponder, wtime=wtime, btime=btime,
                                           winc=winc, binc=binc, movestogo=movestogo, depth=depth, nodes=nodes,
                                           mate=mate)

        return best_move.uci()

    def write_json(self, board:chess.Board):

        """
        Writes all of the board info in json
        """

        best_move = self.get_best_move(board)

        output = OrderedDict([

            ('fen', board.fen()),
            ('fullmoveNumber', board.fullmove_number),
            ('result', board.result()),
            ('isGameOver', board.is_game_over()),
            ('isCheckmate',board.is_checkmate()),
            ('isStalemate', board.is_stalemate()),
            ('isInsufficientMaterial', board.is_insufficient_material()),
            ('isSeventyfiveMoves', board.is_seventyfive_moves()),
            ('isFivefoldRepetition', board.is_fivefold_repetition()),

            ('white', OrderedDict([
                ('hasKingsideCastlingRights', board.has_kingside_castling_rights(chess.WHITE)),
                ('hasQueensideCastlingRights', board.has_queenside_castling_rights(chess.WHITE)),
            ])),

            ('black', OrderedDict([
                ('hasKingsideCastlingRights', board.has_kingside_castling_rights(chess.BLACK)),
                ('hasQueensideCastlingRights', board.has_queenside_castling_rights(chess.BLACK)),
            ])),

            ('turn', OrderedDict([
                ('color', 'white' if board.turn is chess.WHITE else 'black'),
                ('isInCheck', board.is_check()),
                ('bestMove', best_move),
                ('legalMoves', [move.uci() for move in board.legal_moves]),
                ('canClaimDraw', board.can_claim_draw()),
                ('canClaimFiftyMoves', board.can_claim_fifty_moves()),
                ('canClaimThreefoldRepetition', board.can_claim_threefold_repetition()),
            ])),

        ])

        self.finish(output)

    def write_ascii(self, board:chess.Board):

        """
        Loops through a game board and prints it out as ascii. Useful for debugging.
        For example, the starting board would print out:

        ---|--------------------------------
         8 | r | n | b | q | k | b | n | r |
        ---|--------------------------------
         7 | p | p | p | p | p | p | p | p |
        ---|--------------------------------
         6 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         5 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         4 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         3 |   |   |   |   |   |   |   |   |
        ---|--------------------------------
         2 | P | P | P | P | P | P | P | P |
        ---|--------------------------------
         1 | R | N | B | Q | K | B | N | R |
        ---|--------------------------------
           | a | b | c | d | e | f | g | h |

        """

        fen = board.fen()
        rows = fen.split(' ')[0].split('/')
        output = '---|%s\n' % ('-' * 32)
        row_separator = '\n' + output
        row_nums = reversed(range(1,9))

        for row_num, row in zip(row_nums, rows):
            output += ' %s | ' % row_num
            for piece in row:
                if piece.isdigit():
                    output += '  | ' * int(piece)
                else:
                    output += piece + ' | '
            output += row_separator

        output += '   | '
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            output += str(i) + ' | '

        self.set_header('Content-Type', 'text/plain; charset=utf-8')
        self.finish(output)

    def _has_injected_argument(self):
        search_moves = self.get_argument('searchMoves', False)
        ponder = self.get_argument('ponder', False)
        wtime = self.get_argument('wtime', False)
        btime = self.get_argument('btime', False)
        winc = self.get_argument('winc', False)
        binc = self.get_argument('binc', False)
        movestogo = self.get_argument('movestogo', False)
        depth = self.get_argument('depth', False)
        nodes = self.get_argument('nodes', False)
        mate = self.get_argument('mate', False)

        return search_moves or wtime or btime or depth or nodes or mate


    def _check_if_move_is_legal(self, last_saved_fen):
        last_saved_board = chess.Board(last_saved_fen)
        legal_moves = last_saved_board.legal_moves
        received_fen = self.get_argument('position', None)

        if not received_fen:
            self.send_error(500)

        for move in legal_moves:
            last_saved_board.push(move)
            if last_saved_board.fen() == received_fen:
                return True
            last_saved_board = chess.Board(last_saved_fen)

        return False

    def _check_if_player_has_won(self, chess_session_row):
        received_fen = self.get_argument('position', None)
        received_board = chess.Board(received_fen)
        player_has_won = received_board.turn == chess.BLACK and received_board.is_checkmate()

        nr_of_injections_in_this_game = chess_session_row.injected_argument_counter
        nr_of_player_moves = chess_session_row.nr_of_player_moves
        player_has_done_proper_injections = \
            (nr_of_injections_in_this_game / nr_of_player_moves) > ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD\
            and nr_of_injections_in_this_game >= TOTAL_NR_OF_INJECTIONS_THRESHOLD

        if player_has_won and player_has_done_proper_injections:
            pass
