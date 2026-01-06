import random

from game.chessboard import ChessBoard
from game.common import Move
from game.bot.common import get_pieces_to_moves

def easy_bot_input(board: ChessBoard) -> Move:
    pieces_to_moves = get_pieces_to_moves(board, board.current_player)

    selected_piece = random.sample(list(pieces_to_moves.keys()), 1)[0]
    selected_move  = random.sample(pieces_to_moves[selected_piece], 1)[0]

    return selected_move