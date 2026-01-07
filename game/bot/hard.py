from game.chessboard import ChessBoard
from game.common import Move
from game.bot.common import get_pieces_to_moves


def hard_bot_input(board: ChessBoard, max_depth: int) -> Move:
    pieces_to_move = get_pieces_to_moves(board, board.current_player)
    all_moves = [m for moves in pieces_to_move.values() for m in moves]
    
    if not all_moves:
        raise ValueError("No Moves Given")

    best_move = all_moves[0]
    best_eval = -float("inf")
    
    alpha = -float("inf")
    beta = float("inf")
    color = 1 if board.current_player == board.PLAYER_1 else -1
    
    for move in all_moves:
        board.make_move(move)
        eval_score = -hard_bot_internal(board, max_depth - 1, -beta, -alpha, -color)
        board.undo_move()
        
        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

        alpha = max(alpha, eval_score)
        
    return best_move

def hard_bot_internal(board: ChessBoard, depth: int, alpha: float, beta: float, color: int) -> float:
    """
    Standard Negamax with Alpha-Beta Pruning.
    'color' is 1 for PLAYER_1 and -1 for PLAYER_2.
    """
    if board.winner is not None or depth == 0:
        # Return score relative to the current player
        return color * board.get_score(depth)

    pieces_to_moves = get_pieces_to_moves(board, board.current_player)
    if not pieces_to_moves:
        return color * board.get_score(depth)

    max_eval = -float('inf')
    
    for moves in pieces_to_moves.values():
        for move in moves:
            board.make_move(move)
            eval_score = -hard_bot_internal(board, depth - 1, -beta, -alpha, -color)
            board.undo_move()
            
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            if alpha >= beta:
                return alpha  # Snip the branch
                
    return max_eval