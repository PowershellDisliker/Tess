from typing import Tuple
from game.common import PIECE_TYPE, PLAYER_TYPES, Move
from game.chessboard import ChessBoard
from game.bot import easy_bot_input, hard_bot_input
from game.visual.colors import color_text

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
positions = [letter.lower() + str(val) for letter in letters for val in range(1, 9)]

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
                board.make_move(hard_bot_input(board, 4))

    print_board(board)
    print(f"{"White" if board.winner == 1 else "Green"} won in {board.get_turn_number()} moves.")
    for move in board.moves_list:
        print(move)


def get_tuple(pos: str) -> Tuple[int, int] | None:
    if len(pos) != 2:
        return

    return (8 - int(pos[1]), letters.index(pos[0].upper()))


def get_marker(tup: Tuple[int, int]):
    return letters[tup[1]].lower() + str(8 - tup[0])


def print_board(board: ChessBoard, highlight_tiles: list[Tuple[int, int]] | None = None) -> None:
    tile_radius = 1
    legend_foreground_color = "white"
    legend_background_color = None
    tile_color_1 = "gray-0600"
    tile_color_2 = "gray-1600"
    tile_highlight = "red"
    player_1_piece_color = "gray-2400"
    player_2_piece_color = "gray-0100"

    start = 0
    end = board.WIDTH


    print(f"   {" " * tile_radius}{f"{" " * (tile_radius * 2 + 2)}".join([str(color_text(let, foreground_color=legend_foreground_color, background_color=legend_background_color)) for let in letters[:board.WIDTH]])}")

    for row_i in range(board.HEIGHT):
        row = board.tiles[start:end]

        pad = [False] * tile_radius
        values: list[bool] = []
        values.extend(pad)
        values.append(True)
        values.extend(pad)

        for val in values:

            if val:
                print(f"{8 - row_i} ", end="")
            else:
                print(end="  ")

            for col_i, piece in enumerate(row):
                if highlight_tiles and (row_i, col_i) in highlight_tiles:
                    background_color = tile_highlight
                else:
                    background_color = tile_color_1 if (row_i + col_i) % 2 == 1 else tile_color_2
                radius = " " * (tile_radius + 1)

                if piece and val:
                    print(color_text(radius + str(piece) + radius, foreground_color=player_1_piece_color if piece.owner == 1 else player_2_piece_color, background_color=background_color, bold=True), end="")
                else:
                    print(color_text(radius + " " + radius, background_color=background_color), end="")

            print()

        start += board.WIDTH
        end += board.WIDTH


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

        case "score":
            print(board.get_score(0))
            return

        case _:
            if user_input[0] in positions and len(user_input) == 1:
                coords = get_tuple(user_input[0])
                if coords:
                    print_board(board, highlight_tiles=[piece.destination for piece in board.get_piece_moves(coords)])
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
                print("""Command not recognized. Use "?" for help.""")
                return