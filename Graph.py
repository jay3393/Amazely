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
    # Adjust minsize to determine base room size for recursion
    minsize = 5
    if width == minsize and height == minsize:
        #print(f"width: {width}, height: {height}, start: {startcorner}, end: {endcorner}")
        horizontal = random.choice([0,1])
        # 0 = vertical
        # 1 = horizontal
        if horizontal:
            #print("horizontal")
            for x in range(minsize):
                grid[startcorner[1] + 1][random.randrange(startcorner[0], endcorner[0])] = 1
                #grid[startcorner[1] + 3][random.randrange(startcorner[0], endcorner[0])] = 2
        else:
            #print("vertical")
            for x in range(minsize):
                grid[random.randrange(startcorner[1], endcorner[1])][startcorner[0] + 1] = 1
                #grid[random.randrange(startcorner[1], endcorner[1])][startcorner[0] + 3] = 1

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
            # box = grid[startcorner[0] + y][startcorner[1] + cut]
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
        print(f"Walls: {len(walls)}, groupings: {len(groupings)}")
        # time.sleep(0.005)
        # Randomly chooses a removable wall and removes it from that group
        node = random.choice(walls)
        #node = x
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
                #print("box1")
                container1 = group
            if box2 in group:
                #print("box2")
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
                #print("Add box1 to box2 grouping")
                groupings[groupings.index(container2)].append(box1)
            elif container2 == None:
                #print("Add box1 to box2 grouping")
                groupings[groupings.index(container1)].append(box2)

        grid.drawGrid2(graph, node, None)
        grid.drawGrid2(graph, box1, None)
        grid.drawGrid2(graph, box2, None)

def run():
    size = int(grid.WIDTH/2)
    graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))


    populate_maze(graph, size)
    # populate_clean(graph.grid, (0,0), (graph.size - 1, graph.size - 1))
    # populate_dirty(graph.grid, grid.WIDTH * int(grid.WIDTH/8), size)
    # graph.create_border()
    graph.place_start_end()
    grid.initialize_grid(graph)

    #print(graph.grid[graph.start[1]][graph.start[0]], graph.end)

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
        #time.sleep(0.01)

        """Switch between these two queue methods to change the way the program searches"""
        # random.shuffle(queue)
        # random.shuffle(queueEnd)
        # queue = sorted(queue, key=itemgetter(1))
        # queueEnd = sorted(queueEnd, key=itemgetter(1))

        # Pop the first element in the queue
        currentNode = queue.pop(0)
        currentNodeEnd = queueEnd.pop(0)

        # Assign the value of this node to a variable used to detect if the node is an empty cell
        nodeValue = graph.grid[currentNode[0][0]][currentNode[0][1]]
        nodeValueEnd = graph.grid[currentNodeEnd[0][0]][currentNodeEnd[0][1]]

        # If the node IS an emtpy cell, then draw the cell as visited and mark it as visited
        if nodeValue == 4:
            distances = currentNode[1]
            graph.grid[currentNode[0][0]][currentNode[0][1]] = 5
            grid.drawGrid2(graph, currentNode[0], distances)
            #graph.grid[currentNode[0][1]][currentNode[0][0]] = 4
        else:
            pass

        if nodeValueEnd == 4:
            distancesend = currentNodeEnd[1]
            graph.grid[currentNodeEnd[0][0]][currentNodeEnd[0][1]] = 5
            grid.drawGrid2(graph, currentNodeEnd[0], distancesend)
            #graph.grid[currentNodeEnd[0][1]][currentNodeEnd[0][0]] = 5
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
                if edge not in distance.keys() and edge not in distanceEnd.keys() and graph.grid[edge[0]][edge[1]] != 1:
                    graph.grid[edge[0]][edge[1]] = 4
                    queueEnd.append((edge, check_distance(edge, start)))
                    """draws the visited nodes"""
                    grid.drawGrid2(graph, edge, check_distance(edge, start))
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
                if edge not in distance.keys() and edge not in distanceEnd.keys() and graph.grid[edge[0]][edge[1]] != 1:
                    graph.grid[edge[0]][edge[1]] = 4
                    queue.append((edge, check_distance(edge, end)))
                    grid.drawGrid2(graph, edge, check_distance(edge, end))
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
        time.sleep(3)

