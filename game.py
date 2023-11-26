import random
import pygame
import numpy as np

class World:
    # 1 is a wall
    # 9 is the snake head
    # 8 is the snake body
    # 0 is an empty space
    # 2 is food
    
    def __init__(self):
        self.grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.snake = self.Snake([1, 1])
        self.foods = [self.rand_unoccupied_pos()]
        self.grid[self.foods[0][1]][self.foods[0][0]] = 2
        self.points = 0
    
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
    
    def step(self, input_orientation):
        self.grid = self.snake.move(input_orientation, self.grid)
        for i in range(len(self.foods)):
            if self.grid[self.foods[i][1]][self.foods[i][0]] == 9:
                self.points += 1
                self.foods.pop(i)
                self.init_new_food()
    
    # METHOD IS NOT FINAL -> WILL BE REMOVED AND REPLACED WITH STATES
    def check_if_move_kills(self, input_orientation):
        return self.snake.check_if_move_kills(input_orientation, self.grid)
    
    def print_grid(self):
        for i in self.grid:
            print(str(i) + "\n")
    
    def get_grid(self):
        return self.grid
                
    
            
    class Snake:
        def __init__(self, start_pos):
            self.head = self.Node(None, start_pos)
            self.orientation = [1, 0]
        
        def move(self, input_orientation, grid):
            # Don't go back, to where you came from
            if not np.array_equal(np.array(input_orientation), np.array(self.orientation) * -1):
                self.orientation = input_orientation
                
            new_head_pos = np.array(self.head.pos) + np.array(self.orientation)
            
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
        
        
        # METHOD IS NOT FINAL -> WILL BE REMOVED AND REPLACED WITH STATES
        def check_if_move_kills(self, input_orientation, grid):
            # Don't go back, to where you came from
            if not np.array_equal(np.array(input_orientation), np.array(self.orientation) * -1):
                self.orientation = input_orientation
                
            new_head_pos = np.array(self.head.pos) + np.array(self.orientation)
            new_pos = grid[new_head_pos[1]][new_head_pos[0]]
            if new_pos == 1 or new_pos == 8:
                return True
            return False
        
        class Node:
            def __init__(self, next_node=None, pos=[]):
                self.next_node = next_node
                self.pos = pos
            
            def last_node(self):
                n = self
                while n.next_node != None:
                    n = n.next_node
                return n