from Graph import *
import grid
import random
from bidirectional_bfs_solver import bidirection_bfs_solver

PIXEL_SIZE = 10

def init():
    # Initialize a graph object, the graph object should be showing on the screen
    size = int(grid.WIDTH / PIXEL_SIZE)
    graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))
    # Initialize generating a maze onto the graph object
    populate_maze(graph, size)
    graph.place_start_end()
    grid.initialize_grid(graph)
    # Create the start and end point onto the graph and start the solver
    bidirection_bfs_solver(graph)