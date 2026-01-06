from game.chessboard import ChessBoard
from game.bot.common import get_pieces_to_moves
from game.common import Move

from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy


def hard_bot_input(board: ChessBoard, max_depth: int) -> Move:
    pieces_to_move = get_pieces_to_moves(board, board.current_player)

    tasks = []
    for moves in pieces_to_move.values():
        for move in moves:
            new_board = deepcopy(board)
            new_board.make_move(move)
            tasks.append((move, new_board))

    if not tasks:
        raise ValueError("No moves available")

    results = []
    with ProcessPoolExecutor() as executor:
        future_to_move = {
            executor.submit(hard_bot_internal, b, max_depth, 1, -float('inf'), float('inf')): m 
            for m, b in tasks
        }
        
        for future in future_to_move:
            move = future_to_move[future]
            score = future.result()
            results.append((score, move))

    if board.current_player == board.PLAYER_1:
        best_score, best_move = max(results, key=lambda x: x[0])
    else:
        best_score, best_move = min(results, key=lambda x: x[0])

    return best_move

def hard_bot_internal(board: ChessBoard, max_depth: int, current_depth: int, alpha: float, beta: float) -> float:
    if board.winner is not None or current_depth == max_depth:
        return board.get_score(current_depth)

    moving_player = board.current_player
    pieces_to_moves = get_pieces_to_moves(board, moving_player)
    
    if not pieces_to_moves:
        return board.get_score(current_depth)

    if moving_player == board.PLAYER_1:
        max_eval = -float('inf')
        for piece, moves in pieces_to_moves.items():
            for move in moves:
                board.make_move(move)
                eval_score = hard_bot_internal(board, max_depth, current_depth + 1, alpha, beta)
                board.undo_move()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    return max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for piece, moves in pieces_to_moves.items():
            for move in moves:
                board.make_move(move)
                eval_score = hard_bot_internal(board, max_depth, current_depth + 1, alpha, beta)
                board.undo_move()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    return min_eval
        return min_eval