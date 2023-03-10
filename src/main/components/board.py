from helpers import reverseBoard, drawCell, drawBoxCell, repr2dList


class Board:
    def __init__(self, rows, cols, emptyColor):
        self.emptyColor = emptyColor
        self.rows = rows
        self.cols = cols
        self.L = [[emptyColor] * self.cols for _ in range(self.rows)]

    def __repr__(self):
        return repr2dList(self.L)

    def getBoard(self):
        return self.L

    def getRows(self):
        return self.rows

    def getCols(self):
        return self.cols

    def getEmptyColor(self):
        return self.emptyColor

    def getCell(self, row, col):
        return self.L[row][col]

    def isLegalPos(self, row, col):
        return (0 <= row < self.getRows() and 0 <= col < self.getCols() and self.L[row][col] == self.emptyColor)

    # Checks each location on the board and makes the board the same color as the piece

    def putPieceIn(self, piece, color='white'):
        rows, cols = piece.getRows(), piece.getCols()

        for row in range(rows):
            for col in range(cols):
                if piece.getCell(row, col):
                    pieceRow = row + piece.getRow()
                    pieceCol = col + piece.getCol()
                    self.L[pieceRow][pieceCol] = color



    # Flips the board and only copies not full rows to a new list, then add new empty rows to the bottom then flip back
    def removeRows(self):
        newL = []
        for rows in reverseBoard(self.L):
            if self.emptyColor in rows:
                newL.append(rows)

        remRows = self.rows - len(newL)

        for _ in range(remRows):
            emptyRow = [self.emptyColor]*self.cols
            newL.append(emptyRow)

        self.L = reverseBoard(newL)
        return remRows

    def applyGameOver(self, color):
        self.L = list(map(lambda L: list(
            map(lambda c: color if c != self.emptyColor else c, L)), self.L))

    # NOT USED FOR NOW
    def applyColor(self, color):
        self.L = list(map(lambda L: list(
            map(lambda c: color if c == self.emptyColor else c, L)), self.L))
        self.emptyColor = color

    def render(self, app, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                drawCell(app, canvas, self, row, col,
                         self.L[row][col], app.widthColors[app.colorIndex])


class Box(Board):
    def __init__(self, row, col, emptyColor, location):
        super().__init__(row, col, emptyColor)
        self.location = location

    def getLocation(self):
        return self.location

    def render(self, app, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                drawBoxCell(app, canvas, self.location, row,
                            col, app.emptyColors[app.colorIndex])
