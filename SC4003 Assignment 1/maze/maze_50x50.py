import random

# for reproducibility
SEED = 50
random.seed(SEED)

# maze size
MAZE_WIDTH  = 50
MAZE_HEIGHT = 50

all_cells = [(x, y) for x in range(MAZE_WIDTH) for y in range(MAZE_HEIGHT)]

# ranges for the number of green, brown, and wall square
max_cells  = len(all_cells)
num_green = random.randint(50, int(max_cells * 0.25))    # max 25% of cells
num_brown = random.randint(50, int(max_cells * 0.25))    # max 25% of cells
num_wall  = random.randint(50, int(max_cells * 0.25))    # max 25% of cells

# ensure the start position is unique
start_pos       = random.choice(all_cells)
available_cells = set(all_cells) - {start_pos}

# sample random positions
grn_sq           = set(random.sample(list(available_cells), num_green))
available_cells -= grn_sq

brn_sq           = set(random.sample(list(available_cells), num_brown))
available_cells -= brn_sq

wall             = set(random.sample(list(available_cells), num_wall))

# assign rewards
GRN_SQ        = {cell:  1 for cell in grn_sq}
BRN_SQ        = {cell: -1 for cell in brn_sq}
WALL          = wall
START_POS     = start_pos
WHT_SQ_REWARD = -0.05