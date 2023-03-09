import random
from cmu_112_graphics import *
import board
from pieces import *
from helpers import readFile, writeFile, sign
from ai import simulateAll, simHardDrop


def readHighScores(app):
    s = readFile('scores.txt')
    app.scores = parseHighScores(s)
    if app.scores:
        app.highScoreName, app.highScore = (max(
            app.scores, key=app.scores.get), max(app.scores.values()))
    else:
        app.highScoreName, app.highScore = 'None', 0


def parseHighScores(s):
    scores = dict()
    for line in s.splitlines():
        name, score = line.split(',')
        scores[name] = int(score)
    return scores


def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.cellMargin = app.cellSize/24
    app.pieces = [iPiece, jPiece, lPiece,
                  zPiece, sPiece, oPiece, tPiece]

    # Other Colors
    app.colorIndex = 1
    app.textColors = ['blue', 'yellow']
    app.bannerTextColors = ['yellow', 'black']
    app.bannerColors = ['black', 'yellow']
    app.bgColors = ['orange', 'black']

    # Board Colors
    app.emptyColors = ['blue', 'black']
    app.widthColors = ['black', 'grey19']
    # {'single': 100, 'double': 300, 'triple': 500, 'tetris': 800}
    app.points = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
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
    readHighScores(app)
    app.board = board.Board(
        app.rows, app.cols, app.emptyColors[app.colorIndex])

    nextBoard(app)
    holdBoard(app)

    app.timerDelay = 20
    app.timePassed = 0
    app.defaultSpeed = 1000

    app.score = 0
    app.blockSpeed = app.defaultSpeed - 5*app.score

    app.isGameOver = False
    app.paused = False
    app.auto = False

    app.pieceBag = makeBag(app)
    app.fallingPiece = newPiece(app)
    app.nextPiece = newPiece(app)
    app.holdPiece = None
    newOutline(app)

    app.canHold = True
    app.switch = False
    app.moves = simulateAll(app)


def makeBag(app):
    return random.sample(app.pieces, k=len(app.pieces))


def nextFallingPiece(app):
    app.fallingPiece = app.nextPiece
    app.nextPiece = newPiece(app)
    newOutline(app)


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


def newOutline(app):
    app.outline = Outline(app.fallingPiece, app.board)
    app.outline.update(app.board)


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
    newOutline(app)


def keyPressed(app, event):
    key = event.key
    # Misc
    if key == 'r':
        if app.isGameOver:
            name = app.getUserInput('What is your name?')
            writeFile('scores.txt', f'{name},{app.score}\n')
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

    if key == 'w':
        hold, col, rotation = app.moves
        app.fallingPiece.setPos(app.fallingPiece.getRow(), col)
        for _ in range(rotation):
            app.fallingPiece.rotateCounterClockwise(app.board, False)
        simHardDrop(app.fallingPiece, app.board)
        placeFallingPiece(app)

    if key == 'a':
        app.auto = not app.auto

    # if key == 'd':
    #     for k, v in app.aiTest.items():
    #         score, rest = v
    #         print(f'{k}: {score}')
    #     print()

    # print(app.aiTest[app.moves][1])
    app.outline.update(app.board)


def placeFallingPiece(app):
    app.canHold = True
    app.board.putPieceIn(app, app.fallingPiece)
    linesCleared = app.board.removeRows()
    app.score += app.points[linesCleared]

    nextFallingPiece(app)
    app.moves = simulateAll(app)
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

    if app.auto:
        _, col, rotation = app.moves

        if app.fallingPiece.getRotation() != rotation:
            app.fallingPiece.rotateCounterClockwise(app.board)
        elif app.fallingPiece.getCol() != col:
            dcol = sign(col - app.fallingPiece.getCol())
            app.fallingPiece.move(app.board, 0, dcol)
        else:
            app.fallingPiece.move(app.board, +1, 0)
        newOutline(app)


def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill=app.bgColors[app.colorIndex])


def drawScore(app, canvas):
    canvas.create_text(app.width//2, app.margin - app.cellSize//2,
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


def drawScores(app, canvas):
    canvas.create_text(app.width/2, app.margin + 2.5*app.cellSize,
                       text=f'Score: {app.score}     High Score: {app.highScore} by {app.highScoreName}',
                       fill=app.bannerTextColors[app.colorIndex], font=f"Helvetica {app.cellSize//2} bold", anchor=CENTER)


def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawScore(app, canvas)

    app.board.render(app, canvas)
    if not app.isGameOver:
        app.outline.render(app, canvas, app.board)
    app.fallingPiece.render(app, canvas, app.board)

    app.nextBoard.render(app, canvas)
    app.nextPiece.renderBox(app, canvas, app.nextBoard)

    app.holdBoard.render(app, canvas)
    if app.holdPiece:
        app.holdPiece.renderBox(app, canvas, app.holdBoard)

    if app.isGameOver:
        drawText(app, canvas, 'Game Over')
        drawScores(app, canvas)

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
