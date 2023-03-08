from helpers import getCellBounds

class Piece:
    def __init__(self, row, col, margin):
        self.row = row
        self.col = col
        self.L = []
        self.colors = []
        self.widthColor = ['black', 'grey19']
        self.margin = margin
    
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

    # Checks every relative position on the board for legality
    def isLegal(self, board):
        for row in range(self.L):
            for col in range(self.L[row]):
                curRow = row + self.row
                curCol = col + self.col
                if not (0 <= curRow < board.getRows() and 0 <= curCol < board.getCols() and board.isLegalPos(curRow, curCol)):
                    return False
        return True

    def moveFallingPiece(self, board, drow, dcol):
        self.row += drow
        self.col += dcol

        while self.isLegal(board):
            self.row -= drow
            self.col -= dcol
    
    # The columns of a rotated piece equal the rows and the columns equal to #rows - old col - 1
    def rotateCounterClockwise(self, board):
        oldL = self.L
        oldRows, oldCols = len(oldL), len(oldL[0])

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

        if not self.isLegal(board):
            self.L = oldL
            self.row -= oldRows//2 - newRows//2
            self.col -= oldCols//2 - newCols//2
    
    # The rows after rotation equal the columns and the columns equal #cols - old row - 1
    def rotateClockwise(self, board):
        oldL = self.L
        oldRows, oldCols = len(oldL), len(oldL[0])

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

        if not self.isLegal(board):
            self.L = oldL
            self.row -= oldRows//2 - newRows//2
            self.col -= oldCols//2 - newCols//2

    def render(self, app, canvas, board):
        for row in range(self.L):
            for col in range(self.L[row]):
                x0, x1, y0, y1 = getCellBounds(app,board, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, color=self.colors[app.colorIndex], outline=self.widthColor[app.colorIndex], width=self.margin)
    
class iPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[  True,  True,  True,  True ]]
        self.colors = ['red', 'cyan']

class jPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[  True, False, False ],
                  [  True,  True,  True ]]
        self.colors = ['yellow', 'blue']

class lPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[ False, False,  True ],
                  [  True,  True,  True ]]
        self.colors = ['magenta', 'orange']

class oPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[  True,  True ],
                  [  True,  True ]]
        self.colors = ['pink', 'yellow']

class sPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[ False,  True,  True ],
                  [  True,  True, False ]]
        self.colors = ['cyan', 'lime green']

class sPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[  True,  True, False ],
                  [ False,  True,  True ]]
        self.colors = ['green', 'purple1']

class tPiece(Piece):
    def __init__(self, row, col, margin):
        super.__init__(row, col, margin)
        self.L = [[ False,  True, False ],
                    [  True,  True,  True ]]

        self.colors = ['orange', 'red']