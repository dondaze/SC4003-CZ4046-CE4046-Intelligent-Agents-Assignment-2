# green square locations with rewards +1
GRN_SQ    = {(0, 0): +1, (2, 0): +1, (5, 0): +1,
             (3, 1): +1, (4, 2): +1, (5, 3): +1}

# brown square locations with rewards -1
BRN_SQ    = {(1, 1): -1, (5, 1): -1, (2, 2): -1,
             (3, 3): -1, (4, 4): -1}

# wall locations
WALL      = {(1, 0), (4, 1), (1, 4), (2, 4), (3, 4)}

# starting position
START_POS = (2, 3)

# maze size
MAZE_WIDTH  = 6
MAZE_HEIGHT = 6

# white square rewards -0.05
WHT_SQ_REWARD = -0.05