import pygame
from enum import Enum

SCALE_FACTOR = 20
WORLD_HEIGHT = 800
WORLD_WIDTH = 800
WORLD_SQUARES = WORLD_WIDTH/SCALE_FACTOR*WORLD_HEIGHT/SCALE_FACTOR
WATER_COLOR = (0, 157, 196)
FOOD_COLOR = (0, 154, 23)
FOOD2_COLOR = (195, 0, 195)
TEXT_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (255, 255, 255)
INITIAL_POPULATION_SIZE = 10
INITIAL_AMOUNT_FOOD = 1400
SENSING_DISTANCE = 5
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



