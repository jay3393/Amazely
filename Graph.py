import math
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
EXPLORED = 5

class Graph():
    """
    Graph class contains grid to show the value of each box in the grid
    Used to initialize and display pathfinding algorithm
    """
    def __init__(self, size, start, end):
        self.size = size
        if self.size < 4:
            print("Size of graph is too small! (Size must be 4+)")
            return
        self.grid = []
        self.start = start
        self.end = end
        self.edges = {}
        self.border = []
        self.initialize_grid()

    def initialize_grid(self):
        # Populate the grid with 0's
        for row in range(self.size):
            temp = []
            self.grid.append(temp)
            for box in range(self.size):
                temp.append(0)

        # Make all boxes on the edges of the graph into walls
        self.create_border()
        self.find_edges()

    # Place the start and end node on the graph
    def place_start_end(self):
        self.start = (random.randrange(1, self.size - 1), random.randrange(1, self.size - 1))
        self.end = (random.randrange(1, self.size - 1), random.randrange(1, self.size - 1))
        if self.grid[self.start[0]][self.start[1]] == 0 and self.grid[self.end[0]][self.end[1]] == 0:
            self.grid[self.start[0]][self.start[1]] = 2
            self.grid[self.end[0]][self.end[1]] = 3
        else:
            self.place_start_end()

    # Fix the border of the graph
    def create_border(self):
        # Fix the grid edges to 1's
        for box in range(self.size):
            self.grid[0][box] = 1  # Top
            self.grid[box][0] = 1  # Left
            self.grid[box][self.size - 1] = 1  # Right
            self.grid[self.size - 1][box] = 1  # Bottom
            self.border.append((0,box))
            self.border.append((box, 0))
            self.border.append((box, self.size - 1))
            self.border.append((self.size - 1, box))

    # Function to populate the edges of the graph to 1's (walls)
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

# Takes the distance formula and apply it to two points in the graph
def check_distance(coorda, coordb):
    ax = coorda[0]
    ay = coorda[1]
    bx = coordb[0]
    by = coordb[1]

    return int((math.sqrt((bx-ax)**2 + (by-ay)**2) * 100))

# Function to randomly generate noise
def populate_dirty(grid, number, size):
    for x in range(number):
        randx = random.randrange(1, size - 1)
        randy = random.randrange(1, size - 1)
        if grid[randx][randy] != 1 and grid[randx][randy] != 2 and grid[randx][randy] != 3:
            grid[randx][randy] = 1

def populate_maze(graph, size):
    walls = []
    gridder = graph.grid
    groupings = []
    for y in range(2, size - 2, 2):
        for x in range(0, size - 2):
            gridder[y][x] = 1
        for x in range(1, size - 2, 2):
            walls.append((y, x))
            gridder[y][x] = 1

    for x in range(2, size - 2, 2):
        for y in range(0, size - 2):
            gridder[y][x] = 1
        for y in range(1, size - 2, 2):
            walls.append((y, x))
            gridder[y][x] = 1

    for x in range(size - 1):
        gridder[size - 2][x] = 1
        gridder[x][size - 2] = 1

    grid.WIN.fill((0, 0, 0))
    # grid.initialize_grid(graph)

    while True and walls:
        #print(f"Walls: {len(walls)}, groupings: {len(groupings)}")
        # Randomly chooses a removable wall and removes it from that group
        node = random.choice(walls)
        walls.remove(node)

        boxes = []
        for edge in graph.edges[node]:
            if gridder[edge[0]][edge[1]] == 0:
                boxes.append(edge)

        # Should only have 2 white spaces to worry about
        # Check that both white spaces are not in the same grouping
        box1 = boxes[0]
        box2 = boxes[1]
        container1 = None
        container2 = None

        for group in groupings:
            if box1 in group:
                container1 = group
            if box2 in group:
                container2 = group

        # If the containers are both None, then make a new grouping and add those two tuples in that grouping
        if container1 == None and container2 == None:
            # print("Both boxes are not in any groupings, remove wall")
            grouping = [box1, box2]
            groupings.append(grouping)
            gridder[node[0]][node[1]] = 0
            gridder[box1[0]][box1[1]] = 0
            gridder[box2[0]][box2[1]] = 0

        # If the containers are both in the same grouping then don't remove the wall
        elif container1 != None and container1 == container2:
            gridder[node[0]][node[1]] = 1

        # If both containers are different (either or neither but not both can be None),
        # then remove both groupings, add a new one and add both boxes to the new grouping
        elif container1 != container2:
            gridder[node[0]][node[1]] = 0
            gridder[box1[0]][box1[1]] = 0
            gridder[box2[0]][box2[1]] = 0
            if container1 != None and container2 != None:
                #print("Boxes are in different groupings, combine them")
                grouping = container1 + container2
                groupings.remove(container1)
                groupings.remove(container2)
                groupings.append(grouping)
            elif container1 == None:
                groupings[groupings.index(container2)].append(box1)
            elif container2 == None:
                groupings[groupings.index(container1)].append(box2)

        grid.drawGrid2(graph, node, None)
        grid.drawGrid2(graph, box1, None)
        grid.drawGrid2(graph, box2, None)