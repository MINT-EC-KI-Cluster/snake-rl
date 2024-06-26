import torch
from collections import deque
from model import Linear_QNet, QTrainer
import environment
import numpy as np
import random

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent():
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # TODO
    def get_state(game: environment.World):
        state = [
            # current direction
            game.snake.orientation[0] == -1,  
            game.snake.orientation[0] == 1,
            game.snake.orientation[1] == 1,
            game.snake.orientation[1] == -1,

            # danger ahead
            game.danger_in_direction(environment.Direction.LEFT) == 1,
            game.danger_in_direction(environment.Direction.FORWARD) == 1,
            game.danger_in_direction(environment.Direction.RIGHT) == 1,

            # food pos
            game.foods[0][0] < game.snake.head.pos[0], # food left
            game.foods[0][0] > game.snake.head.pos[0], # food right
            game.foods[0][1] < game.snake.head.pos[1], # food above
            game.foods[0][1] > game.snake.head.pos[1], # food below
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    total_score = 0
    record = 0
    agent = Agent()
    game = environment.World()
    while True:
        # get old state
        state_old = Agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.step(final_move)
        state_new = Agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, print result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)


if __name__ == '__main__':
    train()