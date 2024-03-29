import copy

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

# Scores the board based on the cleared lines, holes, bumpiness and total height

def scoreBoard(board):
    clearedLines = countClearedLines(board)  # maximize
    holes = countHoles(board)  # minimize
    bumpiness = calculateBumpiness(board)  # minimize
    targetHeight = abs(totalHeight(board))  # minimize
    # rightmost = rightMostCol(board)  # minimize

  
    th = -1.197002092407255 # -0.510066
    cl = 0.24078582866653464 # 0.760666
    h = -0.060680086302088654 # -0.35663
    b = -0.07049593906555696 # -0.184483
    cost = cl * clearedLines + h * holes + b * bumpiness + th * targetHeight
    return cost

# Made separate checks to allow for the AI to simulate easier
def simLegal(piece, board):
    for row in range(piece.getRows()):
        for col in range(piece.getCols()):
            if piece.getCell(row, col):
                pieceRow = row + piece.getRow()
                pieceCol = col + piece.getCol()
                if not (pieceRow < board.getRows() and pieceCol < board.getCols() and board.getCell(pieceRow, pieceCol) == board.getEmptyColor()):
                    return False
    return True

# Made a separate hard drop to bypass legality checks easier
def simHardDrop(piece, board):
    while simLegal(piece, board):
        piece.setPos(piece.getRow()+1, piece.getCol())
    piece.setPos(piece.getRow()-1, piece.getCol())

# Tries the move and scores it based on a heuristiic


def simulate(app, hold, col, rotation):
    board = copy.deepcopy(app.board)
    if hold and not app.canHold:
        return float('-inf'), []

    if hold and app.holdPiece:
        piece = copy.deepcopy(app.holdPiece)
    elif hold and not app.holdPiece:
        piece = copy.deepcopy(app.nextPiece)
    else:
        piece = copy.deepcopy(app.fallingPiece)

    for _ in range(rotation):
        piece.rotateCounterClockwise(board, False)
    piece.setPos(piece.getRow()+3, col)
    simHardDrop(piece, board)
    if not piece.isLegal(board):
        return float('-inf'), []

    board.putPieceIn(piece)
    return (scoreBoard(board), board)

# Simulates all columns and rotations


def simulateAll(app):
    scores = dict()
    for hold in range(2):
        for col in range(app.board.getCols()):
            for rotation in range(4):
                res = simulate(app, hold, col, rotation)
                scores[(hold, col, rotation)] = res

    best = max(scores, key=lambda k: scores.get(k)[0])
    # print(f'best: {best}')
    # app.aiTest = scores
    return best
