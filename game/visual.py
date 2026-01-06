from typing import Tuple
from game.common import PIECE_TYPE, PLAYER_TYPES, Move
from game.chessboard import ChessBoard
from game.bot import easy_bot_input, hard_bot_input

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
positions = [letter.lower() + str(val) for letter in letters for val in range(8)]

def terminal_interface_loop(board: ChessBoard, player_types: list[PLAYER_TYPES]) -> None:
    while board.running:
        player_type = player_types[board.current_player - 1]
        print_board(board)

        match player_type:
            case PLAYER_TYPES.HUMAN:
                board.make_move(get_human_input(board))

            case PLAYER_TYPES.EASY_BOT:
                board.make_move(easy_bot_input(board))

            case PLAYER_TYPES.HARD_BOT:
                board.make_move(hard_bot_input(board, 5))

    print_board(board)
    print(f"{"White" if board.winner == 1 else "Green"} won in {board.get_turn_number()} moves.")
    for move in board.moves_list:
        print(move)


def get_tuple(pos: str) -> Tuple[int, int] | None:
    if len(pos) != 2:
        return

    return (int(pos[1]), letters.index(pos[0].upper()))


def get_marker(tup: Tuple[int, int]):
    return letters[tup[1]].lower() + str(tup[0])


def print_board(board: ChessBoard) -> None:
    start = 0
    end = board.WIDTH


    print(f"  {"".join([f"  {i} " for i in letters[:board.WIDTH]])}")
    print(f"  {"-" * 33}")

    for row_i in range(board.HEIGHT):
        row = board.tiles[start:end]
        print(f"{row_i} ", end="")
        for i, piece in enumerate(row):
            print("|", end="")
            print(f"\x1b[{'48;5;243' if (row_i + i) % 2 == 1 else '0'}m", end="")

            if piece is None:
                print("   \x1b[0m", end="")
                continue

            print(f" {f"\x1b[97m" if piece.owner == 1 else "\x1b[92m"}{str(piece)} \x1b[0m", end="")
        print("|")

        start += board.WIDTH
        end += board.WIDTH
        print(f"  {"-" * 33}")


def get_human_input(board: ChessBoard) -> Move:
    result = single_human_input(board)

    while result is None:
        print_board(board)
        result = single_human_input(board)

    return result


def single_human_input(board: ChessBoard) -> Move | None:
    user_input = input(">").strip().split(" ")

    match user_input[0]:
        case "?":
            print("""
To move a piece, you must supply the piece you would like to moves location
and then the destiation for the selected piece. You enter this information
in row-major order, using the indicators on the side for help.

Example:

"e4 e6" moves piece on e4 to e6 if it is valid
            """)

        case "check":
            print("Yes" if board.check_for_check(1 if user_input[1] == "white" else 2) else "No")
            return

        case "turn":
            print("White" if board.current_player == 1 else "Green")
            return

        case "undo":
            board.undo_move()
            board.undo_move()
            return

        case _:
            if user_input[0] in positions and len(user_input) == 1:
                coords = get_tuple(user_input[0])
                if coords:
                    print([get_marker(piece.destination) for piece in board.get_piece_moves(coords)])
                return

            elif user_input[0] in positions and len(user_input) == 2:
                coords = get_tuple(user_input[0])
                if coords:
                    moves = board.get_piece_moves(coords)

                    for move in moves:
                        if move.destination == get_tuple(user_input[1]):
                            if move.promotion:
                                promotion_string = input("What piece would you like to promote to?: ")

                                match promotion_string.strip().lower():
                                    case "bishop":
                                        promotion_piece = PIECE_TYPE.BISHOP
                                    case "rook":
                                        promotion_piece = PIECE_TYPE.ROOK
                                    case "knight":
                                        promotion_piece = PIECE_TYPE.KNIGHT
                                    case "queen":
                                        promotion_piece = PIECE_TYPE.QUEEN
                                    case _:
                                        print("Piece Not found")
                                        return
                                
                                move.promotion = promotion_piece
                            return move
                    print("Move not found in valid moves")

            else:
                print("Command Not Recognized")
                return