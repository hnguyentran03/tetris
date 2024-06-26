import sys
sys.path.insert(
    1, '../main')

import gameClass
from tetrisAgent import TetrisAgent
from board import Board
from multiprocessing import Pool
import random

# Runs a full game and returns the fitness, score and heuristic
def testGame(t):
    heuristic, turns = t
    state = State(Board(24, 10, '⬛️'), TetrisAgent(), heuristic)
    state.start()
    for _ in range(turns):
        state = state.getBestNext()
        if state is None:
            return (float('-inf'), 0, heuristic)
    return state.fitness(), state.score, heuristic

# This heuristic is based on the website cited.
def makeRandomHeuristic():
    # cl = random.uniform(0, 1)
    # h = random.uniform(-1, 0)
    # b = random.uniform(-1, 0)
    # ht = random.uniform(-1, 0)
    height = -0.510066
    clearedLines = 0.760666
    holes = -0.35663
    bumpiness = -0.184483
    return (clearedLines, holes, bumpiness, height)

# Runs an entire generation of agents
def runGeneration(populationSize, population):
    with Pool(populationSize) as p:
        L = p.map(testGame, population)
    return L

# StdDev of scores
def getStdDev(L):
    scores = list(map(lambda t: t[1], L))
    avg = sum(scores)/len(scores)
    stdDev = (sum(map(lambda score: (score - avg)**2, scores))/len(scores))**0.5
    return stdDev

# Selects the parents based on the fitness + stDev(score)
def selectParents(L, num, stdDev):
    def fitness(t): return t[0] + stdDev
    return list(map(lambda t: t[2], sorted(L, key=fitness)[-num:]))

# Currently chooses 2 random parents and makes 2 children
def crossover(L, num):
    res = []
    for _ in range(num//2):
        p1, p2 = random.sample(L, len(L)-num)
        _, _, parent1 = p1
        _, _, parent2 = p2
        i = random.randrange(0, len(parent1))
        child1 = list(parent1)
        child1[i] = parent2[i]
        child2 = list(parent2)
        child2[i] = parent1[i]

        res.extend([tuple(child1), tuple(child2)])
    return res

# Mutates them by choosing a random heuristic value, and changing it by a random amount between +-value/2
def mutateOne(h):
    i = random.randrange(0, len(h))
    delta = random.uniform(-h[i]/2, h[i]/2)
    res = list(h)
    res[i] = h[i] + delta
    return tuple(res)

# Mutates all children
def mutate(L):
    return list(map(mutateOne, L))


def main():
    populationSize = 10
    keptParents = 2
    turns = 100

    population = [(makeRandomHeuristic(), turns)
                  for _ in range(populationSize)]

    iterations = 0

    while True:
        L = runGeneration(populationSize, population)

        # Change the genese
        stdDev = getStdDev(L)
        parents = selectParents(L, keptParents, stdDev)
        crossoverL = crossover(L, populationSize - keptParents)
        toMutateL = crossoverL + parents
        mutateL = mutate(toMutateL)

        population = list(map(lambda h: (h, turns), mutateL))

        turns += 0 if max(L, key=lambda t: t[1])[0] == float('-inf') or iterations > 15 else 50
        iterations += 1

        print(f'generation {iterations}', max(L, key=lambda t: t[1]), max(L, key=lambda t: t[0]))


if __name__ == '__main__':
    main()