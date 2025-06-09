import maze.given      as given_maze
import maze.maze_10x10 as maze_10x10_maze
import maze.maze_50x50 as maze_50x50_maze
import maze.maze_70x70 as maze_70x70_maze
from maze import *

# maze grid setup
GRID_WIDTH, GRID_HEIGHT = 720, 720           # maze grid size
WINDOW_WIDTH            = GRID_WIDTH  + 80   # total window width
WINDOW_HEIGHT           = GRID_HEIGHT + 50   # total window height
LINE_WIDTH              = 1                  # grid line width

# colours
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
BROWN = (255, 165, 0)
GREEN = (0, 255, 0)
GREY  = (128, 128, 128)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

# get the colour of the cell
def get_cell_colour(pos):
    if pos in GRN_SQ:
        return GREEN
    elif pos in BRN_SQ:
        return BROWN
    elif pos in WALL:
        return GREY
    else:
        return WHITE

# initialize the maze type
MAZE_TYPE = ''

# get the maze type values
def get_cell_width():
    return GRID_WIDTH // MAZE_WIDTH

def get_cell_height():
    return GRID_HEIGHT // MAZE_HEIGHT

def get_grn_sq():
    return GRN_SQ

def get_brn_sq():
    return BRN_SQ

def get_wall():
    return WALL

def get_start_position():
    return START_POS

def get_maze_height():
    return MAZE_HEIGHT

def get_maze_width():
    return MAZE_WIDTH

def get_wht_sq_reward():
    return WHT_SQ_REWARD

def set_maze_type(maze_type):
    global MAZE_TYPE, GRN_SQ, BRN_SQ, WALL, START_POS, MAZE_WIDTH, MAZE_HEIGHT, WHT_SQ_REWARD
    MAZE_TYPE = maze_type
    if MAZE_TYPE == 'given':
        GRN_SQ        = given_maze.GRN_SQ
        BRN_SQ        = given_maze.BRN_SQ
        WALL          = given_maze.WALL
        START_POS     = given_maze.START_POS
        MAZE_WIDTH    = given_maze.MAZE_WIDTH
        MAZE_HEIGHT   = given_maze.MAZE_HEIGHT
        WHT_SQ_REWARD = given_maze.WHT_SQ_REWARD
    elif MAZE_TYPE == 'maze_10x10':
        GRN_SQ        = maze_10x10_maze.GRN_SQ
        BRN_SQ        = maze_10x10_maze.BRN_SQ
        WALL          = maze_10x10_maze.WALL
        START_POS     = maze_10x10_maze.START_POS
        MAZE_WIDTH    = maze_10x10_maze.MAZE_WIDTH
        MAZE_HEIGHT   = maze_10x10_maze.MAZE_HEIGHT
        WHT_SQ_REWARD = maze_10x10_maze.WHT_SQ_REWARD
    elif MAZE_TYPE == 'maze_50x50':
        GRN_SQ        = maze_50x50_maze.GRN_SQ
        BRN_SQ        = maze_50x50_maze.BRN_SQ
        WALL          = maze_50x50_maze.WALL
        START_POS     = maze_50x50_maze.START_POS
        MAZE_WIDTH    = maze_50x50_maze.MAZE_WIDTH
        MAZE_HEIGHT   = maze_50x50_maze.MAZE_HEIGHT
        WHT_SQ_REWARD = maze_50x50_maze.WHT_SQ_REWARD
    elif MAZE_TYPE == 'maze_70x70':
        GRN_SQ        = maze_70x70_maze.GRN_SQ
        BRN_SQ        = maze_70x70_maze.BRN_SQ
        WALL          = maze_70x70_maze.WALL
        START_POS     = maze_70x70_maze.START_POS
        MAZE_WIDTH    = maze_70x70_maze.MAZE_WIDTH
        MAZE_HEIGHT   = maze_70x70_maze.MAZE_HEIGHT
        WHT_SQ_REWARD = maze_70x70_maze.WHT_SQ_REWARD

# set the maze type values
set_maze_type(MAZE_TYPE)

# button actions
ACTIONS = {'up'   : (0, -1),
           'right': (1, 0),
           'down' : (0, 1),
           'left' : (-1, 0)}

# set discount factor 0.99
GAMMA = 0.99

# transition model
def transition_model(a):
    a_index = list(ACTIONS.keys()).index(a)
    left_a   = list(ACTIONS.keys())[(a_index - 1) % len(ACTIONS)]
    right_a  = list(ACTIONS.keys())[(a_index + 1) % len(ACTIONS)]
    return {left_a: 0.1, a: 0.8, right_a: 0.1}      # return actions and their probabilities

# setting for value iteration algorithm
R_MAX = 1               # maximum reward
C = 0.1                 # cost function
EPSILON = C * R_MAX     # calculate the epsilon
THRESHOLD = EPSILON * (1 - GAMMA) / GAMMA