from cmu_112_graphics import *
from helpers import drawBackground, readHighScores, round_rectangle
from game import game_appStarted
from button import Button, Menu


def startButton(app):
    app.mode = 'game'
    game_appStarted(app)


def scoreButton(app):
    readHighScores(app)
    app.showScore = True
    listScores = list(app.scores.items())
    listScores.sort(key=lambda t: t[1])
    formattedScores = ''
    for name, score in listScores:
        formattedScores += f'{name}: {score}\n'
    app.menu.getData('Scores', formattedScores)


def menuEffect(app):
    app.showScore = False


def splash_appStarted(app):
    start = Button(2*app.width//5, app.height*2//10, 3*app.width //
                   5, app.height*3//10, 'Start', lambda: startButton(app))
    score = Button(2*app.width//5, app.height*3.5//10, 3*app.width //
                   5, app.height*4.5//10, 'Scores', lambda: scoreButton(app))
    stop = Button(2*app.width//5, app.height*5//10, 3*app.width //
                   5, app.height*6//10, 'Quit', app.quit)
    app.menu = Menu(app.width//5, app.height//10, app.width*4//5, app.height*9//10, lambda: menuEffect(app))
    app.buttons = [start, score, stop]
    app.showScore = False


def splash_mouseMoved(app, event):
    for button in app.buttons:
        button.hover(app, event)


def splash_mousePressed(app, event):
    for button in app.buttons:
        button.mousePressed(app, event)

    if app.showScore:
        app.menu.mousePressed(app, event)


def drawTitle(app, canvas):
    canvas.create_text(app.width//2, app.height//10, text='TETRIS',
                       font=f'Helvetica {int(app.height//10)} bold')


def splash_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawTitle(app, canvas)

    for button in app.buttons:
        button.render(app, canvas)

    if app.showScore:
        app.menu.render(app, canvas)
