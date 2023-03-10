from src.main.components.pieces import jPiece, lPiece, sPiece, zPiece, oPiece, iPiece
from fitnessHelpers import countClearedLines, countHoles, calculateBumpiness, totalHeight
import random, copy

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
        self.lines, self.holes, self.bump, self.height = heuristic
       
    def start(self):
        self.pieces = [jPiece, lPiece, sPiece, zPiece, oPiece, iPiece]
        self.bag = []
        self.fallingPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        self.holdPiece = None
        self.canHold = True

        self.gameOver = False

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
    
    def fitness(self, state):
        if not state:
            return float('-inf')
        
        board = state.getBoard()
        clearedLines = countClearedLines(board)  # maximize
        holes = countHoles(board)  # minimize
        bumpiness = calculateBumpiness(board)  # minimize
        targetHeight = abs(totalHeight(board))  # minimize

        return self.lines * clearedLines + self.holes * holes + self.bump * bumpiness + self.height * targetHeight

    def getNext(self, action):
        hold, col, rotate = action['hold'], action['col'], action['rotate']
        if hold and not self.canHold:
            return None
        
        board = copy.deepcopy(self.board)
        newState = State(board, self.agent)

        if hold and self.holdPiece:
            piece = copy.deepcopy(self.holdPiece)
            newState.holdPiece = copy.deepcopy(self.fallingPiece)
        elif hold and not self.holdPiece:
            piece = copy.deepcopy(self.nextPiece)
            newState.holdPiece = copy.deepcopy(self.fallingPiece)
            newState.nextPiece = copy.deepcopy(self.newPiece())
        else:
            piece = copy.deepcopy(self.fallingPiece)
            newState.nextPiece = copy.deepcopy(self.newPiece())
        
        for _ in range(rotate):
            piece.rotateCounterClockwise(self.board, False)
            piece.setPos(piece.getRow()+3, col)
        simHardDrop(piece, board)
        if not piece.isLegal(board):
            return None
        
        board.putPieceIn(piece)
        return newState

    def getBestAction(self):
        bestAction = None
        bestFit = None
        bestState = None
        for action in self.agent.getAllActions(self):
            newState = self.getNext(action)
            fit = self.fitness(newState)
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
        
        
