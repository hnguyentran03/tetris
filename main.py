from cmu_112_graphics import *
import random
from pieces import *
import board


def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.cellMargin = app.cellSize/24
    app.pieces = [iPiece, jPiece, lPiece,
                  zPiece, sPiece, oPiece, tPiece]

    app.colorIndex = 1
    app.textColors = ['blue', 'yellow']
    app.bannerTextColors = ['yellow', 'black']
    app.bannerColors = ['black', 'yellow']
    app.bgColors = ['orange', 'black']

    # Board Colors
    app.emptyColors = ['blue', 'black']
    app.widthColors = ['black', 'grey19']
    # {'single': 100, 'double': 300, 'triple': 500, 'tetris': 800}
    app.scores = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
    restartGame(app)


def nextBoard(app):
    nextWidth = app.width*9/10
    nextLocation = (nextWidth - app.cellSize/2,
                    app.margin + 4/3*app.cellSize)
    app.nextBoard = board.Box(
        4, 4, app.emptyColors[app.colorIndex], nextLocation)


def holdBoard(app):
    holdWidth = app.width*1/10
    holdLocation = (holdWidth - app.cellSize/2,
                    app.margin + 4/3*app.cellSize)
    app.holdBoard = board.Box(
        4, 4, app.emptyColors[app.colorIndex], holdLocation)


def restartGame(app):
    app.board = board.Board(
        app.rows, app.cols, app.emptyColors[app.colorIndex])

    nextBoard(app)
    holdBoard(app)

    app.timerDelay = 50
    app.timePassed = 0
    app.defaultSpeed = 1000

    app.score = 0
    app.blockSpeed = app.defaultSpeed - 5*app.score

    app.isGameOver = False
    app.paused = False

    app.pieceBag = makeBag(app)
    app.fallingPiece = newPiece(app)
    app.nextPiece = newPiece(app)
    app.holdPiece = None

    app.canHold = True
    app.switch = False


def makeBag(app):
    return random.sample(app.pieces, k=len(app.pieces))


def nextFallingPiece(app):
    app.fallingPiece = app.nextPiece
    app.nextPiece = newPiece(app)


def newPiece(app):
    if not app.pieceBag:
        app.pieceBag = makeBag(app)

    pieceType = app.pieceBag.pop(0)
    piece = pieceType(0, 0)
    # Centers new piece
    row = 0
    col = app.board.getCols()//2 - piece.getCols()//2
    piece.setPos(row, col)
    return piece


def holdFallingPiece(app):
    if app.canHold:
        app.canHold = False
        if not app.switch:
            app.switch = True
            app.holdPiece = app.fallingPiece
            nextFallingPiece(app)
        else:
            tempPiece = app.fallingPiece
            app.fallingPiece = app.holdPiece
            app.holdPiece = tempPiece


def keyPressed(app, event):
    key = event.key
    # Misc
    if key == 'r':
        restartGame(app)
    elif key == 'p':
        app.paused = not app.paused

    # Color
    if key == '0':
        app.colorIndex = (app.colorIndex + 1) % len(app.emptyColors)
        restartGame(app)

    if app.isGameOver or app.paused:
        return

    # Movement
    if key == 'Left':
        app.fallingPiece.move(app.board, 0, -1)
    elif key == 'Right':
        app.fallingPiece.move(app.board, 0, +1)
    elif key == 'Down':
        app.fallingPiece.move(app.board, +1, 0)
    elif key == 'Space':
        app.fallingPiece.hardDrop(app.board)
        placeFallingPiece(app)

    # Rotation
    if key in ['z', 'Up']:
        app.fallingPiece.rotateCounterClockwise(app.board)
    elif key == 'x':
        app.fallingPiece.rotateClockwise(app.board)

    # Hold
    if key == 'c':
        holdFallingPiece(app)


def placeFallingPiece(app):
    app.canHold = True
    app.board.putPieceIn(app, app.fallingPiece)
    linesCleared = app.board.removeRows()
    app.score += app.scores[linesCleared]

    nextFallingPiece(app)
    if not app.fallingPiece.isLegal(app.board):
        app.isGameOver = True
        app.board.applyGameOver('grey')


def timerFired(app):
    if app.isGameOver or app.paused:
        return
    app.timePassed += app.timerDelay
    if app.timePassed > app.blockSpeed:
        if not app.fallingPiece.move(app.board, +1, 0):
            placeFallingPiece(app)
        app.timePassed = 0


def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill=app.bgColors[app.colorIndex])


def drawScore(app, canvas):
    canvas.create_text(app.width/2, app.margin - app.cellSize/2,
                       text=f"Score: {app.score}",
                       fill=app.textColors[app.colorIndex],
                       font=f"Helvetica {int(app.cellSize/2)} bold")


def drawText(app, canvas, text):
    canvas.create_rectangle(0,
                            app.margin - app.cellMargin,
                            app.width,
                            app.margin + app.cellSize*3 + app.cellMargin,
                            fill=app.bannerColors[app.colorIndex], outline="")
    canvas.create_text(app.width/2, app.margin + 1.5*app.cellSize,
                       text=text,
                       fill=app.bannerTextColors[app.colorIndex], font=f"Helvetica {app.cellSize} bold")


def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawScore(app, canvas)

    app.board.render(app, canvas)
    app.fallingPiece.render(app, canvas, app.board)

    app.nextBoard.render(app, canvas)
    app.nextPiece.renderBox(app, canvas, app.nextBoard)

    app.holdBoard.render(app, canvas)
    if app.holdPiece:
        app.holdPiece.renderBox(app, canvas, app.holdBoard)

    if app.isGameOver:
        drawText(app, canvas, 'Game Over')

    if app.paused:
        drawText(app, canvas, 'Paused')

# Defines the board


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
