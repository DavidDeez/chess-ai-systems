import chess
from src.chess_evaluator import ChessEvaluator
from src.minimax_engine import MinimaxEngine

class ClassicalSearch:
    """Classical minimax search architecture with hand-crafted evaluation"""
    
    def __init__(self, depth=3):
        self.engine = MinimaxEngine(depth=depth)
        self.evaluator = ChessEvaluator()
        self.architecture_type = "classical_search"
        
    def analyze_position(self, board):
        """Complete position analysis using classical methods"""
        analysis = {
            "architecture": self.architecture_type,
            "best_move": None,
            "evaluation": 0,
            "nodes_searched": 0,
            "search_depth": self.engine.depth
        }
        
        # Get best move and evaluation
        best_move, score = self.engine.search(board)
        analysis["best_move"] = best_move
        analysis["evaluation"] = score / 100  # Normalize
        analysis["nodes_searched"] = self.engine.nodes_searched
        
        # Position features
        analysis["position_features"] = self._extract_classical_features(board)
        
        return analysis
    
    def _extract_classical_features(self, board):
        """Extract hand-crafted chess features"""
        features = {
            "material_balance": self.evaluator.evaluate(board) / 100,
            "mobility": len(list(board.legal_moves)),
            "center_control": self._calculate_center_control(board),
            "pawn_structure": self._evaluate_pawn_structure(board),
            "king_safety": self._evaluate_king_safety(board)
        }
        return features
    
    def _calculate_center_control(self, board):
        """Calculate control of center squares"""
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        control = 0
        for square in center_squares:
            if board.piece_at(square):
                piece = board.piece_at(square)
                if piece.color == chess.WHITE:
                    control += 1
                else:
                    control -= 1
        return control
    
    def _evaluate_pawn_structure(self, board):
        """Simple pawn structure evaluation"""
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        return len(white_pawns) - len(black_pawns)
    
    def _evaluate_king_safety(self, board):
        """Basic king safety evaluation"""
        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)
        
        # Simple: kings in corner are safer
        safety = 0
        if white_king in [chess.A1, chess.H1, chess.A8, chess.H8]:
            safety += 1
        if black_king in [chess.A1, chess.H1, chess.A8, chess.H8]:
            safety -= 1
            
        return safety
