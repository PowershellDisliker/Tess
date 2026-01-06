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