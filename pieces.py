from helpers import drawCell, drawBoxCell, repr2dList


class Piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.L = []
        self.colors = []
        self.rotation = 0

    def __repr__(self):
        return repr((self.rotation, self.row, self.col))

    def getShape(self):
        return self.L

    def getCell(self, row, col):
        return self.L[row][col]

    def getRows(self):
        return len(self.L)

    def getCols(self):
        return len(self.L[0])

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getColor(self, colorIndex):
        return self.colors[colorIndex]

    def getRotation(self):
        return self.rotation

    def setPos(self, row, col):
        self.row = row
        self.col = col

    # Checks every relative position on the board for legality
    def isLegal(self, board):
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                if self.L[row][col]:
                    curRow = row + self.row
                    curCol = col + self.col
                    if not board.isLegalPos(curRow, curCol):
                        return False
        return True

    def move(self, board, drow, dcol):
        self.row += drow
        self.col += dcol

        if not self.isLegal(board):
            self.row -= drow
            self.col -= dcol
            return False
        return True

    def hardDrop(self, board):
        while self.isLegal(board):
            self.row += 1
        self.row -= 1
     
    # TODO: FIX ROTATION TO USE A BETTER SYSTEM
    # The columns of a rotated piece equal the rows and the columns equal to #rows - old col - 1
    def rotateCounterClockwise(self, board, legal=True):
        oldL = self.L
        oldRows, oldCols = self.getRows(), self.getCols()

        newRows, newCols = oldCols, oldRows
        newL = [[None]*newCols for _ in range(newRows)]

        for oldCol in range(oldCols):
            for oldRow in range(oldRows):
                newRow = newRows - oldCol - 1
                newCol = oldRow
                newL[newRow][newCol] = oldL[oldRow][oldCol]

        self.L = newL
        self.row += oldRows//2 - newRows//2
        self.col += oldCols//2 - newCols//2
        self.rotation = (self.rotation + 1) % 4

        if not self.isLegal(board) and legal:
            self.L = oldL
            self.row -= oldRows//2 - newRows//2
            self.col -= oldCols//2 - newCols//2
            self.rotation = (self.rotation - 1) % 4

    # The rows after rotation equal the columns and the columns equal #cols - old row - 1
    def rotateClockwise(self, board):
        oldL = self.L
        oldRows, oldCols = self.getRows(), self.getCols()

        newRows, newCols = oldCols, oldRows
        newL = [[None]*newCols for _ in range(newRows)]

        for oldCol in range(oldCols):
            for oldRow in range(oldRows):
                newRow = oldCol
                newCol = newCols - oldRow - 1
                newL[newRow][newCol] = oldL[oldRow][oldCol]

        self.L = newL
        self.row += oldRows//2 - newRows//2
        self.col += oldCols//2 - newCols//2
        self.rotation = (self.rotation - 1) % 4

        if not self.isLegal(board):
            self.L = oldL
            self.row -= oldRows//2 - newRows//2
            self.col -= oldCols//2 - newCols//2
            self.rotation = (self.rotation + 1) % 4

    def render(self, app, canvas, board):
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                if self.L[row][col]:
                    curRow = self.row + row
                    curCol = self.col + col
                    drawCell(app, canvas, board, curRow, curCol,
                             self.colors[app.colorIndex], app.widthColors[app.colorIndex])

    def renderBox(self, app, canvas, board):
        location = board.getLocation()
        rows, cols = len(self.L), len(self.L[0])
        for row in range(rows):
            for col in range(cols):
                pieceRow = board.getRows()//2 - rows//2 + row
                pieceCol = board.getCols()//2 - cols//2 + col
                if self.L[row][col]:
                    drawBoxCell(app, canvas, location, pieceRow, pieceCol,
                                self.colors[app.colorIndex])


class iPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[True,  True,  True,  True]]
        self.colors = ['red', 'cyan']


class jPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[True, False, False],
                  [True,  True,  True]]
        self.colors = ['yellow', 'blue']


class lPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[False, False,  True],
                  [True,  True,  True]]
        self.colors = ['magenta', 'orange']


class oPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[True,  True],
                  [True,  True]]
        self.colors = ['pink', 'yellow']


class sPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[False,  True,  True],
                  [True,  True, False]]
        self.colors = ['cyan', 'lime green']


class zPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[True,  True, False],
                  [False,  True,  True]]
        self.colors = ['green', 'red']


class tPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.L = [[False,  True, False],
                  [True,  True,  True]]

        self.colors = ['orange', 'purple1']


class Outline(Piece):
    def __init__(self, piece, board):
        self.piece = piece
        super().__init__(piece.getRow(), piece.getCol())
        self.L = piece.L
        self.update(board)

    def hardDrop(self, board):
        while self.isLegal(board):
            self.shownRow += 1
        self.shownRow -= 1

    def update(self, board):
        self.L = self.piece.getShape()
        self.shownRow = 0
        self.shownCol = self.piece.getCol()
        self.hardDrop(board)

    def isLegal(self, board):
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                if self.L[row][col]:
                    curRow = row + self.shownRow
                    curCol = col + self.shownCol
                    if not board.isLegalPos(curRow, curCol):
                        return False
        return True

    def render(self, app, canvas, board):
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                if self.L[row][col]:
                    curRow = self.shownRow + row
                    curCol = self.shownCol + col
                    drawCell(app, canvas, board, curRow, curCol,
                             '', 'white')
