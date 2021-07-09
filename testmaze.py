import Graph
import grid
import random
import pygame

if __name__ == '__main__':
    while True:
        size = int(grid.WIDTH/2)
        graph = Graph(size, (random.randrange(1, size - 1), random.randrange(1, size - 1)), (random.randrange(1, size - 1), random.randrange(1, size - 1)))
        Graph.populate_dirty(graph.grid, grid.WIDTH * int(grid.WIDTH/8), size)
        grid.initialize_grid(graph)


        pygame.display.update()