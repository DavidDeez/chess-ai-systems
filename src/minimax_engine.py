import chess
from .chess_evaluator import ChessEvaluator

class MinimaxEngine:
    """Minimax chess engine with alpha-beta pruning"""
    
    def __init__(self, depth=3):
        self.depth = depth
        self.evaluator = ChessEvaluator()
        self.nodes_searched = 0

    def search(self, board):
        """Find best move using minimax with alpha-beta pruning"""
        self.nodes_searched = 0
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)

        return best_move, best_score

    def minimax(self, board, depth, alpha, beta, maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        self.nodes_searched += 1

        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)

        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
