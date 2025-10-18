import chess
from .classical_search import ClassicalSearch
from .expert_system import ExpertSystem
from .neural_evaluation import NeuralEvaluation

class HybridEngine:
    """Hybrid architecture combining multiple approaches"""
    
    def __init__(self):
        self.classical = ClassicalSearch(depth=3)
        self.expert = ExpertSystem(depth=15)
        self.neural = NeuralEvaluation(depth=3)
        self.architecture_type = "hybrid_engine"
        
    def analyze_position(self, board):
        """Comprehensive analysis using all architectures"""
        analysis = {
            "architecture": self.architecture_type,
            "comparative_analysis": {},
            "recommended_engine": None,
            "confidence_score": 0.0
        }
        
        # Get analysis from all architectures
        classical_analysis = self.classical.analyze_position(board)
        expert_analysis = self.expert.analyze_position(board) 
        neural_analysis = self.neural.analyze_position(board)
        
        # Comparative analysis
        analysis["comparative_analysis"] = {
            "classical": classical_analysis,
            "expert": expert_analysis,
            "neural": neural_analysis
        }
        
        # Determine best engine recommendation
        analysis["recommended_engine"] = self._select_best_engine(
            classical_analysis, expert_analysis, neural_analysis
        )
        
        # Overall confidence score
        analysis["confidence_score"] = self._calculate_confidence(
            classical_analysis, expert_analysis, neural_analysis
        )
        
        return analysis
    
    def _select_best_engine(self, classical, expert, neural):
        """Select the most appropriate engine for the position"""
        
        # If Stockfish is available and position is complex, prefer it
        if expert.get("engine_available", False) and not classical.get("position_features", {}).get("pawn_structure", 0) == 0:
            return "expert_system"
        
        # If neural network is trained and position is typical, use it
        if neural.get("neural_trained", False) and neural.get("neural_features", {}).get("neural_confidence", 0) > 0.7:
            return "neural_evaluation"
        
        # Default to classical for simple positions
        return "classical_search"
    
    def _calculate_confidence(self, classical, expert, neural):
        """Calculate overall confidence in analysis"""
        confidence = 0.0
        factors = 0
        
        # Classical confidence
        if classical.get("nodes_searched", 0) > 1000:
            confidence += 0.3
            factors += 1
        
        # Expert confidence  
        if expert.get("engine_available", False):
            confidence += 0.4
            factors += 1
        
        # Neural confidence
        if neural.get("neural_trained", False) and neural.get("neural_features", {}).get("neural_confidence", 0) > 0.5:
            confidence += 0.3
            factors += 1
        
        return confidence / factors if factors > 0 else 0.0
    
    def get_architecture_comparison(self, board):
        """Get detailed comparison of all architectures"""
        comparison = {
            "performance_metrics": self._compare_performance(board),
            "accuracy_estimates": self._estimate_accuracy(board),
            "computational_overhead": self._calculate_overhead(board)
        }
        return comparison
    
    def _compare_performance(self, board):
        """Compare performance metrics across architectures"""
        import time
        
        metrics = {}
        
        # Time classical search
        start = time.time()
        self.classical.analyze_position(board)
        metrics["classical_time"] = time.time() - start
        
        # Time neural evaluation
        start = time.time()
        self.neural.analyze_position(board)
        metrics["neural_time"] = time.time() - start
        
        # Stockfish time (if available)
        if self.expert.engine.available:
            start = time.time()
            self.expert.analyze_position(board)
            metrics["expert_time"] = time.time() - start
        
        return metrics
    
    def _estimate_accuracy(self, board):
        """Estimate accuracy of each architecture"""
        accuracy = {
            "classical": 0.75,  # Based on your research
            "neural": 0.85,     # Based on your research  
            "expert": 0.98      # Based on your research
        }
        return accuracy
    
    def _calculate_overhead(self, board):
        """Calculate computational overhead"""
        overhead = {
            "classical": "medium",    # Your research finding
            "neural": "low",          # 60% reduction per your research
            "expert": "high"          # Stockfish is resource-intensive
        }
        return overhead
