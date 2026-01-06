from typing import Tuple

from game.chessboard import ChessBoard
from game.common import Move

def get_pieces_to_moves(board: ChessBoard, player_id: int) -> dict[Tuple[int, int], list[Move]]:
    pieces: list[Tuple[int, int]] = board.get_player_pieces(player_id)
    pieces_to_moves: dict[Tuple[int, int], list[Move]] = dict()

    for piece in pieces:
        moves = board.get_piece_moves(piece)
        moves.sort(key=lambda m: m.taken_piece is not None, reverse=True)

        if moves:
            pieces_to_moves[piece] = moves

    return pieces_to_moves


def sort_scores(move: Move) -> bool:
    return move.taken_piece is not None