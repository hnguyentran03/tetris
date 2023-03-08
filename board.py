from helpers import reverseBoard, drawCell


class Board:
    def __init__(self, rows, cols, emptyColor):
        self.emptyColor = emptyColor
        self.rows = rows
        self.cols = cols
        self.L = [[emptyColor] * self.cols for _ in range(self.rows)]

    def getBoard(self):
        return self.L

    def getRows(self):
        return self.rows

    def getCols(self):
        return self.cols

    # Checks each location on the board and makes the board the same color as the piece
    def putPieceInBoard(self, app, piece):
        rows, cols = piece.getRows(), piece.getCols()

        for row in range(rows):
            for col in range(cols):
                if piece.getCell(row, col):
                    pieceRow = row + piece.getRow()
                    pieceCol = col + piece.getCol()
                    self.L[pieceRow][pieceCol] = piece.getColor(app.colorIndex)

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

    def render(self, app, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                drawCell(app, canvas, self, row, col,
                         self.L[row][col], self.widthColor)
