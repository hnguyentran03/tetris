from cmu_112_graphics import *
import random
import pieces
import board

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.cellMargin = app.cellSize/2
    app.pieces = [pieces.iPiece, pieces.jPiece, pieces.lPiece, pieces.zPiece, pieces.sPiece, pieces.oPiece, pieces.tPiece]
    restartGame()
    pass

def restartGame(app):
    app.board = board.Board(app.rows, app.cols)

    app.timerDelay = 50
    app.timePassed = 0
    app.defaultSpeed = 1000

    app.score = 0
    app.blockSpeed = app.defaultSpeed - 5*app.score

    app.isGameOver = False
    app.paused = True

    app.pieceBag = makeBag(app)
    app.fallingPiece = newFallingPiece(app)

def makeBag(app):
    return random.sample(app.pieces, k=len(app.pieces))

def newFallingPiece(app):
    if not app.pieceBag:
        app.pieceBag = makeBag(app)
    return app.pieceBag.pop(0)

def keyPressed(app, event):
    if key == 'r':
        restartGame(app)
    elif key == 'p':
        app.paused = not app.paused
   
    if app.isGameOver or app.paused:
        return
    
    key = event.key
    if key == 'Left':
        app.fallingPiece.move(app.board, 0, -1)
    elif key == 'Right':
        app.fallingPiece.move(app.board, 0, +1)
    elif key == 'Down':
        app.fallingPiece.move(app.board, +1, 0)
    elif key == 'Space':
        app.fallingPiece.hardDrop(app.board)
    
    

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, color='black')
    app.board.render(app, canvas)
    app.fallingPiece.render(app, canvas)

#Defines the board
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 40
    margin = 150
    return (rows, cols, cellSize, margin)

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    runApp(width=width, height=height)

playTetris()