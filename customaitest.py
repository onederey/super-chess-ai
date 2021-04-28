import chess
import asyncio

board0 = chess.Board()


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
        [5, -5,-10, 0, 0,-10, -5, 5],
        [5, 10, 10,-20,-20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]]

knights = [[-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]]

bishops = [[-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]]

rooks = [[0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]]

queens = [[-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]]

king_start = [[-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]]

# late condition Both sides have no queens or
# Every side which has a queen has additionally no other pieces or one minorpiece maximum
# ???

king_late = [[-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]]

def make_matrix(board):
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

async def score_piece(board, color):
    fen = board.epd().split(" ", 1)[0]

    pp = 0
    nn = 0
    bb = 0
    rr = 0
    qq = 0

    if color:
        for piece in fen:
            if piece == "R":
                rr+=1
            elif piece == "N":
                nn+=1
            elif piece == "B":
                bb+=1
            elif piece == "P":
                pp+=1
            elif piece == "Q":
                qq+=1
        return pp * PP + rr * RR + nn * NN + bb * BB + qq * QQ + KK
    else:
        for piece in fen:
            if piece == "r":
                rr+=1
            elif piece == "n":
                nn+=1
            elif piece == "b":
                bb+=1
            elif piece == "p":
                pp+=1
            elif piece == "q":
                qq+=1
        return -(pp * PP + rr * RR + nn * NN + bb * BB + qq * QQ + KK)

async def score_position(board, color):
    matrix = make_matrix(board)
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


        


if __name__ == "__main__":
    print(make_matrix(board0))
