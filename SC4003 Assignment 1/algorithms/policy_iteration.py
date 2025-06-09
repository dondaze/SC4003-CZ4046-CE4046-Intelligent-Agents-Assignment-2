import pandas as pd
import random
import os
import warnings
from config import *
from utils import *
from algorithms.algorithm_utility import *

# suppress futurewarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# set a seed for reproducibility
random.seed(42)

# initialize the policy iteration maze environment
def init_pi_env():
    # create a maze matrix filled with zeros
    pi_env = [[0 for _ in range(get_maze_width())] for _ in range(get_maze_height())]
    # initialize a maze matrix filled with random actions
    pi_policy = [[random.choice(list(ACTIONS.keys())) for _ in range(get_maze_width())] for _ in range(get_maze_height())]
    # return the environment and the policy matrices
    return pi_env, pi_policy

# Bellman equation used for policy iteration
def bellman_equation_pi(vi_env, s, action):
    # check the current state and assign the corresponding reward
    if s in get_grn_sq():       # green square rewards
        reward = get_grn_sq()[s]
    elif s in get_brn_sq():     # brown square rewards
        reward = get_brn_sq()[s]
    elif s in get_wall():       # wall has no reward
        reward = 0
    else:                       # white square rewards
        reward = get_wht_sq_reward()

    # calculate the expected utility of taking action 'action' in state 's'
    utility = expected_utility(vi_env, s, action)

    # return the Bellman equation result
    return reward + (GAMMA * utility)

# perform policy evaluation
def policy_evaluation(pi_env, pi_policy, iteration, results_csv_name):
    
    # iterate until the error is smaller than the tolerance threshold
    while True:
        new_pi_env = copy_env(pi_env)   # create a new environment copy to store the updated utilities
        error = 0                       # initialize the error
        
        # loop through all the states in the environment
        for y in range(get_maze_height()):
            for x in range(get_maze_width()):
                # calculate the Bellman equation result for the current state and action
                new_pi_env[y][x] = bellman_equation_pi(pi_env, (x, y), pi_policy[y][x])
                # update the error with the difference between the new and old utility
                error = max(error, abs(new_pi_env[y][x] - pi_env[y][x]))

        pi_env = new_pi_env             # update the environment with the new utilities
        
        if error < THRESHOLD:           # stop when the error is smaller than the threshold
            break

    # check if folder exists otherwise create it
    folder_path = "result/policy_iteration/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # save the results to a csv file
    if iteration > 1:
        pi_results = pd.read_csv(get_path() + '/result/policy_iteration/' + f'{results_csv_name}.csv')
    else:
        pi_results = pd.DataFrame(columns=['Iteration', 'x', 'y', 'Utility'])

    for y in range(get_maze_height()):
        for x in range(get_maze_width()):
            new_vi_result = pd.DataFrame({'Iteration': [iteration], 'x': [x], 'y': [y], 'Utility': [pi_env[y][x]]})
            pi_results = pd.concat([pi_results, new_vi_result], ignore_index=True)

    pi_results.to_csv(get_path() + '/result/policy_iteration/' + f'{results_csv_name}.csv', index=False)

    return pi_env                      # return the updated environment

# perform policy iteration
def policy_iteration(pi_env, pi_policy, results_csv_name='pi_results'):
    iteration_cnt = 0       # initialize the iteration counter to 0
    
    while True:
        # increment the iteration counter for each iteration
        iteration_cnt += 1
        # perform policy evaluation
        new_pi_env = policy_evaluation(pi_env, pi_policy, iteration_cnt, results_csv_name)
        # initialize the policy_stable flag to True and check if the policy has converged
        policy_stable = True
        
        # loop through all the states in the environment
        for y in range(get_maze_height()):
            for x in range(get_maze_width()):
                old_action = pi_policy[y][x]    # store the old action
                max_utility = float('-inf')
                best_action = None     

                # loop through all possible actions
                for action in ACTIONS:
                    # calculate the Bellman equation result for the current state and action
                    utility = bellman_equation_pi(new_pi_env, (x, y), action)
                    # if the utility is greater than the maximum utility, update the maximum utility and the best action
                    if utility > max_utility:
                        max_utility = utility
                        best_action = action
                
                pi_env[y][x] = max_utility      # update the environment with the Bellman equation result
                pi_policy[y][x] = best_action   # update the policy with the best action

                # if the old action is different from the best action, set the policy_stable flag to False
                if old_action != best_action:
                    policy_stable = False

        if policy_stable:                       # stop when the policy has converged
            break

    return pi_env, pi_policy, iteration_cnt     # return the updated environment, policy and the iteration counter
