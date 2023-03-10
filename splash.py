from cmu_112_graphics import *
from helpers import drawBackground, readHighScores, readFile
from game import game_appStarted
from button import Button, Menu

# EFFECTS FOR BUTTONS AND MENUS


def startButton(app):
    app.mode = 'game'
    game_appStarted(app)


def scoreButton(app):
    readHighScores(app)
    app.scoreMenu.show()
    listScores = list(app.scores.items())
    listScores.sort(key=lambda t: t[1])
    formattedScores = ''
    for name, score in listScores:
        formattedScores += f'{name}: {score}\n'
    app.scoreMenu.getData('Scores', formattedScores)


def scoreMenuEffect(app):
    app.scoreMenu.hide()


def controlButton(app):
    formattedControls = ''
    for name, conList in app.controls.items():

        formattedControls += f'{name}: {conList}\n'
    app.controlMenu.show()
    app.controlMenu.getData('Controls', formattedControls)


def controlMenuEffect(app):
    app.controlMenu.hide()

# INITIALIZE SPLASHSCREEN


def splash_appStarted(app):
    start = Button(2*app.width//5, app.height*2//10, 3*app.width //
                   5, app.height*3//10, 'Start', lambda: startButton(app))
    score = Button(2*app.width//5, app.height*3.5//10, 3*app.width //
                   5, app.height*4.5//10, 'Scores', lambda: scoreButton(app))
    controls = Button(2*app.width//5, app.height*5//10, 3*app.width //
                      5, app.height*6//10, 'Controls', lambda: controlButton(app))
    stop = Button(2*app.width//5, app.height*6.5//10, 3*app.width //
                  5, app.height*7.5//10, 'Quit', app.quit)

    app.buttons = [start, score, controls, stop]

    app.scoreMenu = Menu(app.width//5, app.height//10, app.width*4//5, app.height*9 //
                         10, lambda: scoreMenuEffect(app))
    app.controlMenu = Menu(app.width//5, app.height//10, app.width*4//5, app.height*9 //
                           10, lambda: controlMenuEffect(app))

    app.menus = [app.scoreMenu, app.controlMenu]


def splash_mouseMoved(app, event):
    for button in app.buttons:
        button.hover(app, event)


def splash_mousePressed(app, event):
    for button in app.buttons:
        button.mousePressed(app, event)

    for menu in app.menus:
        menu.mousePressed(app, event)


def drawTitle(app, canvas):
    canvas.create_text(app.width//2, app.height//10, text='TETRIS',
                       font=f'Helvetica {int(app.height//10)} bold')


def splash_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawTitle(app, canvas)

    for button in app.buttons:
        button.render(app, canvas)

    for menu in app.menus:
        menu.render(app, canvas)
