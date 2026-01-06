from game.chessboard import ChessBoard
from game.common import PLAYER_TYPES
from game.visual import terminal_interface_loop
import sys

def main() -> None:

    player_1 = sys.argv[1]
    player_2 = sys.argv[2]

    players = [get_player_type(player_1), get_player_type(player_2)]

    game = ChessBoard()
    terminal_interface_loop(game, players)


def get_player_type(val: str) -> PLAYER_TYPES:
    match val.strip().lower():
        case "human":
            return PLAYER_TYPES.HUMAN
        case "easy":
            return PLAYER_TYPES.EASY_BOT
        case "hard":
            return PLAYER_TYPES.HARD_BOT
        case _:
            raise ValueError(f"Passed value: {val} can not be converted to a player type")


if __name__ == "__main__":
    main()