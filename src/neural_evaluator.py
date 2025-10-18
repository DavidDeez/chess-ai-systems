import torch
import torch.nn as nn
import chess
import numpy as np
import random

class ChessNeuralNetwork(nn.Module):
    """Neural network for chess position evaluation"""
    
    def __init__(self):
        super(ChessNeuralNetwork, self).__init__()
        self.conv1 = nn.Conv2d(12, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        
        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x

class NeuralEvaluator:
    """Neural network-based position evaluator"""
    
    def __init__(self):
        self.model = ChessNeuralNetwork()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.trained = False

    def board_to_tensor(self, board):
        """Convert chess board to neural network input tensor"""
        tensor = np.zeros((12, 8, 8), dtype=np.float32)
        
        piece_idx = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                rank, file = divmod(square, 8)
                idx = piece_idx[piece.piece_type] + (0 if piece.color == chess.WHITE else 6)
                tensor[idx][7-rank][file] = 1.0  # Flip rank for correct orientation

        return torch.FloatTensor(tensor).unsqueeze(0).to(self.device)

    def evaluate(self, board):
        """Evaluate position using neural network"""
        if not self.trained:
            from .chess_evaluator import ChessEvaluator
            return ChessEvaluator.evaluate(board)

        self.model.eval()
        with torch.no_grad():
            tensor = self.board_to_tensor(board)
            score = self.model(tensor).item()

        return score * 100  # Scale to similar range as classic evaluator

    def train(self, positions, labels, epochs=10):
        """Train neural network on labeled positions"""
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

        for epoch in range(epochs):
            total_loss = 0
            for i in range(0, len(positions), 32):
                batch_positions = torch.cat(positions[i:i+32])
                batch_labels = torch.FloatTensor(labels[i:i+32]).to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_positions).squeeze()
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()

            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(positions):.4f}")

        self.trained = True
