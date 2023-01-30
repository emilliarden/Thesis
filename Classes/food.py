from numpy import random
import pygame
from Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH


class Food:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.size = SCALE_FACTOR if energy < 40 else SCALE_FACTOR*2
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.energy = energy

    def init_x_and_y(self):
        self.x = random.randint(0, WORLD_WIDTH)
        self.y = random.randint(0, WORLD_HEIGHT)

    def create_food(water_rects):
        food = []
        for x in range(10, WORLD_WIDTH - 10, SCALE_FACTOR):
            for y in range(10, WORLD_HEIGHT - 10, SCALE_FACTOR):
                food_rect = pygame.Rect(x, y, SCALE_FACTOR, SCALE_FACTOR)
                if food_rect.collidelist(water_rects) > -1:
                    continue
                else:
                    food.append(Food(x, y, 20))
        return food
