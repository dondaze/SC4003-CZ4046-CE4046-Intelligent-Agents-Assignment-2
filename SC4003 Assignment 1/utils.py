import pygame
import time
import os
from config import *

# get the current path
def get_path():
    return os.path.dirname(os.path.abspath(__file__))

# check if folder exists otherwise create it
def check_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)

# return a copy of an environment
def copy_env(env):
    return [[env[y][x] for x in range(get_maze_width())] for y in range(get_maze_height())]

# close the event
def force_close_pygame_window():
    quit_event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(quit_event)