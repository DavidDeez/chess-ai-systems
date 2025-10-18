import chess

class ChessEvaluator:
    """Classic chess position evaluator with piece-square tables"""
    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Piece-Square Tables (simplified for example)
    PST = {
        chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, ...],
        # ... your full PST tables
    }

    @staticmethod
    def evaluate(board):
        """Evaluate chess position using material and positional scoring"""
        if board.is_checkmate():
            return -20000 if board.turn else 20000
        if board.is_stalemate():
            return 0

        score = 0
        # Material and positional evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = ChessEvaluator.PIECE_VALUES[piece.piece_type]
                pst_value = ChessEvaluator.PST[piece.piece_type][square]
                
                if piece.color == chess.WHITE:
                    score += value + pst_value
                else:
                    score -= value + pst_value

        return score
