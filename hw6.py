#################################################
# hw6.py
#
# Your name: Ben Nguyen Tran   
# Your andrew id: hnguyent
#
# Your partner's name: Fa Phanachet
# Your partner's andrew id: pphanach
#################################################

import cs112_f21_week6_linter 
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

#Modified from hw5 by me
#Checks if a number is a perfect square
def isPerfectSquare(n):
    n = (n)**(1/2)
    return n % (n//1) == 0

#Checks if the number is sort of squarish
def isSortOfSquarish(n):

    sortN = list(str(n))
    sortN = sorted(sortN)
    
    if '0' in sortN:
        return False

    sortN = int(''.join(sortN))

    if n <= 0 or not(isPerfectSquare(sortN)) or isPerfectSquare(n):
        return False
    return True

def nthSortOfSquarish(n):
    count = 0
    guess = 0
    while count <= n:
        guess += 1
        if isSortOfSquarish(guess):
            count += 1
    return guess


#################################################
# s21-midterm1-animation
#################################################

#Finds the nearest circle of any given cirlce
def nearestCircle(app, cx, cy):
    nearest = math.sqrt((app.width)**2 + (app.height)**2)
    closestCircle = (app.width, app.height)
    
    for (newCX, newCY) in app.circleCenters:
        if (cx, cy) != (newCX, newCY):
            distance = math.sqrt((cx - newCX)**2 + (cy - newCY)**2)
            
            if distance < nearest:
                closestCircle = (newCX, newCY)
                nearest = distance
    
    return closestCircle

#Start of the app
def s21MidtermAnimation_appStarted(app):
    app.circleCenters = []
    app.r = 20
    app.timePassed = 0

#Deletes all the circles when r is pressted
def s21MidtermAnimation_keyPressed(app, event):
    if event.key == 'r':
        app.circleCenters = []

#Creates a new circle when pressed
def s21MidtermAnimation_mousePressed(app, event):
    newCircleCenter = (event.x, event.y)
    app.circleCenters.append(newCircleCenter)

#Deletes circles after 10 seconds
def s21MidtermAnimation_timerFired(app):
    if app.circleCenters != []:
        app.timePassed += app.timerDelay
    
    if app.timePassed > 5000:
        if len(app.circleCenters) >= 1:
            app.circleCenters = []
        app.timePassed = 0

#Draws the appropriate circles and lines
def s21MidtermAnimation_redrawAll(app, canvas):
    if len(app.circleCenters) > 0:
        for (cx, cy) in app.circleCenters:
            
            canvas.create_oval(cx-app.r, cy-app.r, 
                                cx+app.r, cy+app.r, fill='green')
        
        for (cx, cy) in app.circleCenters:
            if len(app.circleCenters) > 1:
                (newCX, newCY) = nearestCircle(app, cx, cy)
                canvas.create_line(cx, cy, newCX, newCY)

#Runs
def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_')

#################################################
# Tetris
#################################################

#Defines all the pieces shapes
def gamePieces():
    iPiece = [[  True,  True,  True,  True ]]

    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]

    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]

    oPiece = [[  True,  True ],
              [  True,  True ]]

    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]

    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]

    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]
            
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", 
                        "pink", "cyan", "green", "orange" ]
    tetrisPieceNames = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    
    return (tetrisPieces, tetrisPieceColors, tetrisPieceNames)

#Defines the board
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 40
    margin = 150
    return (rows, cols, cellSize, margin)

#Default Settings when the app starts
def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.bonus = False
    
    restartGame(app)

#Reset Game
def restartGame(app):
    
    if app.bonus:
        app.paused = True
        app.emptyColor = 'black'
        app.widthColor = 'grey19'
        app.cellMargin = 2
        app.tetrisPieceColors = ['cyan', 'blue', 'orange', 'yellow',
                                'lime green', 'purple1', 'red']
        app.textColor = 'yellow'
        app.bannerColor = app.textColor
        app.bannerText = 'black'
        app.background = 'black'
        app.outlineColor = 'white'
        app.paused = False
    else:
        app.textColor = 'blue'
        app.bannerColor = 'black'
        app.bannerText = 'yellow'
        app.background = 'orange'
        app.cellMargin = app.cellSize/6
        app.emptyColor = 'blue'
        app.widthColor = 'black'
        app.outlineColor = 'white'
        (app.tetrisPieces, app.tetrisPieceColors, 
                                app.tetrisPieceNames) = gamePieces()

    app.board = [ ([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.holdBoard = [ ([app.emptyColor] * 4) for row in range(4)]
    app.nextBoard = [ ([app.emptyColor] * 4) for row in range(4)]
    app.timerDelay = 50
    app.defaultSpeed = 1000
    app.score = 0
    app.blockSpeed = app.defaultSpeed - 5*app.score
    app.isGameOver = False
    app.paused = False

    #Bonus
    app.nextPiece = None
    app.nextColor = None
    app.nextName = ''

    app.switch = False
    app.holdColor = None
    app.holdName = ''
    app.canHold = True

    app.pieceBag = []
    app.colorBag = []
    app.nameBag = []

    newFallingPiece(app)

    app.timePassed = 0
    app.bonusTimePassed = 0
    app.textTime = False

    app.bonusText = '''Bonus:
            The first two bonuses are a preview of the next piece coming
            which is indicated in the top right with the name of the
            piece and a box. 
            
            The top left has text and box that indicates which block
            you are holding. The button to hold a block is c. If you 
            hold once, you can't hold again until you place a block.

            The next bonus is a clockwise rotation. x and z are clockwise and
            counterclockwise rotations respectively. a also does a full 180
            rotation (but that's not really hard....)

            There is also a bonus where the speed increases proportional
            to the amount of lines you've cleared.
            
            Next, there is also a bonus that creates an outline of where your
            block is going to be placed.

            I changed the appearances of the blocks and board to make it look
            nicer.

            The final bonus is fixing the randomizer of the blocks. The blocks
            are randomized by a randomly permutated group of 7 different blocks.
            Then after the 7 blocks are used up, another random group of 7
            are created.
            
            Note:
            I added a paused button p to pause the game. Also for fun, game 
            over causes the blocks to turn grey.'''
 

#Gives the remaining row of the piece closest to the ground
def closestPiece(app):
    tetrisPiece = app.randomPiece
    rows, cols = len(tetrisPiece), len(tetrisPiece[0])
    
    best = app.rows
    bestDiff = app.rows

    for row in range(rows):
        for col in range(cols):
            if tetrisPiece[row][col]:
                pieceCol = app.fallingPieceCol + col
                pieceRow = app.fallingPieceRow + row
                
                #Checks for which block is closest to the ground
                for boardRow in range(pieceRow, app.rows):
                    if (app.board[boardRow][pieceCol] != app.emptyColor):
                        topRow = boardRow
                        difference = topRow - pieceRow - 1
                        if (bestDiff > difference and difference > 0):
                                best = boardRow
                                bestDiff = difference

    return best

#Makes the board grey when game over
def gameOver(app):
    putPieceInBoard(app)
    
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] != app.emptyColor:
                app.board[row][col] = 'grey'

#Gets the bounds of the cells
def getCellBounds(app, row, col, board):
    if board == app.board:
        
        #Taken from 112 Notes/Lecture
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        cellWidth = gridWidth / app.cols
        cellHeight = gridHeight / app.rows
        x0 = app.margin + col * cellWidth
        x1 = app.margin + (col+1) * cellWidth
        y0 = app.margin + row * cellHeight
        y1 = app.margin + (row+1) * cellHeight
    
    return x0, x1, y0, y1

#Takes care of the movement controls
def keyPressed(app, event):
    if not(app.isGameOver):
        if not(app.paused):
            if event.key == 'Up':
                rotateCounterClockwiseFallingPiece(app)
            elif event.key == 'Right':
                moveFallingPiece(app, 0, +1)
            elif event.key == 'Left':
                moveFallingPiece(app, 0, -1)
            elif event.key == 'Down':
                moveFallingPiece(app, +1, 0)
            elif event.key == 'Space':
                rowsToBottom = closestPiece(app)
                for i in range(rowsToBottom):
                    moveFallingPiece(app, +1, 0)
                
                placeFallingPiece(app)

            elif event.key == 'b':
                app.bonus = not(app.bonus)
                restartGame(app)
                if app.bonus:
                    print(app.bonusText)

            if app.bonus:
                if event.key == 'x':
                    rotateClockwiseFallingPiece(app)
                elif event.key == 'z':
                    rotateCounterClockwiseFallingPiece(app)
                elif event.key == 'a':
                    rotateCounterClockwiseFallingPiece(app)
                    rotateCounterClockwiseFallingPiece(app)
                
                elif event.key == 'c':
                    holdFallingPiece(app)
                
        if event.key == 'p' and app.bonus:
            app.paused = not(app.paused)
    
    if event.key == 'r':
        restartGame(app)

#Places a block
def timerFired(app):
    if not(app.isGameOver or app.paused):
        app.timePassed += app.timerDelay
        if app.timePassed > app.blockSpeed:
            if not(moveFallingPiece(app, +1, 0)):
                placeFallingPiece(app)
            app.timePassed = 0
    
    if app.bonus:
        app.bonusTimePassed += app.timerDelay
        app.textTime = True
        if app.bonusTimePassed > 1000:
            app.textTime = False

#Makes a random bag of 7 different pieces
def makeBag(app):
    tetrisPieces, tetrisPieceColors, tetrisPieceNames = (app.tetrisPieces,
                                                        app.tetrisPieceColors,
                                                        app.tetrisPieceNames)
    piece, color, name = (copy.deepcopy(tetrisPieces),
                          copy.deepcopy(tetrisPieceColors),
                          copy.deepcopy(tetrisPieceNames))  
    i = 0
    newPieceBag, newColorBag, newNameBag = [], [], []
    
    #Randomizes the bag
    while i < len(tetrisPieces):
        num = random.randint(0, len(piece)-1)
        newPiece, newColor, newName = (piece.pop(num), color.pop(num), 
                                      name.pop(num))
        newPieceBag.append(newPiece)
        newColorBag.append(newColor)
        newNameBag.append(newName)
        i += 1
    
    app.pieceBag, app.colorBag, app.nameBag = (newPieceBag, newColorBag,
                                               newNameBag)

#Makes a random piece
def nextFallingPiece(app):
    if app.bonus:
        if app.pieceBag == []:
            makeBag(app)
        nextPiece, nextPieceColor, nextPieceName = (app.pieceBag.pop(), 
                                                    app.colorBag.pop(), 
                                                    app.nameBag.pop())
    else:
        randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
        (nextPiece, nextPieceColor, 
                        nextPieceName) = (app.tetrisPieces[randomIndex], 
                                          app.tetrisPieceColors[randomIndex],
                                          app.tetrisPieceNames[randomIndex])
    return (nextPiece, nextPieceColor, nextPieceName)

#Makes a new piece from the top
def newFallingPiece(app):
    if app.bonus:
        if app.switch:
            colorIndex = app.tetrisPieceColors.index(app.holdColor)
            app.randomPiece = app.tetrisPieces[colorIndex]
            
            tempColor = app.randomPieceColor
            app.randomPieceColor = app.holdColor
            app.holdColor = tempColor
            
            app.switch = False
        
        else:
            if app.nextColor == None:
                app.randomPiece, app.randomPieceColor, blank = (
                                                        nextFallingPiece(app))
            
            else:
                app.randomPiece, app.randomPieceColor = (app.nextPiece, 
                                                        app.nextColor)

            #Prepares Next Piece
            app.nextPiece, app.nextColor, app.nextName = nextFallingPiece(app)

    else:
        app.randomPiece, app.randomPieceColor, blank = nextFallingPiece(app)

    app.fallingPieceCol = app.cols//2 - len(app.randomPiece[0])//2
    app.fallingPieceRow = 0

    newOutline(app)


#Moves a piece left or right
def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
        
    if not(fallingPieceIsLegal(app)):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    
    newOutline(app)
    
    return True

#Checks if the move is legal
def fallingPieceIsLegal(app):
    tetrisPiece = app.randomPiece

    numRows, cols = len(tetrisPiece), len(tetrisPiece[0])
    
    for row in range(numRows):
        for col in range(cols):
            if app.randomPiece[row][col]:
                pieceRow = app.fallingPieceRow + row
                pieceCol = app.fallingPieceCol + col
                
                outOfBounds = ((pieceRow < 0) or 
                            (pieceRow >= app.rows) or 
                            (pieceCol < 0) or 
                            (pieceCol >= app.cols))
                
                if (outOfBounds or 
                    app.board[pieceRow][pieceCol] != app.emptyColor):
                    return False
    return True

#Rotates any piece counterclockwise
def rotateCounterClockwiseFallingPiece(app):
    oldPiece = app.randomPiece
    oldNumRows, oldCols = len(oldPiece), len(oldPiece[0])
    
    newNumRows, newCols = oldCols, oldNumRows
    newPiece = [([None]*newCols) for row in range(newNumRows)]

    for oldCol in range(oldCols):   
        for oldRow in range(oldNumRows):
            newRow = newNumRows - oldCol - 1
            newCol = oldRow
            newPiece[newRow][newCol] = oldPiece[oldRow][oldCol]

    #Centers Piece
    app.randomPiece = newPiece
    app.fallingPieceRow += oldNumRows//2 - newNumRows//2
    app.fallingPieceCol += oldCols//2 - newCols//2

    if not(fallingPieceIsLegal(app)):
        app.randomPiece = oldPiece
        app.fallingPieceRow -= oldNumRows//2 - newNumRows//2 
        app.fallingPieceCol -= oldCols//2 - newCols//2 
    
    newOutline(app)

#Rotates any piece clockwise
def rotateClockwiseFallingPiece(app):
    oldPiece = app.randomPiece
    oldNumRows, oldCols = len(oldPiece), len(oldPiece[0])
    
    newNumRows, newCols = oldCols, oldNumRows
    newPiece = [([None]*newCols) for row in range(newNumRows)]

    for oldCol in range(oldCols):   
        for oldRow in range(oldNumRows):
            newRow = oldCol
            newCol = newCols - oldRow - 1
            newPiece[newRow][newCol] = oldPiece[oldRow][oldCol]   
    
    #Centers Piece
    app.randomPiece = newPiece
    app.fallingPieceRow += oldNumRows//2 - newNumRows//2
    app.fallingPieceCol += oldCols//2 - oldCols//2

    if not(fallingPieceIsLegal(app)):
        app.randomPiece = oldPiece
        app.fallingPieceRow -= oldNumRows//2 - newNumRows//2
        app.fallingPieceCol -= oldCols//2 - oldCols//2
    
    newOutline(app)

#Puts the piece into the board
def putPieceInBoard(app):
    tetrisPiece = app.randomPiece

    numRows, cols = len(tetrisPiece), len(tetrisPiece[0])
    for row in range(numRows):
        for col in range(cols):
            if tetrisPiece[row][col]:
                pieceRow = row + app.fallingPieceRow
                pieceCol = col + app.fallingPieceCol

                app.board[pieceRow][pieceCol] = app.randomPieceColor

#Places the block to put another piece
def placeFallingPiece(app):
    putPieceInBoard(app)
    
    app.canHold = True
    removeFullRows(app)

    if app.bonus:
        if app.defaultSpeed - app.score * 10 > 100:
            app.blockSpeed = app.defaultSpeed - app.score * 10
        else:
            app.blockSpeed = 10
    
    newFallingPiece(app)

    if not(fallingPieceIsLegal(app)):
        app.isGameOver = True
        if app.bonus:
            gameOver(app)
    
    

#Holds the falling pieces
def holdFallingPiece(app):
    if app.canHold:
        app.canHold = False
        if app.holdColor == None:
            app.holdColor = app.randomPieceColor
            
        else:
            app.switch = True
        
        colorIndex = app.tetrisPieceColors.index(app.randomPieceColor)
        app.holdName = app.tetrisPieceNames[colorIndex]
        newFallingPiece(app)

#Reverses the board
def reverseBoard(board):
    return board[::-1]

#Removes any full rows to clear lines
def removeFullRows(app):
    newBoard = []
    
    for rows in reverseBoard(app.board):
        if app.emptyColor in rows:
            newBoard.append(rows)
    
    remainingRows = app.rows - len(newBoard)
    app.score += remainingRows**2
    
    for i in range(remainingRows):
        emptyRow = [app.emptyColor]*app.cols
        newBoard.append(emptyRow)
    
    app.board = reverseBoard(newBoard)

#Makes a new outline each time there's a rotation or move
def newOutline(app):
    app.outline = copy.deepcopy(app.randomPiece)
    app.fallingOutlineCol = app.fallingPieceCol
    app.fallingOutlineRow = app.fallingPieceRow
    for i in range(closestPiece(app)):
        app.fallingOutlineRow += 1
        if not(fallingOutlineIsLegal(app)):
            app.fallingOutlineRow -= 1

#Makes sure the outline doesn't overlap    
def fallingOutlineIsLegal(app):
    tetrisOutline = app.outline

    numRows, cols = len(tetrisOutline), len(tetrisOutline[0])
    
    for row in range(numRows):
        for col in range(cols):
            if tetrisOutline[row][col]:
                pieceRow = app.fallingOutlineRow + row
                pieceCol = app.fallingOutlineCol + col
                
                outOfBounds = ((pieceRow < 0) or 
                            (pieceRow >= app.rows) or 
                            (pieceCol < 0) or 
                            (pieceCol >= app.cols))
                
                if (outOfBounds or 
                    app.board[pieceRow][pieceCol] != app.emptyColor):
                    return False
    return True

#Makes the graphic of the piece that's falling
def drawFallingPiece(app, canvas):
    tetrisPiece = app.randomPiece
    numRows, cols = len(tetrisPiece), len(tetrisPiece[0])
    for row in range(numRows):
        for col in range(cols):
            
            if tetrisPiece[row][col]:
                pieceCol = app.fallingPieceCol + col
                pieceRow = app.fallingPieceRow + row
                drawCell(app, canvas, pieceRow, pieceCol, 
                        app.randomPieceColor, app.widthColor, app.board)

#Draws a single cell box
def drawCell(app, canvas, row, col, color, outlineColor, board):
    x0, x1, y0, y1 = getCellBounds(app, row, col, board)
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = app.cellMargin, 
                            outline = outlineColor)

#Draws the board with all the current pieces and it's states
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col], app.widthColor,
                        app.board)

#Draws the boxes of the preview and hold
def drawBonusBoxes(app, canvas, width, name, boxType, location, board):
    canvas.create_text(width, app.margin+app.cellSize/2,
                        text = boxType+ f": {name}",
                        fill = app.textColor,
                        font = f"Helvetica {int(app.cellSize/2)} bold")
    drawBox(app, canvas, location, board, app.emptyColor)

#Draws the text to preview which block is next and held
def drawBonusHoldNext(app, canvas):
    #HOLD
    holdWidth = app.width*1/10
    holdLocation = (holdWidth - app.cellSize/2, 
                            app.margin + 4/3*app.cellSize)
    drawBonusBoxes(app, canvas, holdWidth, app.holdName, 'Hold', 
                    holdLocation, app.holdBoard)

    if app.holdColor != None:
        holdPiece = app.tetrisPieces[app.tetrisPieceColors.index(app.holdColor)]
        drawPreviewPiece(app, canvas, holdLocation, app.holdColor, holdPiece)
    
    #NEXT
    nextWidth = app.width*9/10
    nextLocation = (nextWidth - app.cellSize/2, 
                            app.margin + 4/3*app.cellSize)
    drawBonusBoxes(app, canvas, nextWidth, app.nextName, 'Next',
                 nextLocation, app.nextBoard)

    drawPreviewPiece(app, canvas, nextLocation, app.nextColor, app.nextPiece)

#Draws the bonus activated
def drawText(app, canvas, text):
    canvas.create_rectangle(0, 
                        app.margin + app.cellSize*app.rows, 
                            app.width, 
                            app.height, 
                            fill = app.bannerColor)
    canvas.create_text(app.width/2, app.margin + (app.rows+2)*app.cellSize, 
                    text=text,
                    fill= app.bannerText, font=f"Helvetica {app.cellSize} bold")

#Draws the outline that's been created
def drawOutline(app, canvas):
    tetrisPiece = app.outline
    numRows, numCols = len(tetrisPiece), len(tetrisPiece[0])

    for row in range(numRows):
        for col in range(numCols):
        
            if tetrisPiece[row][col]:
                pieceCol = app.fallingOutlineCol + col
                pieceRow = app.fallingOutlineRow + row
                drawCell(app, canvas, pieceRow, pieceCol, 
                    app.emptyColor, app.outlineColor, app.board)

#draws the preview box
def drawBox(app, canvas, location, board, color):
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
                drawBoxCell(app, canvas, location, row, col, color)

#Draws the cell in the preview box
def drawBoxCell(app, canvas, location, row, col, color):
    boxSize = app.cellSize/2
    boxMargin = app.cellMargin/2
    x, y = location
    canvas.create_rectangle(x+(col-1)*boxSize,y+(row-1)*boxSize, 
                                    x+col*boxSize, y+row*boxSize, 
                                 fill = color, 
                                 outline = app.widthColor,
                                 width = boxMargin)

#Draws the piece of in the preview boxes
def drawPreviewPiece(app, canvas, location, color, piece):
    tetrisPiece = piece
    numRows, numCols = len(tetrisPiece), len(tetrisPiece[0])
    for row in range(numRows):
        for col in range(numCols):
            pieceCol = len(app.holdBoard[0])//2 - numCols//2 + col
            pieceRow = len(app.holdBoard)//2 - numRows//2 + row
            if tetrisPiece[row][col]:
                drawBoxCell(app, canvas, location, pieceRow, pieceCol, 
                        color)

#Draws the board and piece
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.background)
    canvas.create_text(app.width/2, app.margin - app.cellSize/2, 
                            text = f"Score: {app.score}",
                            fill = app.textColor, 
                            font = f"Helvetica {int(app.cellSize/2)} bold")

    drawBoard(app, canvas)
    #if not(app.isGameOver): 
    if app.bonus:
        drawOutline(app, canvas)
    
    drawFallingPiece(app, canvas)

    if app.bonus:
        drawBonusHoldNext(app, canvas)

        if app.textTime:
            drawText(app,canvas, 'Bonus!')
   
    if app.paused:
        drawText(app,canvas, "Game Paused")
    
    if app.isGameOver:
        drawText(app, canvas, 'Game Over')
        drawBoard(app,canvas)

#Runs program
def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    runApp(width=width, height=height)

#################################################
# Test Functions
#################################################

def testIsPerfectSquare():
    print('Testing isPerfectSquare(n))...', end='')
    assert(isPerfectSquare(4) == True)
    assert(isPerfectSquare(9) == True)
    assert(isPerfectSquare(10) == False)
    assert(isPerfectSquare(225) == True)
    assert(isPerfectSquare(1225) == True)
    assert(isPerfectSquare(1226) == False)
    print('Passed')


def testIsSortOfSquarish():
    print('Testing isSortOfSquarish(n))...', end='')
    assert(isSortOfSquarish(52) == True)
    assert(isSortOfSquarish(16) == False)
    assert(isSortOfSquarish(502) == False)
    assert(isSortOfSquarish(414) == True)
    assert(isSortOfSquarish(5221) == True)
    assert(isSortOfSquarish(6221) == False)
    assert(isSortOfSquarish(-52) == False)
    print('Passed')


def testNthSortOfSquarish():
    print('Testing nthSortOfSquarish()...', end='')
    assert(nthSortOfSquarish(0) == 52)
    assert(nthSortOfSquarish(1) == 61)
    assert(nthSortOfSquarish(2) == 63)
    assert(nthSortOfSquarish(3) == 94)
    assert(nthSortOfSquarish(4) == 252)
    assert(nthSortOfSquarish(8) == 522)
    print('Passed')

def testAll():
    testIsPerfectSquare()
    testIsSortOfSquarish()
    testNthSortOfSquarish()

#################################################
# main
#################################################

def main():
    cs112_f21_week6_linter.lint()
    s21Midterm1Animation()
    playTetris()
    testAll()

if __name__ == '__main__':
    main()