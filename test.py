import math
from queue import Queue
import grid
import time
import pygame
import random
import sys
from operator import itemgetter

EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4

class Graph():
    def __init__(self, size, start, end):
        self.size = size
        if self.size < 4:
            print("Size of graph is too small! (Size must be 4+)")
            return
        self.grid = []
        self.start = start
        self.end = end
        self.edges = {}
        self.initialize_grid()

    def initialize_grid(self):
        # Populate the grid with 0's
        for row in range(self.size):
            temp = []
            self.grid.append(temp)
            for box in range(self.size):
                temp.append(0)


        # Fix the grid edges to 1's
        for box in range(self.size):
            self.grid[0][box] = 1 # Top
            self.grid[box][0] = 1 # Left
            self.grid[box][self.size - 1] = 1  # Right
            self.grid[self.size - 1][box] = 1 # Bottom

        self.grid[self.start[1]][self.start[0]] = 2
        self.grid[self.end[1]][self.end[0]] = 3

        self.find_edges()

    def find_edges(self):
        for row in range(1, self.size - 1):
            for box in range(1, self.size - 1):
                neighbors = [(row-1, box), (row, box-1), (row+1, box), (row, box+1)] # the tuples of the boxes up, left, down, and right of current box
                self.edges[(row, box)] = neighbors

    def __print__(self):
        try:
            print(self.grid)
        except:
            return

def populate_dirty(grid, number, size):
    for x in range(number):
        randx = random.randrange(1, size - 1)
        randy = random.randrange(1, size - 1)
        if grid[randx][randy] != 1 and grid[randx][randy] != 2 and grid[randx][randy] != 3:
            grid[randx][randy] = 1

def check_distance(coorda, coordb):
    ax = coorda[0]
    ay = coorda[1]
    bx = coordb[0]
    by = coordb[1]

    return int(-(math.sqrt((bx-ax)**2 + (by-ay)**2) * 100))

def run():
    size = 250
    graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))
    populate_dirty(graph.grid, 30000, size)

    start = graph.start
    end = graph.end

    grid.initialize_grid(graph)

    found = 0
    #print(graph.grid)

    distance = {start:None}

    #queue = Queue()
    queue = []

    visited = [start]
    #queue.put(start)
    queue.insert(0, start)

    while queue and not found:
        #time.sleep(.1)
        #currentNode = queue.get()
        currentNode = queue.pop(0)
        #print(currentNode, end)
        nodeValue = graph.grid[currentNode[1]][currentNode[0]]


        if nodeValue == 0:
            grid.drawGrid2(graph, currentNode)
            graph.grid[currentNode[1]][currentNode[0]] = 4
        else:
            pass

        #visited.append(currentNode)
        edges = graph.edges.get(currentNode,None)
        if edges != None:
            closest_edge = []
            for edge in edges:
                if edge not in visited and graph.grid[edge[1]][edge[0]] != 1:
                    closest_edge.append((edge, check_distance(edge, end)))
                    #queue.put(edge)
                    visited.append(edge)
                    distance[edge] = currentNode
           # print(closest_edge)

            if True:
                closest_edge = sorted(closest_edge, key=itemgetter(1))

                if len(closest_edge) >= 1:
                    front = closest_edge[len(closest_edge) - 1]
                    queue.insert(0, front[0])

                for edge in range(len(closest_edge)):
                    #queue.put(edge[0])
                    queue.append(closest_edge[edge][0])

                #print(queue)


        if nodeValue == 3:
            #print(distance)
            found = 1

    finish = 0
    backtrack = end
    while not finish:
        time.sleep(.01)
        if backtrack == start:
            finish = 1
        if backtrack != start and backtrack != end:
            grid.drawGrid3(graph, backtrack)
        try:
            backtrack = distance[backtrack]
        except:
            print("No path found!")
            finish = 1

if __name__ == '__main__':
    while True:
        run()
        pygame.display.update()
        time.sleep(3)

