import os
import random
import networkModel as model
import numpy as np
from env import Env

# folders probably won't use but ok
mainFolder = os.path.dirname(__file__)

env = Env()
random.seed(None)
agent = model.DQNAgent(83, 5)
batch_size = 1024

# main game loop
for e in range(10000):
    state = env.reset()
    while True:
        action = agent.act(state)
        step = np.zeros(5)
        step[action] = 1
        next_state, reward, done = env.step(step)

        reward = reward if not done else -100
        if reward != 0:
            agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
        if len(agent.memory) > batch_size:
            loss = agent.replay(batch_size)

    if e % 500 is 0:
        print(f'done {e}')
    if e % 1000 is 0:
        agent.save(f'checkPoint{e}.h5')
        print(f'cp {e} done!')

agent.save('final.h5')
