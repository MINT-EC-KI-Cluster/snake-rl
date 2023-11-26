import pygame
from environment import World
import sys, os

pygame.init()

screen_width = 960
screen_height = 960
blockSize = 60


world = World()
snake_head = pygame.image.load('Art/SnakeHead.png')
snake_head = pygame.transform.scale(snake_head, (blockSize, blockSize))

snake_body = pygame.image.load('Art/SnakeBody.png')
snake_body = pygame.transform.scale(snake_body, (blockSize, blockSize))

fence = pygame.image.load('Art/fence.png')
fence = pygame.transform.scale(fence, (blockSize, blockSize))

light_blue_tile = pygame.image.load('Art/light_blue_tile.png')
light_blue_tile = pygame.transform.scale(light_blue_tile, (blockSize, blockSize))

dark_blue_tile = pygame.image.load('Art/dark_blue_tile.png')
dark_blue_tile = pygame.transform.scale(dark_blue_tile, (blockSize, blockSize))

apple = pygame.image.load('Art/apple.png')
apple = pygame.transform.scale(apple, (blockSize, blockSize))


screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface((screen_width, screen_height))
clock = pygame.time.Clock()
running = True


def drawGrid():
    grid = world.get_grid()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 1:
                background.blit(fence, (x * blockSize, y * blockSize))
            else:
                if ((x + y) % 2 == 0):
                    background.blit(light_blue_tile, (x * blockSize, y * blockSize))
                else:
                    background.blit(dark_blue_tile, (x * blockSize, y * blockSize))

def drawGame():
    screen.blit(background, (0, 0))
    
    grid = world.get_grid()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 9:
                screen.blit(snake_head, (x * blockSize, y * blockSize))
            elif grid[y][x] == 8:
                screen.blit(snake_body, (x * blockSize, y * blockSize))
            elif grid[y][x] == 2:
                screen.blit(apple, (x * blockSize, y * blockSize))
                
drawGrid()
input_queue = []
last_input = [1, 0]

time_to_update_world_ms = 200
update_world_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_world_event, time_to_update_world_ms)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                input_queue.append([-1, 0])
            elif event.key == pygame.K_RIGHT:
                input_queue.append([1, 0])
            elif event.key == pygame.K_UP:
                input_queue.append([0, -1])
            elif event.key == pygame.K_DOWN:
                input_queue.append([0, 1])
                
        # This event gets called when the frame gets updated
        if event.type == update_world_event:
            to_move = last_input
            if not len(input_queue) == 0:
                to_move = input_queue.pop()
                last_input = to_move
            
            
            if world.check_if_move_kills(to_move):
                pygame.quit()
                running = False
                break
            world.step(to_move)

            drawGame()
            pygame.display.flip()
            
    if not running:
        break
        
    clock.tick(60)  # limits FPS to 60
pygame.quit()