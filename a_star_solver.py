from Graph import *

def get_distance(coorda, coordb):
    ax = coorda[0]
    ay = coorda[1]
    bx = coordb[0]
    by = coordb[1]

    """Change to either to change the visual looks when pathfinding"""
    # return float((math.sqrt((bx-ax)**2 + (by-ay)**2)))
    return abs(bx-ax) + abs(by-ay)

def a_star_solver(graph):
    start = graph.start
    end = graph.end
    found = 0

    # Dictionaries to trace which node found which in the order -> {child: parent}
    # For the following, we use two of each to record each of the two, start and end nodes
    distance = {start: [None, get_distance(start, end), 0]}

    # f(n) = g(n) + h(n)
    # f is the total score
    # g is the distance from start node to n
    # h is the estimate from node to end

    # Arrays to keep trace of which nodes to search next
    # Initializes the queue to first track the start and end simultaneously

    # Node(coordinates, length of shortest distance from starting node, distance from this node to the end node using Euclidean distance)
    queue = []
    queue.append((start, distance.get(start)[1]))

    # Time to wait before solving the maze
    # time.sleep(2)

    while queue and not found:
        time.sleep(.001)

        """Comment out queue and queueEnd for bidirectional bfs instead of bidirectional sorted queue"""
        queue = sorted(queue, key=itemgetter(1))

        # Pop the first element in the queue
        currentNode = queue.pop(0)
        # print(currentNode)

        # Assign the value of this node to a variable used to detect if the node is an empty cell
        nodeValue = graph.grid[currentNode[0][0]][currentNode[0][1]]

        # If the node IS an emtpy cell, then draw the cell as visited and mark it as visited
        if nodeValue == 4:
            distances = currentNode[1] * 100
            # print(distances)
            graph.grid[currentNode[0][0]][currentNode[0][1]] = 5
            grid.drawGrid2(graph, currentNode[0], distances)

        # Gets all the neighbors of the node
        edges = graph.edges.get(currentNode[0], None)

        # For the neighbors of the node, check that each of it's neighbors are not in the start node's visited array
        # If the node's neighbor is in the start node's visited array, then take the current backtrace of end node and add it onto start node (backtrace)
        # If the node's neighbor is not in the start node's visited array, then add this node to the backtrace of end node

        if edges != None and not found:
            for edge in edges:
                if edge not in distance.keys() and graph.grid[edge[0]][edge[1]] != 1:
                    if graph.grid[edge[0]][edge[1]] != 3:
                        graph.grid[edge[0]][edge[1]] = 4
                    g_Score = distance.get(currentNode[0])[2] + 1
                    h_Score = get_distance(edge, end)
                    f_Score = float(g_Score + h_Score)
                    # print(g_Score,h_Score,f_Score)

                    queue.append((edge, f_Score))
                    grid.drawGrid2(graph, edge, check_distance(edge, end))
                    distance[edge] = [currentNode[0], f_Score, g_Score]

        if currentNode[0] == end:
            found = True

    # Backtraces the given dictionary of child: parent pairs
    # Shows the parent value that found the child key
    finish = 0
    count = 0
    backtrack = end
    while not finish:
        time.sleep(.001)
        if backtrack == start:
            finish = 1
            print(count)
        if backtrack != start and backtrack != end:
            grid.drawGrid3(graph, backtrack)
            count += 1
        try:
            backtrack = distance[backtrack][0]
        except:
            print(f"No path found!")
            finish = 1