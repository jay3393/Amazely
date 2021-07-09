import pygame
import sys

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Breadth First Search Visualizer")


RED = (255, 0, 0) # Starting Node
WHITE = (255, 255, 255) # Wall Node
BLACK = (0, 0, 0) # Empty Node
YELLOW = (255, 255, 0) # End Node
GREY = (128, 128, 128) # Visited Node
DARKGREY = (100, 100, 100) # Next Node
BLUE = (0, 0, 255) #Backtrack Node
GREEN = (0, 255, 0)
GREEN2 = (0, 125, 0)
PURPLE = (225, 0, 225)
PURPLE2 = (125, 0, 125)

WIN.fill(BLACK)

def drawGrid3(grid, coord):
    blockSize = int(WIDTH / grid.size)  # Set the size of the grid block
    xi = coord[0]
    yi = coord[1]
    x = xi * blockSize
    y = yi * blockSize

    rect = pygame.Rect(x, y, blockSize, blockSize)
    pygame.draw.rect(WIN, GREEN, rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

def drawGrid2(grid, coord, distance):
    blockSize = int(WIDTH / grid.size)  # Set the size of the grid block
    xi = coord[0]
    yi = coord[1]
    x = xi * blockSize
    y = yi * blockSize
    blue = min(int(distance/117), 255)
    red = 255 - blue

    rect = pygame.Rect(x, y, blockSize, blockSize)
    pygame.draw.rect(WIN, (red, 0, blue), rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

def initialize_grid(grid):
    blockSize = int(WIDTH/grid.size) #Set the size of the grid block
    for x in range(0, WIDTH, blockSize):
        for y in range(0, WIDTH, blockSize):
            xi = int(x/blockSize)
            yi = int(y/blockSize)
            if grid.grid[yi][xi] == 0:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(WIN, DARKGREY, rect)
            if grid.grid[yi][xi] == 1:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(WIN, BLACK, rect)
            if grid.grid[yi][xi] == 2:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(WIN, YELLOW, rect)
            if grid.grid[yi][xi] == 3:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(WIN, RED, rect)
    pygame.display.update()

# while True:
#         drawGrid(grid)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         pygame.display.update()

