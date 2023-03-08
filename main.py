from cmu_112_graphics import *
import random
from pieces import *
import board


def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.cellMargin = app.cellSize/24
    app.pieces = [iPiece, jPiece, lPiece,
                  zPiece, sPiece, oPiece, tPiece]

    app.colorIndex = 0
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


def restartGame(app):
    app.board = board.Board(
        app.rows, app.cols, app.emptyColors[app.colorIndex])

    app.timerDelay = 50
    app.timePassed = 0
    app.defaultSpeed = 1000

    app.score = 0
    app.blockSpeed = app.defaultSpeed - 5*app.score

    app.isGameOver = False
    app.paused = False

    app.pieceBag = makeBag(app)
    app.fallingPiece = newFallingPiece(app)


def makeBag(app):
    return random.sample(app.pieces, k=len(app.pieces))


def newFallingPiece(app):
    if not app.pieceBag:
        app.pieceBag = makeBag(app)

    pieceType = app.pieceBag.pop(0)
    piece = pieceType(0, 0)
    # Centers new piece
    row = 0
    col = app.board.getCols()//2 - piece.getCols()//2
    piece.setPos(row, col)
    return piece


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
    if key == 'z':
        app.fallingPiece.rotateCounterClockwise(app.board)
    elif key == 'x':
        app.fallingPiece.rotateClockwise(app.board)


def placeFallingPiece(app):
    app.board.putPieceIn(app, app.fallingPiece)
    linesCleared = app.board.removeRows()
    app.fallingPiece = newFallingPiece(app)

    app.score += app.scores[linesCleared]

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

    piece = app.fallingPiece
    app.board.render(app, canvas)
    piece.render(app, canvas, app.board)

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
