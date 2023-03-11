class TetrisAgent:
    def getAllActions(self, state):
        board = state.getBoard()
        res = []
        for hold in range(2):
            for col in range(board.getCols()):
                for rotation in range(4):
                    res.append(
                        {'hold': bool(hold), 'col': col, 'rotate': rotation})
        return res