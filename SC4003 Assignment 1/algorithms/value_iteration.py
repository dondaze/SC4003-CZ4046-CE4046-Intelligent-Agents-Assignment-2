import pandas as pd
import os
from config import *
from utils import *
from algorithms.algorithm_utility import *

# initialize the value iteration maze environment
def init_vi_env():
    # grid matrix filled with zeros
    vi_env = [[0 for _ in range(get_maze_width())] for _ in range(get_maze_height())]
    return vi_env

# Bellman equation used for value iteration
def bellman_equation_vi(vi_env, s):
    # check the current state rewards
    if s in get_grn_sq():           # green square rewards
        reward = get_grn_sq()[s]
    elif s in get_brn_sq():         # brown square rewards
        reward = get_brn_sq()[s]
    elif s in get_wall():           # wall has no reward
        reward = 0
    else:                           # white square rewards
        reward = get_wht_sq_reward()

    max_utility = float('-inf')     # set the maximum utility
    best_action = None              # set the best action
    
    # loop through all possible actions
    for action in ACTIONS:
        # calculate the expected utility of taking action the current action in the current state
        utility = expected_utility(vi_env, s, action)
        # if the utility is greater than the maximum utility, update the maximum utility and the best action
        if utility > max_utility:
            max_utility = utility
            best_action = action

    # return the Bellman equation result and the best action
    return (reward + GAMMA * max_utility), best_action

# perform value iteration
def value_iteration(vi_env, results_csv_name='vi_results'):
    vi_results_list = []    # store the value iteration results
    iteration_cnt = 0       # initialize the iteration counter to 0

    # iterate until the error is smaller than the tolerance threshold
    while True:
        iteration_cnt += 1              # increment the iteration counter for each iteration
        new_vi_env = copy_env(vi_env)   # create a new environment copy to store the updated utilities
        error = 0                       # initialize the error

        # loop through all the states in the environment
        for y in range(get_maze_height()):
            for x in range(get_maze_width()):
                # calculate the Bellman equation result and the best action for the current state
                max_utility, best_action = bellman_equation_vi(vi_env, (x, y))
                # update the new environment with the Bellman equation result
                new_vi_env[y][x] = max_utility
                # update the error if the difference between the new and old utility is greater than the current error
                error = max(error, abs(max_utility - vi_env[y][x]))

                # add to the results
                vi_results_list.append({'Iteration': iteration_cnt, 'x': x, 'y': y, 'Utility': max_utility})

        vi_env = new_vi_env                             # update the environment with the new environment

        if error < THRESHOLD * (1 - GAMMA) / GAMMA:     # stop when the error is smaller than the threshold
            break

    # check if folder exists otherwise create it
    folder_path = "result/value_iteration/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # save the results to a csv file
    vi_results = pd.DataFrame(vi_results_list)
    vi_results.to_csv(get_path() + '/result/value_iteration/' + f'{results_csv_name}.csv', index=False)

    return vi_env, iteration_cnt                       # return the updated environment and the iteration counter

# generate the optimal policy based on the value iteration results
def generate_policy(vi_env):
    # create a matrix to store the optimal policies for each state
    policy = [[None for _ in range(get_maze_width())] for _ in range(get_maze_height())]
    
    # loop through all the states in the environment
    for y in range(get_maze_height()):
        for x in range(get_maze_width()):
            max_utility = float('-inf')     # set the maximum utility
            best_action = None

            # loop through all the possible actions
            for action in ACTIONS:
                # calculate the expected utility of taking the current action in the current state
                utility = expected_utility(vi_env, (x, y), action)
                # if the utility is greater than the maximum utility, update the maximum utility and the best action
                if utility > max_utility:
                    max_utility = utility
                    best_action = action
            # update the policy with the best action for the current state
            policy[y][x] = best_action
    
    return policy       # return the optimal policyS