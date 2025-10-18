import chess
import torch
from src.neural_evaluator import NeuralEvaluator
from src.minimax_engine import MinimaxEngine

class NeuralEvaluation:
    """Neural network evaluation architecture"""
    
    def __init__(self, depth=3):
        self.minimax_engine = MinimaxEngine(depth=depth)
        self.neural_evaluator = NeuralEvaluator()
        self.architecture_type = "neural_evaluation"
        
    def analyze_position(self, board):
        """Complete position analysis using neural network evaluation"""
        analysis = {
            "architecture": self.architecture_type,
            "best_move": None,
            "evaluation": 0,
            "nodes_searched": 0,
            "neural_trained": self.neural_evaluator.trained,
            "search_depth": self.minimax_engine.depth
        }
        
        # Use neural network for evaluation in minimax search
        original_evaluator = self.minimax_engine.evaluator
        if self.neural_evaluator.trained:
            self.minimax_engine.evaluator = self.neural_evaluator
        
        # Get best move
        best_move, score = self.minimax_engine.search(board)
        analysis["best_move"] = best_move
        analysis["evaluation"] = score / 100
        analysis["nodes_searched"] = self.minimax_engine.nodes_searched
        
        # Restore original evaluator
        self.minimax_engine.evaluator = original_evaluator
        
        # Neural network features
        analysis["neural_features"] = self._extract_neural_features(board)
        
        return analysis
    
    def _extract_neural_features(self, board):
        """Extract neural network specific features"""
        features = {
            "neural_confidence": self._get_neural_confidence(board),
            "position_complexity": self._estimate_complexity(board),
            "training_status": "trained" if self.neural_evaluator.trained else "untrained"
        }
        
        if self.neural_evaluator.trained:
            # Get raw neural network output
            with torch.no_grad():
                tensor = self.neural_evaluator.board_to_tensor(board)
                raw_output = self.neural_evaluator.model(tensor).item()
                features["raw_neural_output"] = raw_output
                features["evaluation_consistency"] = self._check_evaluation_consistency(board)
        
        return features
    
    def _get_neural_confidence(self, board):
        """Estimate neural network confidence in evaluation"""
        if not self.neural_evaluator.trained:
            return 0.0
            
        # Simple confidence based on evaluation magnitude
        evaluation = abs(self.neural_evaluator.evaluate(board)) / 100
        return min(evaluation / 5.0, 1.0)  # Normalize to 0-1
    
    def _estimate_complexity(self, board):
        """Estimate position complexity"""
        legal_moves = len(list(board.legal_moves))
        piece_count = len(board.piece_map())
        
        # Simple complexity metric
        complexity = (legal_moves * piece_count) / 100.0
        return min(complexity, 1.0)
    
    def _check_evaluation_consistency(self, board):
        """Check if neural and classical evaluations agree"""
        neural_eval = self.neural_evaluator.evaluate(board) / 100
        from src.chess_evaluator import ChessEvaluator
        classical_eval = ChessEvaluator.evaluate(board) / 100
        
        difference = abs(neural_eval - classical_eval)
        return "high" if difference < 1.0 else "low"
