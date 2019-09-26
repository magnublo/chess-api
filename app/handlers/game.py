from collections import OrderedDict
from tornado import gen
import chess

from app.handlers import BaseHandler, engine


class GameHandler(BaseHandler):

    def get(self):

        """
        Write out all of the board information for a given FEN.
        If no fen is provided, then it writes out the board in starting position.
        """

        #Check cookie, retrieve representation of FEN board after computer made move
        #if there is no cookie, make FEN board in starting position and set new cookie value
        #get list of all legal moves from this board
        #check that the received FEN board is indeed one move away from previous FEN board
        #if received board is illegal, send player_tried_cheating=True and have frontend reset board
        #if received board is legal, calculate best move and return

        #if receives parameters which is UCI but not "depth", return snarky comment which says "i have of course patched that one"

        fen = self.get_argument('fen', None) or chess.STARTING_FEN
        move = self.get_argument('move', None)

        try:

            board = chess.Board(fen)

            if move:
                board.push_uci(move)

            self.write_board(board)

        except ValueError:
            self.set_status(400)

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

        if board.is_game_over():
            return None

        engine.isready()
        engine.ucinewgame()
        engine.position(board)

        best_move, ponder_move = engine.go()

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
