from helpers import getCellBounds

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

    
