# File IO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()


def writeFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)


# Board
def getCellBounds(app, board, row, col):
    # Taken from 112 Notes/Lecture
    gridWidth = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / board.getCols()
    cellHeight = gridHeight / board.getRows()
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight

    return x0, x1, y0, y1


def reverseBoard(board):
    return board[::-1]

# Taken from 112 Notes
def repr2dList(L):
    if (L == []):
        return '[]'
    output = []
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

# Drawing


def drawCell(app, canvas, board, row, col, color, outline):
    x0, x1, y0, y1 = getCellBounds(app, board, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                            outline=outline, width=app.cellMargin)


def drawBoxCell(app, canvas, location, row, col, color):
    boxSize = app.cellSize/2
    boxMargin = app.cellMargin/2
    x, y = location
    canvas.create_rectangle(x+(col-1)*boxSize, y+(row-1)*boxSize,
                            x+col*boxSize, y+row*boxSize,
                            fill=color,
                            outline=app.widthColors[app.colorIndex],
                            width=boxMargin)
