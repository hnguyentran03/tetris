def getCellBounds(app, board, row, col):
    #Taken from 112 Notes/Lecture
    gridWidth  = app.width - 2*app.margin
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