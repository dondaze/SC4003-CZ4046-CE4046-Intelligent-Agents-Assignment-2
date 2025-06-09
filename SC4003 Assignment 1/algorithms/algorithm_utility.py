import pygame
import matplotlib.pyplot as plt
import numpy as np
from config import *
from utils import *

# check if the state is a wall or out of bounds
def is_wall(s):
    return s in get_wall() or s[0] < 0 or s[0] >= get_maze_width() or s[1] < 0 or s[1] >= get_maze_height()

# calculate the next state utility based on the current state and action
def next_state_utility(env, s, a):
    # check if the current state is a wall
    if s in get_wall():
        return env[s[1]][s[0]]

    # calculate the next state based on the action
    new_x, new_y = s
    new_x += ACTIONS[a][0]
    new_y += ACTIONS[a][1]

    # check if the next state is a wall or out of bounds
    if is_wall((new_x, new_y)):
        return env[s[1]][s[0]]      # return the current state utility
    else:
        return env[new_y][new_x]    # return the next state utility

# calculate the expected utility of taking action 'a' in state 's'
# expected utility for state s and action a: EU(s, a) = Σ_s' P(s' | s, a) * U_i(s')
def expected_utility(env, s, a):
    # zero the expected utility
    exp_utility = 0
    # calculate the expected utility by looping through all possible next states
    # (according to the transition model)
    for action, prob in transition_model(a).items():
        exp_utility += prob * next_state_utility(env, s, action)
    return exp_utility

# draw the action arrows on the grid (using the symbols ←, →, ↑, ↓)
def draw_action(screen, action, x, y):
    # get the arrow image for each action
    arrow_img = pygame.image.load(get_path() + '/asset/' + action + '-arrow.png')
    arrow_img = pygame.transform.scale(arrow_img, (get_cell_width() // 2, get_cell_height() // 2))
    screen.blit(arrow_img, (x * get_cell_width() + get_cell_width() // 4, y * get_cell_height() + get_cell_height() // 4))

# set the text font and size
def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, get_cell_height() // 3)

    # set the label rectangle
    rect = pygame.Rect(x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height())

    # show the text label with the text centered on the cell
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# to visualize the environment
def visualize_env(env_name):
    pygame.init()       # initialize the visualization
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(WHITE)

    # loop through all the states in the environment
    for y in range(get_maze_height()):
        for x in range(get_maze_width()):
            # get the colour of the current state based on the utility
            colour = get_cell_colour((x, y))
            # draw a rectangle for the current state
            pygame.draw.rect(screen, colour, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()))
            # draw the grid lines
            pygame.draw.rect(screen, BLACK, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()), LINE_WIDTH)
            if (x, y) == get_start_position():
                text_content = 'Start'
            elif (x, y) in get_wall():
                text_content = 'Wall'
            elif (x, y) in get_grn_sq():
                text_content = str(get_grn_sq()[(x, y)])
                if int(text_content) > 0:
                    text_content = '+' + text_content
            elif (x, y) in get_brn_sq():
                text_content = str(get_brn_sq()[(x, y)])
            else:
                text_content = ''
        
            if text_content:
                draw_text(screen, text_content, x, y)

    font = pygame.font.Font(None, get_cell_height() // 3)   # set font size for labels

    # draw row labels
    for y in range(get_maze_height()):
        label = font.render(str(y), True, BLUE)
        screen.blit(label, (WINDOW_WIDTH - 50, y * get_cell_height() + get_cell_height() // 3 + 10))

    # draw column labels
    for x in range(get_maze_width()):
        label = font.render(str(x), True, RED)
        screen.blit(label, (x * get_cell_width() + get_cell_height() // 3 + 10, WINDOW_HEIGHT-30))

    pygame.display.flip()                                   # update the display

    # convert Pygame surface to array for Matplotlib
    img_data = pygame.surfarray.array3d(screen)
    img_data = img_data.transpose([1, 0, 2])                # transpose to match image shape

    # display with Matplotlib
    plt.imshow(img_data)
    plt.axis('off')             # hide axes
    plt.show()

    pygame.display.quit()       # close visualization
    pygame.quit()               # quit visualization

# visualize the policy
def visualize_policy(policy, policy_name):
    # initialize the visualization
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(WHITE)

    # loop through all the states in the environment
    for y in range(get_maze_height()):
        for x in range(get_maze_width()):
            # gete the color of the current state based on the utility
            colour = get_cell_colour((x, y))
            # draw a rectangle for the current state
            pygame.draw.rect(screen, colour, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()))
            # draw the grid lines
            pygame.draw.rect(screen, BLACK, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()), LINE_WIDTH)
            # check if the current state is not a wall
            if (x, y) in get_wall():
                text_content = "Wall"
                draw_text(screen, text_content, x, y)
            else:
                action = policy[y][x]                       # get the optimal action for the current state
                draw_action(screen, action, x, y)           # draw the optimal action on the screen

    font = pygame.font.Font(None, get_cell_height() // 3)   # set font size for labels

    # draw row labels
    for y in range(get_maze_height()):
        label = font.render(str(y), True, BLUE)
        screen.blit(label, (WINDOW_WIDTH - 50, y * get_cell_height() + get_cell_height() // 3 + 10))

    # draw column labels
    for x in range(get_maze_width()):
        label = font.render(str(x), True, RED)
        screen.blit(label, (x * get_cell_width() + get_cell_height() // 3 + 10, WINDOW_HEIGHT-30))

    pygame.display.flip()                                   # update the display

    # convert Pygame surface to array for Matplotlib
    img_data = pygame.surfarray.array3d(screen)
    img_data = img_data.transpose([1, 0, 2])                # transpose to match image shape

    # display with Matplotlib
    plt.imshow(img_data)
    plt.axis('off')             # hide axes
    plt.show()

    pygame.display.quit()       # close visualization
    pygame.quit()               # quit visualization

# Fto visualize the utility values
def visualize_utility(env, utility_name):
    # initialize the visualization
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(WHITE)

    # Loop through all the states in the environment
    for y in range(get_maze_height()):
        for x in range(get_maze_width()):
            # get the color of the current state based on the utility
            colour = get_cell_colour((x, y))
            # draw a rectangle for the current state
            pygame.draw.rect(screen, colour, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()))
            # draw the grid lines
            pygame.draw.rect(screen, BLACK, (x * get_cell_width(), y * get_cell_height(), get_cell_width(), get_cell_height()), LINE_WIDTH)
            if (x, y) in get_wall():
                text_content = "Wall"
                draw_text(screen, text_content, x, y)
            else:
                draw_text(screen, f'{env[y][x]:.4f}', x, y)  # add the utility value to the visualization

    font = pygame.font.Font(None, get_cell_height() // 3)    # set font size for labels

    # draw row labels
    for y in range(get_maze_height()):
        label = font.render(str(y), True, BLUE)
        screen.blit(label, (WINDOW_WIDTH - 50, y * get_cell_height() + get_cell_height() // 3 + 10))

    # draw column labels
    for x in range(get_maze_width()):
        label = font.render(str(x), True, RED)
        screen.blit(label, (x * get_cell_width() + get_cell_height() // 3 + 10, WINDOW_HEIGHT-30))
        
    pygame.display.flip()                                    # update the display

    # convert Pygame surface to array for Matplotlib
    img_data = pygame.surfarray.array3d(screen)
    img_data = img_data.transpose([1, 0, 2])                 # transpose to match image shape

    # display with Matplotlib
    plt.imshow(img_data)
    plt.axis('off')             # hide axes
    plt.show()

    pygame.display.quit()       # close visualization
    pygame.quit()               # quit visualization