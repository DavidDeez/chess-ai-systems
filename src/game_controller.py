import chess
from .minimax_engine import MinimaxEngine
from .stockfish_engine import StockfishEngine
from .neural_evaluator import NeuralEvaluator

class ChessGame:
    """Main chess game controller coordinating all engines"""
    
    def __init__(self):
        self.board = chess.Board()
        self.minimax_engine = MinimaxEngine(depth=3)
        self.stockfish_engine = StockfishEngine()
        self.neural_evaluator = NeuralEvaluator()
        self.move_history = []
        self.current_engine = "minimax"

    def make_move(self, move_uci):
        """Make a move on the board"""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(self.board.san(move))
                return True
            return False
        except:
            return False

    def get_ai_move(self, engine_type="minimax", depth=3):
        """Get move from specified AI engine"""
        self.minimax_engine.depth = depth
        self.current_engine = engine_type

        if engine_type == "stockfish" and self.stockfish_engine.available:
            move, score = self.stockfish_engine.get_best_move(self.board)
            engine_name = "Stockfish"
        elif engine_type == "neural":
            # Use neural evaluator with minimax search
            move, score = self.minimax_engine.search(self.board)
            engine_name = "Neural-Minimax"
        else:
            move, score = self.minimax_engine.search(self.board)
            engine_name = "Minimax"

        if move and not self.board.is_game_over():
            self.board.push(move)
            self.move_history.append(self.board.san(move))
            return move, score, engine_name

        return None, 0, engine_name

    def get_evaluation_comparison(self):
        """Get evaluation from all engines for comparison"""
        evaluations = {}
        
        # Classic minimax evaluation
        classic_eval = self.minimax_engine.evaluator.evaluate(self.board) / 100
        evaluations["Classic"] = classic_eval

        # Stockfish evaluation
        if self.stockfish_engine.available:
            sf_eval = self.stockfish_engine.evaluate_position(self.board)
            evaluations["Stockfish"] = sf_eval

        # Neural network evaluation
        if self.neural_evaluator.trained:
            nn_eval = self.neural_evaluator.evaluate(self.board) / 100
            evaluations["Neural"] = nn_eval

        return evaluations

    def reset_game(self):
        """Reset the game state"""
        self.board = chess.Board()
        self.move_history = []
        return self.board.fen()
