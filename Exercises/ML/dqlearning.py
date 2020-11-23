'''
Implenting Deep Q-learning using a tensorflow

The exercise is from GeeksForGeeks with the same title
'''

### Importing required libraries
import numpy is as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQAgent
from r.policy import EpsGreedyQPolicy
from r.memory import SequentialMemory

### Build the enviroment
enviroment_name = 'MountainCar-v0'
env = gym.make(enviroment_name)
np.random.seed(0)
env.seed(0)

# Extracting the number of possible actions
num_actions = env.action_space.n

### Building a learning agent
agent = Sequential()
agent.add(Flatten(input_shape =(1, ) + env.observation_space.shape))
agent.add(Dense(16))
agent.add(Activation('relu'))
agent.add(Dense(num_actions))
agent.add(Activation('linear'))

### Find the optimal strategy
strategy = EpsGreedyPolicy()
memory = SequentialMemory(limit = 10000, window_length = 1)
dqn = DQNAgent(model = agent, nb_actions = num_actions, memory = memory,
               nb_steps_warmup = 10)
target_model_update = (lr = 1e-2, policy = strategy)
fqn.compile(Adam(lr = 1e-3), metrics =['mae'])

# Visualize the training
dqn.fit(env, nb_steps = 5000, visualize = True, verbose = 2)

### Testing the learning agent
dqn.test(env, nb_episodes = 5, visualize=True)
