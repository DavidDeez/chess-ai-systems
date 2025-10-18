import chess
from src.stockfish_engine import StockfishEngine

class ExpertSystem:
    """Stockfish expert system integration architecture"""
    
    def __init__(self, depth=15):
        self.engine = StockfishEngine(depth=depth)
        self.architecture_type = "expert_system"
        
    def analyze_position(self, board):
        """Complete position analysis using Stockfish expert system"""
        analysis = {
            "architecture": self.architecture_type,
            "best_move": None,
            "evaluation": 0,
            "engine_available": self.engine.available,
            "search_depth": 15  # Stockfish default
        }
        
        if not self.engine.available:
            analysis["error"] = "Stockfish engine not available"
            return analysis
        
        # Get Stockfish analysis
        best_move, evaluation = self.engine.get_best_move(board)
        analysis["best_move"] = best_move
        analysis["evaluation"] = evaluation
        
        # Expert system features
        analysis["expert_features"] = self._extract_expert_features(board)
        
        return analysis
    
    def _extract_expert_features(self, board):
        """Extract expert-level position analysis"""
        if not self.engine.available:
            return {}
            
        self.engine.engine.set_fen_position(board.fen())
        
        features = {
            "position_analysis": self.engine.engine.get_evaluation(),
            "top_moves": self.engine.engine.get_top_moves(3),
            "wdl_stats": self._get_win_draw_loss_stats(),
            "theoretical_eval": self._get_theoretical_evaluation(board)
        }
        
        return features
    
    def _get_win_draw_loss_stats(self):
        """Get win/draw/loss statistics from Stockfish"""
        try:
            # This would require Stockfish with WDL support
            return {"win": 0, "draw": 0, "loss": 0}  # Placeholder
        except:
            return {"win": 0, "draw": 0, "loss": 0}
    
    def _get_theoretical_evaluation(self, board):
        """Check if position is in opening theory"""
        # Simple implementation - could use opening database
        opening_moves = ["e2e4", "d2d4", "c2c4", "g1f3"]
        if len(board.move_stack) < 8:
            return "opening"
        elif len(board.move_stack) < 25:
            return "middlegame"
        else:
            return "endgame"
