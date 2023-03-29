import random

import pygame
from enum import Enum

SCALE_FACTOR = 5
WORLD_HEIGHT = 800
WORLD_WIDTH = 800
WORLD_SQUARES = WORLD_WIDTH/SCALE_FACTOR*WORLD_HEIGHT/SCALE_FACTOR
WATER_COLOR = (0, 157, 196)
FOOD_COLOR = (0, 154, 23)
FOOD2_COLOR = (195, 0, 195)
TEXT_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (255, 255, 255)
INITIAL_POPULATION_SIZE = 10
INITIAL_AMOUNT_FOOD = WORLD_SQUARES*0.8
SENSING_DISTANCE = 3
START_POSITION = (0, 0)

class FoodDistribution(Enum):
    Full = 1
    Random = 2
    Corner = 3
    Circle = 4

class StartMode(Enum):
    New = 1
    Checkpoint = 2
    Winner = 3

class SensingMode(Enum):
    Box = 1
    Cross = 2
    Pyramid = 3

def get_number_of_inputs(sensing_mode):
    number_of_inputs = 0
    if sensing_mode == SensingMode.Box:
        for i in range(1, SENSING_DISTANCE+1):
            number_of_inputs += (i * 8)
    elif sensing_mode == SensingMode.Cross:
        number_of_inputs = (4*SENSING_DISTANCE)
    elif sensing_mode == SensingMode.Pyramid:
        if SENSING_DISTANCE == 4:
            number_of_inputs = 40
        elif SENSING_DISTANCE == 3:
            number_of_inputs = 24
        elif SENSING_DISTANCE == 2:
            number_of_inputs = 12
        elif SENSING_DISTANCE == 1:
            number_of_inputs = 4

    # +2 for own coordinates
    return number_of_inputs + 2
