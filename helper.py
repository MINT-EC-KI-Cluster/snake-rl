import pygame

def sum_arrays(arr1: list, arr2: list):
    arr3 = arr1.copy()
    for i in range(len(arr2)):
        arr3[i] += arr2[i]
    return arr3

def make_grid(grid_width: int, grid_height: int):
    grid = [0] * grid_height
    for i in range(len(grid)):
        grid[i] = [0] * grid_width
    grid[0] = [1] * grid_width
    grid[len(grid)-1] = [1] * grid_width
    for i in range(1, len(grid)-1):
        grid[i][0] = 1
        grid[i][len(grid[i])-1] = 1
    return grid

class GraphicsLoader:
    def __init__(self, blockSize: int):
        self.snake_head = pygame.image.load('Art/SnakeHead.png')
        self.snake_head = pygame.transform.scale(self.snake_head, (blockSize, blockSize))

        self.snake_body = pygame.image.load('Art/SnakeBody.png')
        self.snake_body = pygame.transform.scale(self.snake_body, (blockSize, blockSize))

        self.fence = pygame.image.load('Art/fence.png')
        self.fence = pygame.transform.scale(self.fence, (blockSize, blockSize))

        self.light_blue_tile = pygame.image.load('Art/light_blue_tile.png')
        self.light_blue_tile = pygame.transform.scale(self.light_blue_tile, (blockSize, blockSize))

        self.dark_blue_tile = pygame.image.load('Art/dark_blue_tile.png')
        self.dark_blue_tile = pygame.transform.scale(self.dark_blue_tile, (blockSize, blockSize))

        self.apple = pygame.image.load('Art/apple.png')
        self.apple = pygame.transform.scale(self.apple, (blockSize, blockSize))