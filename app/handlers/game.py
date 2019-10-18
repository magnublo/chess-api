import hashlib
import json
import time
from enum import Enum
from random import random

from utils import ChessBoardWithUnsaitizedFen as Board, flatten, get_meme_hint
from chess import STARTING_FEN, WHITE, BLACK

from app.handlers import BaseHandler, engine, info_handler
from app.models.chess_session import ChessSession
from definitions import ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD, TOTAL_NR_OF_INJECTIONS_THRESHOLD, \
    ONE_MOVE_AFTER_START_FENS, COOKIE_NAME, ILLEGAL_MOVE_MESSAGE, COMPUTER_HAS_WON_MESSAGE, HUMAN_HAS_WON_MESSAGE, \
    HUMAN_HAS_WON_BUT_CHEATED_MESSAGE, ONE_MOVE_AFTER_START_FENS_UNSANITIZED_DICT


class GAME_STATE(Enum):
    NOT_FINISHED = 0
    HUMAN_HAS_WON = 1
    COMPUTER_HAS_WON = 2
    HUMAN_HAS_WON_BUT_CHEATED = 4


def _replace_oldest_chess_session_with_new(db_session, cookie_val):
    chess_session_row = db_session.query(ChessSession).order_by(ChessSession.time_updated.asc()).first()
    chess_session_row.cookie = cookie_val
    chess_session_row.fen = STARTING_FEN
    chess_session_row.injected_argument_counter = 0
    chess_session_row.time_updated = time.time()
    db_session.commit()
    return chess_session_row


def _resolve_chess_session_from_cookie_session(db_session, cookie_val):
    if not cookie_val:
        new_cookie_val = hashlib.md5((str(time.time() + random())).encode('utf-8')).hexdigest()
        chess_session_row = _replace_oldest_chess_session_with_new(db_session, cookie_val=new_cookie_val)
        return chess_session_row, new_cookie_val
    else:
        chess_session_row = db_session.query(ChessSession).filter_by(
            cookie=cookie_val).first()
        if not chess_session_row:
            chess_session_row = _replace_oldest_chess_session_with_new(db_session,
                                                                       cookie_val=cookie_val)
        return chess_session_row, None


class GameHandler(BaseHandler):

    def post(self):

        with self.make_session() as db_session:

            response_dict = {}
            received_fen = self.get_argument('position', None)
            cookie_val = self.get_cookie(COOKIE_NAME)

            chess_session_row, new_cookie_val = _resolve_chess_session_from_cookie_session(db_session, cookie_val)

            if new_cookie_val:
                self.set_cookie(COOKIE_NAME, new_cookie_val)

            move_is_legal, sanitized_fen, board_is_reset = self._move_is_legal(received_fen, chess_session_row.fen)

            if board_is_reset:
                chess_session_row.injected_argument_counter = 0
                chess_session_row.nr_of_player_moves = 0
                db_session.commit()

            if not move_is_legal:
                response_dict["resetBoard"] = True
                response_dict["img"] = get_meme_hint()
                response_dict["msg"] = ILLEGAL_MOVE_MESSAGE
                db_session.commit()
                self.write(response_dict)
                self.finish()
                return

            received_board = Board(sanitized_fen)
            chess_session_row.nr_of_player_moves += 1
            injected_arguments = self._get_injected_arguments()
            if len(injected_arguments.keys()) > 0:
                info_dict = json.dumps(info_handler.info)
                response_dict["info"] = info_dict

            chess_session_row.injected_argument_counter += "searchmoves" in injected_arguments.keys()

            best_move = self.get_best_move(received_board)
            if best_move is not None:
                received_board.push(best_move)
            outbound_board = received_board

            game_state = self._get_game_state(outbound_board, chess_session_row.injected_argument_counter,
                                              chess_session_row.nr_of_player_moves)

            if game_state == GAME_STATE.NOT_FINISHED:
                chess_session_row.fen = outbound_board.fen()
                response_dict["bestMove"] = best_move.uci()
            elif game_state == GAME_STATE.COMPUTER_HAS_WON:
                response_dict["msg"] = COMPUTER_HAS_WON_MESSAGE
                response_dict["bestMove"] = best_move.uci()
                response_dict["img"] = get_meme_hint()
            elif game_state == GAME_STATE.HUMAN_HAS_WON:
                response_dict["msg"] = HUMAN_HAS_WON_MESSAGE
            elif game_state == GAME_STATE.HUMAN_HAS_WON_BUT_CHEATED:
                response_dict["msg"] = HUMAN_HAS_WON_BUT_CHEATED_MESSAGE
                response_dict["img"] = get_meme_hint()

            db_session.commit()
            self.write(response_dict)
            self.finish()

        # Check cookie, retrieve last FEN board
        # if there is no cookie, make FEN board in starting position and set new cookie value
        # get list of all legal moves from this position and find out of received board is legal
        # if received board is illegal, send player_tried_cheating=True and have frontend reset board
        # if request has a depth parameter, increment nr of requests received with depth parameter
        # if computer is check mate, see if depth parameter request counter is 10 or => 90 %
        # calculate best move and return

    def get_best_move(self, board: Board):

        class PythonChessCompatibleMove:
            def __init__(self, from_square, to_square):
                self.from_square = from_square
                self.to_square = to_square
                self.promotion = None

        search_moves_str = self.get_argument('searchmoves', False)
        if search_moves_str:
            search_moves = []
            strs_of_individual_moves_to_be_searched = search_moves_str.split(" ")
            for move_str in strs_of_individual_moves_to_be_searched:
                search_moves.append(PythonChessCompatibleMove(from_square=move_str[0:2], to_square=move_str[2:4]))
        else:
            search_moves = None

        ponder = self.get_argument('ponder', None)
        wtime = self.get_argument('wtime', None)
        btime = self.get_argument('btime', None)
        winc = self.get_argument('winc', None)
        binc = self.get_argument('binc', None)
        movestogo = self.get_argument('movestogo', None)
        depth = self.get_argument('depth', None)
        nodes = self.get_argument('nodes', None)
        mate = self.get_argument('mate', None)
        movetime = self.get_argument('movetime', None)

        if board.is_game_over():
            return None

        engine.isready()
        engine.ucinewgame()
        engine.position(board)

        best_move, ponder_move = engine.go(searchmoves=search_moves, ponder=ponder, wtime=wtime, btime=btime,
                                           winc=winc, binc=binc, movestogo=movestogo, depth=depth, nodes=nodes,
                                           mate=mate, movetime=movetime)

        return best_move

    def _get_injected_arguments(self):
        dict = {}
        dict["searchmoves"] = self.get_argument('searchmoves', False)
        dict["btime"] = self.get_argument('btime', False)
        dict["depth"] = self.get_argument('depth', False)
        dict["nodes"] = self.get_argument('nodes', False)
        dict["movetime"] = self.get_argument('movetime', False)

        keys = [key for key in dict.keys()]

        for key in keys:
            if dict[key] is False:
                del dict[key]

        return dict

    def _move_is_legal(self, received_fen, last_saved_fen):
        if received_fen in ONE_MOVE_AFTER_START_FENS:
            try:
                received_fen = ONE_MOVE_AFTER_START_FENS_UNSANITIZED_DICT[received_fen]
            except KeyError:
                pass
            return True, received_fen, True

        last_saved_board = Board(last_saved_fen)
        legal_moves = [move for move in last_saved_board.legal_moves]

        if not received_fen:
            self.send_error(500)
        for move in legal_moves:
            last_saved_board.push(move)
            sanitized_fen = last_saved_board.fen()
            unsanitized_fen = last_saved_board.unsanitized_fen()
            if sanitized_fen == received_fen or unsanitized_fen == received_fen:
                return True, sanitized_fen, False
            last_saved_board = Board(last_saved_fen)

        return False, None, False

    def _get_game_state(self, received_board: Board, nr_of_moves_with_injections,
                        total_nr_of_moves) -> GAME_STATE:

        if received_board.turn == BLACK and received_board.is_checkmate():
            sufficient_percent_injections = (
                                                                       nr_of_moves_with_injections /
                                                                       total_nr_of_moves) > \
                                                           ARGUMENT_INJECTION_PERCENTAGE_THRESHOLD

            sufficient_nr_of_injections = nr_of_moves_with_injections > TOTAL_NR_OF_INJECTIONS_THRESHOLD

            if sufficient_percent_injections and sufficient_nr_of_injections:
                return GAME_STATE.HUMAN_HAS_WON
            else:
                return GAME_STATE.HUMAN_HAS_WON_BUT_CHEATED


        elif received_board.turn == WHITE and received_board.is_checkmate():
            return GAME_STATE.COMPUTER_HAS_WON

        else:
            return GAME_STATE.NOT_FINISHED

