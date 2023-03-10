def countClearedLines(board):
    count = 0
    for line in board.getBoard():
        if board.getEmptyColor() not in line:
            count += 1
    return count


def countHoles(board):
    count = 0
    for col in range(board.getCols()):
        blocked = False
        for row in range(board.getRows()):
            if board.getCell(row, col) != board.getEmptyColor():
                blocked = True
            elif board.getCell(row, col) == board.getEmptyColor() and blocked:
                count += 1
    return count


def colHeight(board, col):
    for row in range(board.getRows()):
        if board.getCell(row, col) != board.getEmptyColor():
            return board.getRows() - row
    return 0


def calculateBumpiness(board):
    res = 0
    for col in range(board.getCols() - 1):
        res += abs(colHeight(board, col) - colHeight(board, col+1))
    return res


def totalHeight(board):
    res = 0
    for col in range(board.getCols()):
        res += colHeight(board, col)
    return res


def rightMostCol(board):
    count = 0
    for row in range(board.getRows()):
        if board.getCell(row, board.getCols()-1) != board.getEmptyColor():
            count += 1
    return count
