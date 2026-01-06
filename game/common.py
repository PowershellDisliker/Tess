from typing import Tuple
from enum import Enum

class PIECE_TYPE(Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5


class MOVE_RESPONSE(Enum):
    SUCCESS = 0
    INVALID_OUT_OF_TURN = 1
    INVALID_ERROR_FETCHING_TILE = 2
    INVALID_TILE_IS_NONE = 3
    INVALID_MOVEMENT = 4
    INVALID_PUTS_SELF_IN_CHECK = 5


class PLAYER_TYPES(Enum):
    HUMAN = 0
    EASY_BOT = 1
    HARD_BOT = 2


class ChessPiece():

    def __init__(self, owner: int, direction: int, piece_type: PIECE_TYPE) -> None:
        self.piece_type = piece_type
        self.owner = owner
        self.direction = direction
        self.moved = False

    def set_moved(self) -> None:
        self.moved = True

    def __str__(self) -> str:
        match self.piece_type:
            case PIECE_TYPE.KING:
                return "k"
            case PIECE_TYPE.QUEEN:
                return "q"
            case PIECE_TYPE.BISHOP:
                return "b"
            case PIECE_TYPE.KNIGHT:
                return "n"
            case PIECE_TYPE.ROOK:
                return "r"
            case PIECE_TYPE.PAWN:
                return "p"


class Move():
    def __init__(
            self,
            source: Tuple[int, int],
            destination: Tuple[int, int],
            moved: bool,
            double_moved_pawn: Tuple[int, int] | None = None,
            promotion: PIECE_TYPE | None = None,
            taken_piece: Tuple[ChessPiece, Tuple[int, int]] | None = None,
            castled_rook: Tuple[Tuple[int, int], Tuple[int, int]] | None = None
        ) -> None:

        self.source = source
        self.destination = destination
        self.moved = moved
        self.double_moved_pawn = double_moved_pawn
        self.promotion = promotion
        self.taken_piece = taken_piece
        self.castled_rook = castled_rook

    def __eq__(self, other) -> bool:
        if self.source == other.source and \
        self.destination == other.destination and \
        self.moved == other.moved and \
        self.double_moved_pawn == other.double_moved_pawn and \
        self.promotion == other.promotion and \
        self.taken_piece == other.taken_piece and \
        self.castled_rook == other.castled_rook:
            return True
        return False

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination} {"Promotion " if self.promotion else ""}{f"Take {self.taken_piece[0]} " if self.taken_piece else ""}{"Castled" if self.castled_rook else ""}"


def get_index(pos: Tuple[int ,int]) -> int | None:
    for val in pos:
        if val > 7 or val < 0:
            return None

    return pos[0] * 8 + pos[1]


def get_coords(index: int) -> Tuple[int, int]:
    return (index // 8, index % 8)


def add_tuples(one: Tuple[int, int], two: Tuple[int, int]) -> Tuple[int, int]:
    return (one[0] + two[0], one[1] + two[1])