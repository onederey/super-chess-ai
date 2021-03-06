import ai
import chess
from chessboard import display #play test

class Player():

    def __init__(self, depth):
        self.depth = depth
        self.AI = ai.ChessAIStockfishEval()
        self.board = chess.Board()

    def ai_move(self, strategy, color = False):
        print("AI is thinking...")
        if strategy == "random":
            move = self.AI.random_ultimate(self.board)[0]
            self.board.push(move)
        elif strategy == "custom":
            move = self.AI.custom_ultimate(self.board, self.depth+1, float('-inf'), float('inf'), True, color)[0]
            self.board.push(move)
        elif strategy == "stockfish":
            move = self.AI.minimax(self.board, self.depth, float('-inf'), float('inf'), True, color)[0]  #поменять на True если АИ ходит первым!
            self.board.push(move)

    def human_move(self):
        print("Your turn...")
        while True:
            move = input()
            try:
                move_uci = chess.Move.from_uci(move)
            except ValueError:
                print("Try again!")
            
            legal = list(self.board.legal_moves)
            if move_uci in legal:
                return self.board.push(move_uci)
            else:
                print("Illegal move!")

    def play(self, strategy):
        print("Starting!")
        print(self.board)
        while True:
            self.human_move()
            print(self.board)
            self.ai_move(strategy)
            print(self.board)

            if self.board.is_game_over():
                break

    def play_test(self, strategy):
        print("Starting!")
        display.start(self.board.fen())
        print(self.board)
        while True:
            self.human_move()
            print(self.board)
            display.update(self.board.fen())
            self.ai_move(strategy)
            print(self.board)
            display.update(self.board.fen())

            if self.board.is_game_over():
                break

    def play_stockfish(self):
        print("Starting!")
        display.start(self.board.fen())
        print(self.board)
        while True:
            self.ai_move("stockfish", True)
            print(self.board)
            display.update(self.board.fen())
            self.ai_move("stockfish", False)
            print(self.board)
            display.update(self.board.fen())

            if self.board.is_game_over():
                break

    def play_stockfish_vs_custom(self):
        print("Starting!")
        display.start(self.board.fen())
        print(self.board)
        while True:
            self.ai_move("custom", True)
            print(self.board)
            display.update(self.board.fen())
            self.ai_move("stockfish", False)
            print(self.board)
            display.update(self.board.fen())

            if self.board.is_game_over():
                break

    def play_random_vs_custom(self):
        print("Starting!")
        display.start(self.board.fen())
        print(self.board)
        while True:
            self.ai_move("random", True)
            print(self.board)
            display.update(self.board.fen())
            self.ai_move("custom", False)
            print(self.board)
            display.update(self.board.fen())

            if self.board.is_game_over():
                break


if __name__ == '__main__':
    game = Player(3)
    game.play_stockfish_vs_custom()
    #game.play("custom"),