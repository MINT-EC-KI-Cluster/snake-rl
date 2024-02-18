import random
import pygame
import helper
from enum import Enum

class Direction(Enum):
    LEFT = 0
    FORWARD = 1
    RIGHT = 2

class World:
    # 1 is a wall
    # 9 is the snake head
    # 8 is the snake body
    # 0 is an empty space
    # 2 is food
    screen_width = 960
    screen_height = 960
    blockSize = 60
    frame_rate = 60

    
    def __init__(self):
        pygame.init()

        self.graphics_loader = helper.GraphicsLoader(World.blockSize)

        self.screen = pygame.display.set_mode((World.screen_width, World.screen_height))
        self.background = pygame.Surface((World.screen_width, World.screen_height))
        self.clock = pygame.time.Clock()
        
        self.grid_width = int(World.screen_width / World.blockSize)
        self.grid_height = int(World.screen_height / World.blockSize)
        
        self.grid = helper.make_grid(self.grid_width, self.grid_height)
        self.snake = World.Snake([int(self.grid_width / 2), int(self.grid_height / 2)])
        self.foods = [self.rand_unoccupied_pos()]
        self.grid[self.foods[0][1]][self.foods[0][0]] = 2
        self.score = 0
        self.curr_frame = 0

        self.draw_grid()
    
    def rand_unoccupied_pos(self):
        rand_y, rand_x = (0, 0)
        while self.grid[rand_y][rand_x] != 0:
            rand_y = random.randint(0, len(self.grid)-1)
            rand_x = random.randint(0, len(self.grid[rand_y])-1)
        return [rand_x, rand_y]
    
    def init_new_food(self):
        pos = self.rand_unoccupied_pos()
        self.grid[pos[1]][pos[0]] = 2
        self.foods.append(pos)
    
    def step(self, input_orientation: list):
        if (input_orientation[0] == 1):
            input_orientation = Direction.LEFT
        elif (input_orientation[1] == 1):
            input_orientation = Direction.FORWARD
        elif (input_orientation[2] == 1):
            input_orientation = Direction.RIGHT

        # 1. grab all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        reward = 0
        game_over = False
        # 2. check if lost
        if self.danger_in_direction(input_orientation) == 1 or self.curr_frame > (100 * (self.score + 1)):
            reward = -10
            game_over = True
            return reward, game_over, self.score

        # 3. move
        self.grid = self.snake.move(input_orientation, self.grid)
        self.curr_frame += 1

        # 4. check for apple
        for i in range(len(self.foods)):
            if self.grid[self.foods[i][1]][self.foods[i][0]] == 9:
                self.score += 1
                reward += 10
                self.foods.pop(i)
                self.init_new_food()
        
        # 5. update ui
        self.update_ui()
        self.clock.tick(World.frame_rate)    

        # 6. return reward 
        return reward, game_over, self.score 

    def reset(self):
        self.grid = helper.make_grid(self.grid_width, self.grid_height)
        self.snake = World.Snake([int(self.grid_width / 2), int(self.grid_height / 2)])
        self.foods = [self.rand_unoccupied_pos()]
        self.grid[self.foods[0][1]][self.foods[0][0]] = 2
        self.score = 0
        self.curr_frame = 0
    
    def danger_in_direction(self, direction: Direction):
        orientation = self.snake.get_new_orientation(direction)
        curr_pos = helper.sum_arrays(self.snake.head.pos, orientation)
        distance = 1
        while self.grid[curr_pos[1]][curr_pos[0]] == 0 or self.grid[curr_pos[1]][curr_pos[0]] == 2:
            distance += 1
            curr_pos = helper.sum_arrays(curr_pos, orientation)
        return distance
    
    def print_grid(self):
        for i in self.grid:
            print(str(i) + "\n")
    
    def get_grid(self):
        return self.grid
    
    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    self.background.blit(self.graphics_loader.fence, (x * World.blockSize, y * World.blockSize))
                else:
                    if ((x + y) % 2 == 0):
                        self.background.blit(self.graphics_loader.light_blue_tile, (x * World.blockSize, y * World.blockSize))
                    else:
                        self.background.blit(self.graphics_loader.dark_blue_tile, (x * World.blockSize, y * World.blockSize))
    
    def update_ui(self):
        self.screen.blit(self.background, (0, 0))
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 9:
                    self.screen.blit(self.graphics_loader.snake_head, (x * World.blockSize, y * World.blockSize))
                elif self.grid[y][x] == 8:
                    self.screen.blit(self.graphics_loader.snake_body, (x * World.blockSize, y * World.blockSize))
                elif self.grid[y][x] == 2:
                    self.screen.blit(self.graphics_loader.apple, (x * World.blockSize, y * World.blockSize))
        pygame.display.flip()

            
    class Snake:
        def __init__(self, start_pos: list):
            self.head = self.Node(None, start_pos)
            self.orientation = [1, 0]
        
        def get_new_orientation(self, input: Direction):
            orientation = [self.orientation[0], self.orientation[1]]
            if (input == Direction.RIGHT):
                # Turn Right
                y = orientation[1] * -1
                orientation[1] = orientation[0]
                orientation[0] = y
            elif (input == Direction.LEFT):
                # Turn Left
                x = orientation[0] * -1
                orientation[0] = orientation[1]
                orientation[1] = x
            return orientation

        def move(self, input: Direction, grid: list):
            self.orientation = self.get_new_orientation(input)
                
            new_head_pos = helper.sum_arrays(self.head.pos, self.orientation)
            
            if grid[new_head_pos[1]][new_head_pos[0]] == 2:
                # The snake grows when getting food, so we can just add the head and be done
                self.head = self.Node(self.head, new_head_pos)
            else:
                # Set tail pos to 0 as the node travels away
                tail_pos = self.head.last_node().pos
                grid[tail_pos[1]][tail_pos[0]] = 0
                
                # Update positions of snake nodes
                n = self.head
                last_pos = 0
                while n != None:
                    last_pos = n.pos
                    n.pos = new_head_pos
                    new_head_pos = last_pos
                    n = n.next_node
            
            # Overwrite digits in grid representing snake 
            n = self.head
            grid[n.pos[1]][n.pos[0]] = 9
            n = n.next_node
            while n != None:
                grid[n.pos[1]][n.pos[0]] = 8
                n = n.next_node
            
            return grid

        class Node:
            def __init__(self, next_node=None, pos=[]):
                self.next_node = next_node
                self.pos = pos
            
            def last_node(self):
                n = self
                while n.next_node != None:
                    n = n.next_node
                return n