# tetris
The base of this project is from the 15-112 Tetris homework guide: https://www.cs.cmu.edu/~112-f22/notes/notes-tetris/index.html.

On top of it, I revamped it with OOP, a scoreboard, a next piece preview, holding pieces, an outline for where the piece will be droppeed, and an AI that simulates all moves and chooses the best one based on a heuristic.

Currently, the heuristic ideas are taken from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/. But I implemented my own genetic algorithm to help calculate my own heuristic.

To start the program, run the main.py file in src/main/main.py.