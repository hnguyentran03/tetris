import copy
from helpers import reverseBoard

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

th = -0.510066
cl = 0.760666
h = -0.85663
b = -0.184483

def scoreBoard(board):
    clearedLines = countClearedLines(board) # maximize
    holes = countHoles(board) # minimize
    bumpiness = calculateBumpiness(board) # minimize
    #Aim for 4 high with a gap in one of them
    targetHeight = abs(totalHeight(board))  #minimize
    rightmost = rightMostCol(board) # minimize
    return cl * clearedLines + h * holes + b * bumpiness + th * targetHeight


def simulate(app, hold, col, rotation):
    board = copy.deepcopy(app.board)
    if hold and app.holdPiece and app.canHold:
        copy.deepcopy(app.holdPiece)
    elif hold and not app.holdPiece and not app.canHold:
        piece = copy.deepcopy(app.nextPiece)
    elif not hold: 
        piece = copy.deepcopy(app.fallingPiece)
    else:
        return float('-inf')

    piece.setPos(piece.getRow(), col)
    if not piece.isLegal(board):
        return float('-inf')
    for _ in range(rotation):
        piece.rotateCounterClockwise(board)
    
    piece.hardDrop(board)
    board.putPieceIn(app, piece)
    return scoreBoard(board)

def simulateAll(app):
    bestScore = None
    bestActions = (None, None, None)
    for hold in range(2):
        for col in range(app.board.getCols()):
            for rotation in range(4):
                    score = simulate(app, hold, col, rotation)
                    print(score, hold, col, rotation)
                    if bestScore is None or score > bestScore:
                        bestActions = (hold, col, rotation)
                        bestScore = score
    print('best: ', bestScore, bestActions)
    return bestActions



        


