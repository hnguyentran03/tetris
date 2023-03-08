class Piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.L = []

    def isLegal(self, board):
        for row, _ in enumerate(self.L):
            for col, _ in enumerate(self.L[row]):
                curRow = row + self.row
                curCol = col + self.col
                if not (0 <= curRow < len(board) and 0 <= curCol < len(board[curRow]) and board[curRow][curCol]):
                    return False
        return True

    def moveFallingPiece(self, board, drow, dcol):
        self.row += drow
        self.col += dcol

        while self.isLegal(board):
            self.row -= drow
            self.col -= dcol
    
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
    
class iPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[  True,  True,  True,  True ]]
        self.colors = ['red', 'cyan']

class jPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[  True, False, False ],
                  [  True,  True,  True ]]
        self.colors = ['yellow', 'blue']

class lPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[ False, False,  True ],
                  [  True,  True,  True ]]
        self.colors = ['magenta', 'orange']

class oPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[  True,  True ],
                  [  True,  True ]]
        self.colors = ['pink', 'yellow']

class sPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[ False,  True,  True ],
                  [  True,  True, False ]]
        self.colors = ['cyan', 'lime green']

class sPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[  True,  True, False ],
                  [ False,  True,  True ]]
        self.colors = ['green', 'purple1']

class tPiece(Piece):
    def __init__(self, row, col):
        super.__init__(row, col)
        self.L = [[ False,  True, False ],
                    [  True,  True,  True ]]

        self.colors = ['orange', 'red']