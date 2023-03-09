from cmu_112_graphics import *
from splash import *
from game import *


def appStarted(app):
    # Colors
    app.colorIndex = 1
    app.textColors = ['blue', 'yellow']
    app.bannerTextColors = ['yellow', 'black']
    app.bannerColors = ['black', 'yellow']
    app.bgColors = ['orange', 'black']

    # Button Colors
    app.buttonColors = ['orange', 'grey']
    app.buttonOutline = ['blue', 'white']
    app.buttonHover = ['dark orange', 'grey19']

    # Board Colors
    app.emptyColors = ['blue', 'black']
    app.widthColors = ['black', 'grey19']

    app.mode = 'splash'
    splash_appStarted(app)

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


if __name__ == '__main__':
    playTetris()
