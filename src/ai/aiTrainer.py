import sys
sys.path.insert(
    1, '/Users/ADMIN/Desktop/School/CMU/Fun/tetris-redo/src/main/components')

from gameClass import State
from tetrisAgent import TetrisAgent
from board import Board
from multiprocessing import Pool
import random


def testGame(t):
    heuristic, turns = t
    state = State(Board(24, 10, '⬛️'), TetrisAgent(), heuristic)
    state.start()
    for _ in range(turns):
        state = state.getBestNext()
        if state is None:
            return (float('-inf'), 0, heuristic)
    return state.fitness(), state.score, heuristic


def makeRandomHeuristic():
    cl = random.uniform(0, 1)
    h = random.uniform(-1, 0)
    b = random.uniform(-1, 0)
    ht = random.uniform(-1, 0)
    return (cl, h, b, ht)


def runGeneration(populationSize, population):
    with Pool(populationSize) as p:
        L = p.map(testGame, population)
    return L


def selectParents(L, num, stdDev):
    def fitness(t): return t[0] + stdDev
    return list(map(lambda t: t[2], sorted(L, key=fitness)[-num:]))


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


def getStdDev(L):
    scores = list(map(lambda t: t[1], L))
    avg = sum(scores)/len(scores)
    stdDev = (sum(map(lambda score: (score - avg)**2, scores))/len(scores))**0.5
    return stdDev


def mutateOne(h):
    i = random.randrange(0, len(h))
    delta = random.uniform(-h[i], h[i])
    res = list(h)
    res[i] = h[i] + delta
    return tuple(res)


def mutate(L):
    return list(map(mutateOne, L))


def main():
    populationSize = 10
    keptParents = 2
    turns = 100

    population = [(makeRandomHeuristic(), turns)
                  for _ in range(populationSize)]

    while True:
        L = runGeneration(populationSize, population)

        # Change the genese
        stdDev = getStdDev(L)
        parents = selectParents(L, keptParents, stdDev)
        crossoverL = crossover(L, populationSize - keptParents)
        toMutateL = crossoverL + parents
        mutateL = mutate(toMutateL)

        turns += 0 if max(L, key=lambda t: t[1])[0] == float('-inf') else 50
        population = list(map(lambda h: (h, turns), mutateL))

        print(max(L, key=lambda t: t[1]))


if __name__ == '__main__':
    main()
