import chess
from stockfish import Stockfish

class StockfishEngine:
    """Wrapper for Stockfish chess engine expert system"""
    
    def __init__(self, depth=15):
        try:
            self.engine = Stockfish(depth=depth)
            self.available = True
        except Exception as e:
            print(f"Stockfish not available: {e}")
            self.available = False

    def get_best_move(self, board):
        """Get best move from Stockfish expert system"""
        if not self.available:
            return None, 0

        self.engine.set_fen_position(board.fen())
        best_move = self.engine.get_best_move()
        evaluation = self.engine.get_evaluation()

        # Convert evaluation to numeric score
        eval_score = 0
        if evaluation['type'] == 'cp':
            eval_score = evaluation['value'] / 100.0
        elif evaluation['type'] == 'mate':
            eval_score = 10000 if evaluation['value'] > 0 else -10000

        return chess.Move.from_uci(best_move) if best_move else None, eval_score

    def evaluate_position(self, board):
        """Get position evaluation from Stockfish"""
        if not self.available:
            return 0

        self.engine.set_fen_position(board.fen())
        evaluation = self.engine.get_evaluation()

        if evaluation['type'] == 'cp':
            return evaluation['value'] / 100.0
        elif evaluation['type'] == 'mate':
            return 10000 if evaluation['value'] > 0 else -10000
        return 0
