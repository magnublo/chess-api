import chess
from chess import uci

class ChessBoardWithUnsaitizedFen(chess.Board):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def unsanitized_fen(self):
        fen = []
        fen.append(self.board_fen())
        fen.append("w" if self.turn == chess.WHITE else "b")
        fen.append(self.castling_xfen())
        fen.append(chess.SQUARE_NAMES[self.ep_square])
        fen.append(str(self.halfmove_clock))
        fen.append(str(self.fullmove_number))
        return " ".join(fen)


class InfoHandlerWithPrintableMoves(chess.uci.InfoHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pv(self, moves):
        self.info["pv"][self.info.get("multipv", 1)] = [move.from_square + move.to_square for move in moves]

    def currmove(self, move):
        self.info["currmove"] = move.from_square + move.to_square


def flatten(current_dict, current_key, result_dict):

    # For every key in the dictionary
    for key in current_dict:
        # If the value is of type `dict`, then recurse with the value
        if isinstance(current_dict[key], dict):
            flatten(current_dict[key], current_key + key, result_dict)
        # Otherwise, add the element to the result
        else:
            result_dict[current_key + key] = current_dict[key]
    return result_dict


def get_meme_hint():
    with open("meme_hint_img") as meme_hint_file:
        base64_img = meme_hint_file.read()

    return base64_img
