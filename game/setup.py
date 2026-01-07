from typing import Tuple
from game.common import ChessPiece, PIECE_TYPE

def get_starting_board(bottom_player: int, top_player: int) -> list[ChessPiece | None]:
    return [
        ChessPiece(top_player, 1, PIECE_TYPE.ROOK), ChessPiece(top_player, 1, PIECE_TYPE.KNIGHT), ChessPiece(top_player, 1, PIECE_TYPE.BISHOP), ChessPiece(top_player, 1, PIECE_TYPE.QUEEN), ChessPiece(top_player, 1, PIECE_TYPE.KING), ChessPiece(top_player, 1, PIECE_TYPE.BISHOP), ChessPiece(top_player, 1, PIECE_TYPE.KNIGHT), ChessPiece(top_player, 1, PIECE_TYPE.ROOK),
        ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN), ChessPiece(top_player, 1, PIECE_TYPE.PAWN),
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN), ChessPiece(bottom_player, -1, PIECE_TYPE.PAWN),
        ChessPiece(bottom_player, -1, PIECE_TYPE.ROOK), ChessPiece(bottom_player, -1, PIECE_TYPE.KNIGHT), ChessPiece(bottom_player, -1, PIECE_TYPE.BISHOP), ChessPiece(bottom_player, -1, PIECE_TYPE.QUEEN), ChessPiece(bottom_player, -1, PIECE_TYPE.KING), ChessPiece(bottom_player, -1, PIECE_TYPE.BISHOP), ChessPiece(bottom_player, -1, PIECE_TYPE.KNIGHT), ChessPiece(bottom_player, -1, PIECE_TYPE.ROOK),
    ]


def get_piece_square_tables() -> dict[Tuple[PIECE_TYPE, int], list[int]]:
    to_return: dict[Tuple[PIECE_TYPE, int], list[int]] = dict()

    to_return[(PIECE_TYPE.PAWN, 1)] = [
        50, 50, 50, 50, 50, 50, 50, 50,
        15, 20, 30, 30, 30, 30, 20, 15,
        10, 13, 15, 15, 15, 15, 13, 10,
        5, 7, 10, 10, 10, 10, 7, 5,
        3, 4, 8, 8, 8, 8, 4, 3,
        2, 3, 6, 6, 6, 6, 3, 2,
        1, 2, 4, 4, 4, 4, 2, 1,
        0, 0, 0, 0, 0, 0, 0, 0,
    ]

    to_return[(PIECE_TYPE.PAWN, 2)] = [
        0, 0, 0, 0, 0, 0, 0, 0,
        1, 2, 4, 4, 4, 4, 2, 1,
        2, 3, 6, 6, 6, 6, 3, 2,
        3, 4, 8, 8, 8, 8, 4, 3,
        5, 7, 10, 10, 10, 10, 7, 5,
        10, 13, 15, 15, 15, 15, 13, 10,
        15, 20, 30, 30, 30, 30, 20, 15,
        50, 50, 50, 50, 50, 50, 50, 50,
    ]

    center = [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 10, 10, 10, 10, 10, 10, 0,
        5, 10, 30, 30, 30, 30, 10, 5,
        5, 10, 30, 50, 50, 30, 10, 5,
        5, 10, 30, 50, 50, 30, 10, 5,
        5, 10, 30, 30, 30, 30, 10, 5,
        0, 10, 10, 10, 10, 10, 10, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    to_return[(PIECE_TYPE.ROOK, 1)] = [
        10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 15, 15, 15, 15, 10, 10,
        10, 15, 20, 20, 20, 20, 15, 10,
        10, 20, 30, 30, 30, 30, 20, 10,
        8, 15, 20, 25, 25, 20, 15, 8,
        5, 10, 15, 20, 20, 15, 10, 5,
        2, 4, 8, 10, 10, 8, 4, 2,
        0, 0, 0, 50, 0, 50, 0, 0
    ]

    to_return[(PIECE_TYPE.ROOK, 2)] = [
        0, 0, 0, 50, 0, 50, 0, 0,
        2, 4, 8, 10, 10, 8, 4, 2,
        5, 10, 15, 20, 20, 15, 10, 5,
        8, 15, 20, 25, 25, 20, 15, 8,
        10, 20, 30, 30, 30, 30, 20, 10,
        10, 15, 20, 20, 20, 20, 15, 10,
        10, 10, 15, 15, 15, 15, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10,
    ]

    to_return[(PIECE_TYPE.KING, 1)] = [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 5, 5, 5, 5, 5, 5, 5,
        10, 10, 10, 10, 10, 10, 10, 10,
        20, 20, 50, 20, 20, 20, 50, 20,
    ]

    to_return[(PIECE_TYPE.KING, 2)] = [
        20, 20, 50, 20, 20, 20, 50, 20,
        10, 10, 10, 10, 10, 10, 10, 10,
        5, 5, 5, 5, 5, 5, 5, 5,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
    ]

    to_return[(PIECE_TYPE.BISHOP, 1)] = center
    to_return[(PIECE_TYPE.BISHOP, 2)] = center
    to_return[(PIECE_TYPE.KNIGHT, 1)] = center
    to_return[(PIECE_TYPE.KNIGHT, 2)] = center
    to_return[(PIECE_TYPE.QUEEN, 1)] = center
    to_return[(PIECE_TYPE.QUEEN, 2)] = center

    return to_return