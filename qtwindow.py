import sys
import re

import chess

import play

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMessageBox



class MainWindow(QWidget):
    """
    Create a surface for the chessboard.
    """
    def __init__(self):
        """
        Initialize the chessboard.
        """
        super().__init__()

        self.setWindowTitle("Super Chess AI: Your turn")
        self.setGeometry(100, 100, 600, 600) #300, 300, 800, 800

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(0, 0, 600, 600)

        self.boardSize = min(self.widgetSvg.width(),
                             self.widgetSvg.height())
        self.coordinates = True
        self.margin = 0.05 * self.boardSize if self.coordinates else 0
        self.squareSize = (self.boardSize - 2 * self.margin) / 8.0
        self.pieceToMove = [None, None]

        self.board = chess.Board()
        self.drawBoard()
        self.custom = play.Player(4)

        self.turn = 0

    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        """
        Handle left mouse clicks and enable moving chess pieces by
        clicking on a chess piece and then the target square.

        Moves must be made according to the rules of chess because
        illegal moves are suppressed.
        """
        if event.x() <= self.boardSize and event.y() <= self.boardSize:
            if event.buttons() == Qt.LeftButton:
                if self.margin < event.x() < self.boardSize - self.margin and self.margin < event.y() < self.boardSize - self.margin:
                    file = int((event.x() - self.margin) / self.squareSize)
                    rank = 7 - int((event.y() - self.margin) / self.squareSize)
                    square = chess.square(file, rank)
                    piece = self.board.piece_at(square)
                    coordinates = "{}{}".format(chr(file + 97), str(rank + 1))
                    if self.pieceToMove[0] is not None:
                        try:
                            move = chess.Move.from_uci("{}{}".format(self.pieceToMove[1], coordinates))
                            if (re.match('\D8', coordinates)) and self.pieceToMove[0].piece_type == 1:
                                move = chess.Move.from_uci("{}{}{}".format(self.pieceToMove[1], coordinates, 'q'))
                                if move in self.board.legal_moves:
                                    self.board.push(move)
                                    self.turn = 1
                                else:
                                    move = chess.Move.drop
                        except ValueError:
                            move = chess.Move.drop
                        if move in self.board.legal_moves:
                            self.board.push(move)
                            self.turn = 1

                        self.setWindowTitle("Super Chess AI: AI turn")
                        piece = None
                        coordinates = None
                    self.pieceToMove = [piece, coordinates]
                    self.drawBoard()
        self.drawBoard()
        if self.turn == 1:
            self.turn = 0
            self.custom.ai_move("custom", self.board)
            self.setWindowTitle("Super Chess AI: Your turn")
            self.drawBoard()
        if (self.board.is_game_over()) or (self.board.is_checkmate()):
            self.showDialog()

    def showDialog():
        # хз, как сделать диалоговое окно
        # тут был код, но он не работал
        pass  

    def drawBoard(self):
        """
        Draw a chessboard with the starting position and then redraw
        it for every new move.
        """
        self.boardSvg = self.board._repr_svg_().encode("UTF-8")
        self.drawBoardSvg = self.widgetSvg.load(self.boardSvg)

        return self.drawBoardSvg


if __name__ == "__main__":
    chessGui = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(chessGui.exec_())