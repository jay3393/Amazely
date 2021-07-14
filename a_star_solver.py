from Graph import *

def a_star_solver(graph):
    start = graph.start
    end = graph.end
    found = 0

    # Dictionaries to trace which node found which in the order -> {child: parent}
    # For the following, we use two of each to record each of the two, start and end nodes
    distance = {start: None}

    # Arrays to keep trace of which nodes to search next
    # Initializes the queue to first track the start and end simultaneously

    # Node(coordinates, length of shortest distance from starting node, distance from this node to the end node using Euclidean distance)
    queue = []
    queue.append((start, 0, check_distance(start, end)))

    # Time to wait before solving the maze
    # time.sleep(2)

    while queue and not found:
        time.sleep(0.001)

        """Comment out queue and queueEnd for bidirectional bfs instead of bidirectional sorted queue"""
        queue = sorted(queue, key=itemgetter(2))

        # Pop the first element in the queue
        currentNode = queue.pop(0)

        # Assign the value of this node to a variable used to detect if the node is an empty cell
        nodeValue = graph.grid[currentNode[0][0]][currentNode[0][1]]

        # If the node IS an emtpy cell, then draw the cell as visited and mark it as visited
        if nodeValue == 4:
            distances = currentNode[2]
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
                    graph.grid[edge[0]][edge[1]] = 4
                    shortest_dist = currentNode[1] + 1
                    #print(int(check_distance(edge, end)) + shortest_dist)
                    queue.append((edge, shortest_dist, int(check_distance(edge, end)/100) + shortest_dist))
                    grid.drawGrid2(graph, edge, check_distance(edge, end))
                    distance[edge] = currentNode[0]

        if currentNode[0] == end:
            found = True

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