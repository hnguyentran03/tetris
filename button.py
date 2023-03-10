from helpers import round_rectangle
from cmu_112_graphics import *


class Menu:
    def __init__(self, x0, y0, x1, y1, f):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.f = f
        self.title = ''
        self.data = ''
        self.shown = False

    def getData(self, title, data):
        self.title = title
        self.data = data

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False

    def inBounds(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def mousePressed(self, app, event):
        if not self.inBounds(event.x, event.y):
            self.f()

    def render(self, app, canvas):
        if self.shown:
            round_rectangle(app, canvas, self.x0, self.y0, self.x1, self.y1,
                            fill=app.bgColors[app.colorIndex], outline=app.buttonOutline[app.colorIndex])

            canvas.create_text((self.x1+self.x0)//2, (self.y0+self.y1)*2//10, text=self.title,
                               font=f'Helvetica {int((self.y1+self.y0)//10)} bold', fill=app.buttonOutline[app.colorIndex])

            canvas.create_text((self.x1+self.x0)//2, (self.y0+self.y1)*3//10, text=self.data,
                               font=f'Helvetica {int((self.y1+self.y0)//50)} bold', fill=app.buttonOutline[app.colorIndex], anchor=N)


class Button(Menu):
    def __init__(self, x0, y0, x1, y1, text, f):
        super().__init__(x0, y0, x1, y1, f)
        self.text = text
        self.hovered = False

    def inBounds(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def mousePressed(self, app, event):
        if self.inBounds(event.x, event.y):
            self.f()

    def hover(self, app, event):
        self.hovered = self.inBounds(event.x, event.y)

    def render(self, app, canvas):
        color = app.buttonHover[app.colorIndex] if self.hovered else app.buttonColors[app.colorIndex]
        round_rectangle(app, canvas, self.x0, self.y0, self.x1, self.y1,
                        outline=app.buttonOutline[app.colorIndex], fill=color)
        canvas.create_text((self.x1+self.x0)/2, (self.y1+self.y0)/2, text=self.text,
                           font=f'Helvetica {int((self.y1-self.y0)/3)}', fill=app.buttonOutline[app.colorIndex])
