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

        # Place the start and end node on the graph
        self.grid[self.start[1]][self.start[0]] = 2
        self.grid[self.end[1]][self.end[0]] = 3

        # Fix the border of the graph, make all boxes on the edges of the graph into walls
        self.find_edges()

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

# Function to randomly generate a maze/noise using inputs of the grid, the number of dirty boxes, and the size of the graph
def populate_dirty(grid, number, size):
    for x in range(number):
        randx = random.randrange(1, size - 1)
        randy = random.randrange(1, size - 1)
        if grid[randx][randy] != 1 and grid[randx][randy] != 2 and grid[randx][randy] != 3:
            grid[randx][randy] = 1

def populate_clean(grid, startcorner, endcorner):
    width = endcorner[1] - startcorner[1] + 1
    height = endcorner[0] - startcorner[0] + 1
    #print(f"width: {width}, height: {height}, start: {startcorner}, end: {endcorner}")
    if width == 5 and height == 5:
        #print("what")
        return #print("basecase")
    if width >= height:
        #print("vertical")
        cut = None
        if width % 2 == 0:
            cut = int(width/2) - 1
        else:
            cut = int(width/5) - 1
        for y in range(height):
            #print(y, cut)
            grid[startcorner[0] + y][startcorner[1] + cut] = 1
        for x in range(max(int(height/5), 2)):
            if height != 1:
                grid[random.randrange(startcorner[0], endcorner[0])][startcorner[1] + cut] = 0
        #print((startcorner[0], startcorner[1] + cut), endcorner)
        return populate_clean(grid, startcorner, (endcorner[0], startcorner[1] + cut)), populate_clean(grid, (startcorner[0], startcorner[1] + cut + 1), endcorner)
    else:
        #print("horizontal")
        cut = None
        if height % 2 == 0:
            cut = int(height/2) - 1
        else:
            cut = int(height/5) - 1
        for y in range(width):
            #print(cut)
            grid[startcorner[0] + cut][startcorner[1] + y] = 1
        for x in range(max(int(width/5), 2)):
            if width != 1:
                grid[startcorner[0] + cut][random.randrange(startcorner[1], endcorner[1])] = 0
        #print(grid, (startcorner[0] + cut, startcorner[1]), endcorner)
        return populate_clean(grid, startcorner, (startcorner[0] + cut, endcorner[1])), populate_clean(grid, (startcorner[0] + cut + 1, startcorner[1]), endcorner)

# Takes the distance formula and apply it to two points in the graph
def check_distance(coorda, coordb):
    ax = coorda[0]
    ay = coorda[1]
    bx = coordb[0]
    by = coordb[1]

    return int((math.sqrt((bx-ax)**2 + (by-ay)**2) * 100))

def run():
    size = int(grid.WIDTH/2)
    graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))

    populate_clean(graph.grid, (0,0), (graph.size - 1, graph.size - 1))
    # populate_dirty(graph.grid, grid.WIDTH * int(grid.WIDTH/8), size)
    grid.initialize_grid(graph)

    start = graph.start
    end = graph.end
    found = 0

    # Dictionaries to trace which node found which in the order -> {child: parent}
    # For the following, we use two of each to record each of the two, start and end nodes
    distance = {start: None}
    distanceEnd = {end: None}

    # Arrays to keep trace of which nodes to search next
    # Initializes the queue to first track the start and end simultaneously
    queue = []
    queueEnd = []
    queue.append((start, sys.maxsize))
    queueEnd.append(((end), sys.maxsize))

    # Time to wait before solving the maze
    time.sleep(2)

    while queue and queueEnd and not found:
        #time.sleep(0.1)

        # Switch between these two queue methods to change the way the program searches
        # random.shuffle(queue)
        # random.shuffle(queueEnd)
        queue = sorted(queue, key=itemgetter(1))
        queueEnd = sorted(queueEnd, key=itemgetter(1))

        # Pop the first element in the queue
        currentNode = queue.pop(0)
        currentNodeEnd = queueEnd.pop(0)

        # Assign the value of this node to a variable used to detect if the node is an empty cell
        nodeValue = graph.grid[currentNode[0][1]][currentNode[0][0]]
        nodeValueEnd = graph.grid[currentNodeEnd[0][1]][currentNodeEnd[0][0]]

        # If the node IS an emtpy cell, then draw the cell as visited and mark it as visited
        if nodeValue == 0:
            distances = currentNode[1]
            grid.drawGrid2(graph, currentNode[0], distances)
            graph.grid[currentNode[0][1]][currentNode[0][0]] = 4
        else:
            pass

        if nodeValueEnd == 0:
            distancesend = currentNodeEnd[1]
            grid.drawGrid2(graph, currentNodeEnd[0], distancesend)
            graph.grid[currentNodeEnd[0][1]][currentNodeEnd[0][0]] = 4
        else:
            pass

        # Gets all the neighbors of the node
        edges = graph.edges.get(currentNode[0], None)
        edgesEnd = graph.edges.get(currentNodeEnd[0], None)

        # For the neighbors of the node, check that each of it's neighbors are not in the start node's visited array
        # If the node's neighbor is in the start node's visited array, then take the current backtrace of end node and add it onto start node (backtrace)
        # If the node's neighbor is not in the start node's visited array, then add this node to the backtrace of end node
        if edgesEnd != None and not found:
            for edge in edgesEnd:
                if edge in distance.keys() and not found:
                    print("End found start tip")
                    found = 1
                    temp = edge  # parent of current node we working with
                    distance[currentNodeEnd[0]] = temp
                    temp = currentNodeEnd[0]
                    while temp != end and temp != None:
                        child = distanceEnd[temp]
                        distance[child] = temp
                        temp = child
                if edge not in distance.keys() and edge not in distanceEnd.keys() and graph.grid[edge[1]][edge[0]] != 1:
                    queueEnd.append((edge, check_distance(edge, start)))
                    distanceEnd[edge] = currentNodeEnd[0]

        if edges != None and not found:
            for edge in edges:
                if edge in distanceEnd.keys():
                    print("Start found end tip")
                    found = 1
                    temp = currentNode[0]  # parent of current node we working with
                    distance[edge] = temp
                    temp = edge
                    while temp != end and temp != None:
                        child = distanceEnd[temp]
                        distance[child] = temp
                        temp = child
                if edge not in distance and edge not in distanceEnd and graph.grid[edge[1]][edge[0]] != 1:
                    queue.append((edge, check_distance(edge, end)))
                    distance[edge] = currentNode[0]

        # Safety check that validates that the node
        # if nodeValue == 3:
        #     print("reached")
        #     found = 1


    # Backtraces the given dictionary of child: parent pairs
    # Shows the parent value that found the child key
    finish = 0
    backtrack = end
    while not finish:
        time.sleep(.001)
        if backtrack == start:
            finish = 1
        if backtrack != start and backtrack != end:
            grid.drawGrid3(graph, backtrack)
        try:
            backtrack = distance[backtrack]
        except:
            print(f"No path found!")
            finish = 1

if __name__ == '__main__':
    while True:
        old_time = time.time()
        run()
        pygame.display.update()
        print(f"Time taken: {time.time()- old_time}")
        print("Running next generation")
        time.sleep(2)

