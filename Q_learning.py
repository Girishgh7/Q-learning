import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import random
import numpy as np
import matplotlib.pyplot as plt
import gym

env = gym.make('Taxi-v3')

alpha = 0.9
gamma = 0.95
epsilon = 0.1
epsilon_decay = 0.9995
min_epsilon = 0.01
num_episodes = 100000
max_steps = 200

# 5x5 grid, 500 different states, 4 directions, 4 different locations, 1 passenger, 1 destination
q_table = np.zeros((env.observation_space.n, env.action_space.n))

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[state])

for episode in range(num_episodes):
    state, _ = env.reset()
    done = False

    for step in range(max_steps):
        action = choose_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        
        done = terminated or truncated
        
        # Update Q-table
        q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state, action])
        
        state = next_state
        
        if done:
            break

    # Decay epsilon
    epsilon = max(epsilon * epsilon_decay, min_epsilon)

# Render the environment for a few episodes
env = gym.make('Taxi-v3', render_mode='human')

for episode in range(10):
    state, _ = env.reset()
    done = False
    print("Episode number:", episode)
    
    for step in range(max_steps):
        action = np.argmax(q_table[state])
        next_state, reward, terminated, truncated, _ = env.step(action)
        env.render()
        state = next_state
        
        if terminated or truncated:
            env.render()
            print("Episode finished after {} steps".format(step))
            break

env.close()