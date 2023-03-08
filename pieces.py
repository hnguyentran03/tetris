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
