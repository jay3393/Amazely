from Graph import *
import grid
import random
from bidirectional_bfs_solver import bidirection_bfs_solver
from a_star_solver import a_star_solver
import pygame

PIXEL_SIZE = 10
"""False = maze generation, True = custom walls"""
CUSTOM_WALLS = True

def get_grid_pos(pos, gap):
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col

def init():
    # Initialize size of graph
    size = int(grid.WIDTH / PIXEL_SIZE)
    # Initialize generating a maze onto the graph object (define CUSTOM_WALLS = True to allow building your own walls)
    if CUSTOM_WALLS:
        graph = Graph(size, None, None)
        grid.initialize_grid(graph)
        started = False
        start_placed = None
        end_placed = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if started:
                    continue

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_grid_pos(pos, PIXEL_SIZE)
                    box = graph.grid[row][col]
                    if start_placed is None and box != 3:
                        graph.grid[row][col] = 2
                        grid.draw_start(graph, (row, col), start_placed)
                        start_placed = (row, col)
                    elif end_placed is None and box != 2:
                        graph.grid[row][col] = 3
                        grid.draw_end(graph, (row, col), end_placed)
                        end_placed = (row, col)
                    else:
                        if box != 2 and box != 3:
                            graph.grid[row][col] = 1
                            grid.draw_wall(graph, (row, col))

                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_grid_pos(pos, PIXEL_SIZE)
                    box = graph.grid[row][col]
                    if box == 2:
                        start_placed = None
                    if box == 3:
                        end_placed = None
                    if (row, col) not in graph.border:
                        grid.draw_undo(graph, (row, col))
                        graph.grid[row][col] = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not started and start_placed and end_placed:
                        print("Done")
                        running = False
                        graph.start = start_placed
                        graph.end = end_placed

    else:
        # Initialize a graph object, the graph object should be showing on the screen
        graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))
        populate_maze(graph, size)
        # populate_dirty(graph.grid, 100000, graph.size)
        graph.place_start_end()
        grid.initialize_grid(graph)
    # Create the start and end point onto the graph and start the solver
    # bidirection_bfs_solver(graph) #14.17,12.67
    a_star_solver(graph) #14.77