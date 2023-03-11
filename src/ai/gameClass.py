import sys
sys.path.insert(
    1, '/Users/ADMIN/Desktop/School/CMU/Fun/tetris-redo/src/main/components')
sys.path.insert(1, '/Users/ADMIN/Desktop/School/CMU/Fun/tetris-redo/src/main')
from pieces import jPiece, lPiece, sPiece, zPiece, oPiece, iPiece
import copy
import random
from fitnessHelpers import countHoles, calculateBumpiness, totalHeight




# HELPERS


def simLegal(piece, board):
    for row in range(piece.getRows()):
        for col in range(piece.getCols()):
            if piece.getCell(row, col):
                pieceRow = row + piece.getRow()
                pieceCol = col + piece.getCol()
                if not (pieceRow < board.getRows() and pieceCol < board.getCols() and board.getCell(pieceRow, pieceCol) == board.getEmptyColor()):
                    return False
    return True


def simHardDrop(piece, board):
    while simLegal(piece, board):
        piece.setPos(piece.getRow()+1, piece.getCol())
    piece.setPos(piece.getRow()-1, piece.getCol())

# MAIN CLASS


class State:
    def __init__(self, board, agent, heuristic):
        self.board = board
        self.agent = agent
        self.heuristic = heuristic
        self.points = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
    
    def getBoard(self):
        return self.board

    def start(self):
        self.pieces = [jPiece, lPiece, sPiece, zPiece, oPiece, iPiece]
        self.bag = random.sample(self.pieces, k=len(self.pieces))
        self.ogBag = copy.deepcopy(self.bag)
        self.fallingPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        self.holdPiece = None
        self.canHold = True

        self.gameOver = False
        self.linesCleared = 0
        self.totalLines = 0
        self.score = 0

    def newPiece(self):
        if not self.bag:
            self.bag = random.sample(self.pieces, k=len(self.pieces))

        pieceType = self.bag.pop(0)
        piece = pieceType(0, 0)
        # Centers new piece
        row = 0
        col = self.board.getCols()//2 - piece.getCols()//2
        piece.setPos(row, col)
        return piece

    def fitness(self):
        l, h, b, ht = self.heuristic
        board = self.getBoard()
        clearedLines = self.linesCleared  # maximize
        holes = countHoles(board)  # minimize
        bumpiness = calculateBumpiness(board)  # minimize
        targetHeight = abs(totalHeight(board))  # minimize

        return l * clearedLines + h * holes + b * bumpiness + ht * targetHeight

    def getNext(self, action):
        hold, col, rotate = action['hold'], action['col'], action['rotate']
        if hold and not self.canHold:
            print('huh')
            return None

        newState = copy.deepcopy(self)
        board = newState.board
        # print(newState)

        if hold and self.holdPiece:
            piece = copy.deepcopy(self.holdPiece)

            # set up new state
            newState.holdPiece = copy.deepcopy(self.fallingPiece)
            newState.fallingPiece = copy.deepcopy(self.nextPiece)
        elif hold and not self.holdPiece:
            piece = copy.deepcopy(self.nextPiece)

            # set up new state
            newState.fallingPiece = copy.deepcopy(self.newPiece())
            newState.holdPiece = copy.deepcopy(self.fallingPiece)
        else:
            piece = copy.deepcopy(self.fallingPiece)

            # set up new state
            newState.fallingPiece = copy.deepcopy(self.nextPiece)

        for _ in range(rotate):
            piece.rotateCounterClockwise(self.board, False)
            piece.setPos(piece.getRow()+3, col)
        simHardDrop(piece, board)
        if not piece.isLegal(board):
            return None
        
        
        board.putPieceIn(piece, '⬜️')
        newState.linesCleared = board.removeRows()
        newState.totalLines += newState.linesCleared
        newState.nextPiece = copy.deepcopy(self.newPiece())

        newState.score += newState.points[newState.linesCleared]
        
        # Restore old
        self.bag = self.ogBag
        return newState

    def getBestAction(self):
        bestAction = None
        bestFit = None
        bestState = None
        for action in self.agent.getAllActions(self):
            newState = self.getNext(action)
            fit = newState.fitness() if newState else float('-inf')
            if not bestFit or fit > bestFit:
                bestFit = fit
                bestAction = action
                bestState = newState
        return bestAction, bestState

    def getBestNext(self):
        _, bestState = self.getBestAction()
        if not bestState:
            self.gameOver = True
        return bestState


    

    
        
