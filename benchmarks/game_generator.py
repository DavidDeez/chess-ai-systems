import chess
import chess.pgn
import random
from io import StringIO

class GameGenerator:
    """Generate training games and test positions for benchmarking"""
    
    def __init__(self):
        self.games_generated = 0
        self.positions_generated = 0
    
    def generate_random_games(self, num_games=50, max_moves=40):
        """Generate random games for training and testing"""
        games = []
        
        print(f"🎲 Generating {num_games} random games...")
        
        for game_num in range(num_games):
            board = chess.Board()
            moves = []
            moves_played = 0
            
            while not board.is_game_over() and moves_played < max_moves:
                legal_moves = list(board.legal_moves)
                
                # Mix of random and somewhat reasonable moves
                if random.random() < 0.7 and len(legal_moves) > 1:
                    # Prefer central moves and captures
                    central_moves = [m for m in legal_moves if self._is_central_move(m)]
                    capture_moves = [m for m in legal_moves if board.is_capture(m)]
                    
                    if capture_moves and random.random() < 0.6:
                        move = random.choice(capture_moves)
                    elif central_moves:
                        move = random.choice(central_moves[:min(3, len(central_moves))])
                    else:
                        move = random.choice(legal_moves[:min(5, len(legal_moves))])
                else:
                    move = random.choice(legal_moves)
                
                moves.append(move)
                board.push(move)
                moves_played += 1
            
            game_data = {
                "game_id": game_num + 1,
                "moves": [move.uci() for move in moves],
                "final_fen": board.fen(),
                "result": self._get_game_result(board),
                "total_moves": moves_played
            }
            
            games.append(game_data)
            
            if (game_num + 1) % 10 == 0:
                print(f"  Generated {game_num + 1}/{num_games} games")
        
        self.games_generated += num_games
        return games
    
    def extract_test_positions(self, games, positions_per_game=3):
        """Extract test positions from generated games"""
        test_positions = []
        
        print("📋 Extracting test positions from games...")
        
        for game in games:
            board = chess.Board()
            moves = [chess.Move.from_uci(move) for move in game["moves"]]
            
            # Sample positions at different game stages
            sampling_points = [
                min(8, len(moves)),  # Opening
                min(len(moves) // 2, len(moves)),  # Middlegame
                min(len(moves) - 5, len(moves))   # Late game
            ]
            
            for move_idx in sampling_points:
                if move_idx < len(moves):
                    # Replay to this position
                    temp_board = chess.Board()
                    for i in range(move_idx):
                        temp_board.push(moves[i])
                    
                    position_data = {
                        "fen": temp_board.fen(),
                        "move_number": move_idx + 1,
                        "game_phase": self._classify_game_phase(temp_board),
                        "complexity": self._calculate_position_complexity(temp_board)
                    }
                    
                    test_positions.append(position_data)
        
        self.positions_generated += len(test_positions)
        print(f"✅ Extracted {len(test_positions)} test positions")
        return test_positions
    
    def create_accuracy_test_suite(self, num_positions=30):
        """Create test suite with known best moves for accuracy testing"""
        test_suite = []
        
        # Classic chess puzzles and positions with known solutions
        classic_positions = [
            {
                "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
                "best_move": "f3e5",  # Fork
                "description": "Knight fork opportunity"
            },
            {
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/3P1N2/PPP2PPP/RNBQKB1R w KQkq - 0 1", 
                "best_move": "d3d4",  # Center control
                "description": "Center pawn break"
            },
            # Add more known test positions
        ]
        
        # Generate additional random test positions
        random_games = self.generate_random_games(num_games=10, max_moves=25)
        random_positions = self.extract_test_positions(random_games, positions_per_game=2)
        
        # Use Stockfish to determine best moves for random positions
        try:
            from src.stockfish_engine import StockfishEngine
            stockfish = StockfishEngine()
            
            if stockfish.available:
                for position in random_positions[:20]:  # Limit for speed
                    board = chess.Board(position["fen"])
                    best_move, _ = stockfish.get_best_move(board)
                    
                    if best_move:
                        test_suite.append({
                            "fen": position["fen"],
                            "best_move": best_move.uci(),
                            "description": f"Generated position - {position['game_phase']}"
                        })
        except:
            pass
        
        # Add classic positions
        test_suite.extend(classic_positions)
        
        print(f"✅ Created accuracy test suite with {len(test_suite)} positions")
        return test_suite[:num_positions]  # Limit to requested number
    
    def _is_central_move(self, move):
        """Check if move is to central squares"""
        central_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        return move.to_square in central_squares
    
    def _get_game_result(self, board):
        """Determine game result"""
        if board.is_checkmate():
            return "checkmate"
        elif board.is_stalemate():
            return "stalemate" 
        elif board.is_insufficient_material():
            return "insufficient_material"
        elif board.can_claim_draw():
            return "draw"
        else:
            return "in_progress"
    
    def _classify_game_phase(self, board):
        """Classify game phase based on piece count and move number"""
        piece_count = len(board.piece_map())
        move_number = board.fullmove_number
        
        if piece_count >= 30 and move_number < 15:
            return "opening"
        elif piece_count >= 20:
            return "middlegame"
        else:
            return "endgame"
    
    def _calculate_position_complexity(self, board):
        """Calculate position complexity score"""
        legal_moves = len(list(board.legal_moves))
        piece_count = len(board.piece_map())
        capture_moves = len([m for m in board.legal_moves if board.is_capture(m)])
        
        complexity = (legal_moves * piece_count * (capture_moves + 1)) / 100.0
        return min(complexity, 10.0)  # Scale to 0-10
    
    def export_training_data(self, games, filename="training_games.json"):
        """Export generated games to file"""
        import json
        
        export_data = {
            "total_games": len(games),
            "total_positions": self.positions_generated,
            "games": games
        }
        
        with open(f"benchmarks/results/{filename}", "w") as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Training data exported to benchmarks/results/{filename}")
