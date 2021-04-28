import os
import re
import time
import asyncio
import chess
import chess.engine
import random
from chessboard import display

PP = 100
NN = 320
BB = 330
RR = 500
QQ = 900
KK = 20000

pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -90, -90, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]]

knights = [[-50, -40, -30, -30, -30, -30, -40, -50],
           [-40, -20,  0,  0,  0,  0, -20, -40],
           [-30,  0, 10, 15, 15, 10,  0, -30],
           [-30,  5, 15, 20, 20, 15,  5, -30],
           [-30,  0, 15, 20, 20, 15,  0, -30],
           [-30,  5, 10, 15, 15, 10,  5, -30],
           [-40, -20,  0,  5,  5,  0, -20, -40],
           [-50, -40, -30, -30, -30, -30, -40, -50]]

bishops = [[-20, -10, -10, -10, -10, -10, -10, -20],
           [-10,  0,  0,  0,  0,  0,  0, -10],
           [-10,  0,  5, 10, 10,  5,  0, -10],
           [-10,  5,  5, 10, 10,  5,  5, -10],
           [-10,  0, 10, 10, 10, 10,  0, -10],
           [-10, 10, 10, 10, 10, 10, 10, -10],
           [-10,  5,  0,  0,  0,  0,  5, -10],
           [-20, -10, -10, -10, -10, -10, -10, -20]]

rooks = [[0, 0, 0, 0, 0, 0, 0, 0],
         [5, 10, 10, 10, 10, 10, 10,  5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [0,  0,  0,  5,  5,  0,  0,  0]]

queens = [[-20, -10, -10, -5, -5, -10, -10, -20],
          [-10,  0,  0,  0,  0,  0,  0, -10],
          [-10,  0,  5,  5,  5,  5,  0, -10],
          [-5,  0,  5,  5,  5,  5,  0, -5],
          [0,  0,  5,  5,  5,  5,  0, -5],
          [-10,  5,  5,  5,  5,  5,  0, -10],
          [-10,  0,  5,  0,  0,  0,  0, -10],
          [-20, -10, -10, -5, -5, -10, -10, -20]]

king_start = [[-30, -40, -40, -50, -50, -40, -40, -30],
              [-30, -40, -40, -50, -50, -40, -40, -30],
              [-30, -40, -40, -50, -50, -40, -40, -30],
              [-30, -40, -40, -50, -50, -40, -40, -30],
              [-20, -30, -30, -40, -40, -30, -30, -20],
              [-10, -20, -20, -20, -20, -20, -20, -10],
              [20, 20,  0,  0,  0,  0, 20, 20],
              [20, 30, 10,  0,  0, 10, 30, 20]]

# late condition Both sides have no queens or
# Every side which has a queen has additionally no other pieces or one minorpiece maximum
# ???

king_late = [[-50, -40, -30, -20, -20, -30, -40, -50],
             [-30, -20, -10,  0,  0, -10, -20, -30],
             [-30, -10, 20, 30, 30, 20, -10, -30],
             [-30, -10, 30, 40, 40, 30, -10, -30],
             [-30, -10, 30, 40, 40, 30, -10, -30],
             [-30, -10, 20, 30, 30, 20, -10, -30],
             [-30, -30,  0,  0,  0,  0, -30, -30],
             [-50, -30, -30, -30, -30, -30, -30, -50]]


class ChessAIStockfishEval():

    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            os.path.abspath("stockfish/stockfish.exe"))
        self.time = 0.01

    def reload(self):
        self.engine.quit()
        self.engine = chess.engine.SimpleEngine.popen_uci(
            os.path.abspath("stockfish/stockfish.exe"))

    def make_matrix(self, board):
        pgn = board.epd()
        foo = []
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append('.')
                else:
                    foo2.append(thing)
            foo.append(foo2)
        return foo


    async def score_piece(self, board, color):
        fen = board.epd().split(" ", 1)[0]

        pp = 0
        nn = 0
        bb = 0
        rr = 0
        qq = 0

        if color:
            for piece in fen:
                if piece == "P":
                    rr += 1
                elif piece == "N":
                    nn += 1
                elif piece == "B":
                    bb += 1
                elif piece == "R":
                    pp += 1
                elif piece == "Q":
                    qq += 1
            return pp * PP + rr * RR + nn * NN + bb * BB + qq * QQ + KK
        else:
            for piece in fen:
                if piece == "p":
                    rr += 1
                elif piece == "n":
                    nn += 1
                elif piece == "b":
                    bb += 1
                elif piece == "r":
                    pp += 1
                elif piece == "q":
                    qq += 1
            return -(pp * PP + rr * RR + nn * NN + bb * BB + qq * QQ + KK)


    async def score_position(self, board, color):
        matrix = self.make_matrix(board)
        score = 0
        if color:
            for i in range(8):
                for j in range(8):
                    if matrix[i][j] == "P":
                        score += pawn[i][j]
                    elif matrix[i][j] == "N":
                        score += knights[i][j]
                    elif matrix[i][j] == "B":
                        score += bishops[i][j]
                    elif matrix[i][j] == "R":
                        score += rooks[i][j]
                    elif matrix[i][j] == "Q":
                        score += queens[i][j]
                    elif matrix[i][j] == "K":
                        score += king_start[i][j]
            return score
        else:
            pawn.reverse()
            knights.reverse()
            bishops.reverse()
            rooks.reverse()
            queens.reverse()
            king_start.reverse()
            for i in range(8):
                for j in range(8):
                    if matrix[i][j] == "p":
                        score += pawn[i][j]
                    elif matrix[i][j] == "n":
                        score += knights[i][j]
                    elif matrix[i][j] == "b":
                        score += bishops[i][j]
                    elif matrix[i][j] == "r":
                        score += rooks[i][j]
                    elif matrix[i][j] == "q":
                        score += queens[i][j]
                    elif matrix[i][j] == "k":
                        score += king_start[i][j]
            pawn.reverse()
            knights.reverse()
            bishops.reverse()
            rooks.reverse()
            queens.reverse()
            king_start.reverse()
            return -score

    def get_score_custom(self, board, color):
        a = asyncio.run(self.score_piece(board, color))
        b = asyncio.run(self.score_position(board, color))
        return a + b

    def custom_evaluation(self, board, color):
        return self.get_score_custom(board, color)

    def custom_ultimate(self, board, depth, a, b, max_player, color):
        if depth == 0 or board.is_game_over():
            return None, self.custom_evaluation(board, color)

        legal_moves = list(board.legal_moves)
        best_move = legal_moves[0]
        print(depth * "\t", depth)
        if max_player:
            maxEval = float('-inf')
            for move in legal_moves:
                board.push(move)
                current = self.custom_ultimate(
                    board, depth - 1, a, b, False, not color)[1]
                board.pop()
                if current > maxEval:
                    maxEval = current
                    best_move = move
                a = max(a, current)
                if b <= a:
                    break
            return best_move, maxEval
        else:
            minEval = float('inf')
            for move in legal_moves:
                board.push(move)
                current = self.custom_ultimate(
                    board, depth - 1, a, b, True, not color)[1]
                board.pop()
                if current < minEval:
                    minEval = current
                    best_move = move
                b = min(b, current)
                if b <= a:
                    break
            return best_move, minEval

    def random_ultimate(self, board):
        legal_moves = list(board.legal_moves)
        return legal_moves[random.randint(0, len(legal_moves)) - 1], None

    def stockfish_evaluation(self, board, color, time_limit=0.01):
        result = self.engine.analyse(
            board, chess.engine.Limit(time=time_limit))
        if not color:
            return result['score'].black().score()
        else:
            return result['score'].white().score()

    def minimax(self, board, depth, a, b, max_player, color):
        if depth == 0 or board.is_game_over():
            return None, self.stockfish_evaluation(board, color, self.time)

        print("\t" * depth, depth)

        legal_moves = list(board.legal_moves)
        best_move = legal_moves[0]

        if max_player:
            maxEval = float('-inf')
            for move in legal_moves:
                board.push(move)
                current = self.minimax(
                    board, depth - 1, a, b, False, not color)[1]
                board.pop()
                try:
                    if current > maxEval:
                        maxEval = current
                        best_move = move
                    a = max(a, current)
                except TypeError:
                    self.reload()
                    #self.time = self.time + 0.02
                    try:
                        self.stockfish_evaluation(board, color, self.time*2.5)
                        if current > maxEval:
                            maxEval = current
                            best_move = move
                        a = max(a, current)
                    except TypeError:
                        print("Error")
                if b <= a:
                    break
            return best_move, maxEval
        else:
            minEval = float('inf')
            for move in legal_moves:
                board.push(move)
                current = self.minimax(
                    board, depth - 1, a, b, True, not color)[1]
                board.pop()
                try:
                    if current < minEval:
                        minEval = current
                        best_move = move
                    b = min(b, current)
                except TypeError:
                    self.reload()
                    #self.time = self.time + 0.02
                    try:
                        self.stockfish_evaluation(board, color, self.time*2.5)
                        if current < minEval:
                            minEval = current
                            best_move = move
                        b = min(b, current)
                    except TypeError:
                        print("Error")
                if b <= a:
                    break
            return best_move, minEval
