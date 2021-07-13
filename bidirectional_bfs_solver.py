from Graph import *

def bidirection_bfs_solver(graph):
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
    # time.sleep(2)

    while queue and queueEnd and not found:
        time.sleep(0.01)

        """Comment out queue and queueEnd for bidirectional bfs instead of bidirectional sorted queue"""
        queue = sorted(queue, key=itemgetter(1))
        queueEnd = sorted(queueEnd, key=itemgetter(1))

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
        else:
            pass

        if nodeValueEnd == 4:
            distancesend = currentNodeEnd[1]
            graph.grid[currentNodeEnd[0][0]][currentNodeEnd[0][1]] = 5
            grid.drawGrid2(graph, currentNodeEnd[0], distancesend)
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