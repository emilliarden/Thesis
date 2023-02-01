from numpy import random
import pygame
from Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH


class Food:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.size = SCALE_FACTOR
        self.energy = energy

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, SCALE_FACTOR, SCALE_FACTOR)
        return rect


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

    def create_random_food(water_rects, amountOfFood):
        food = []
        for _ in range(amountOfFood):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(0, WORLD_HEIGHT)
            food_rect = pygame.Rect(x, y, SCALE_FACTOR, SCALE_FACTOR)
            if food_rect.collidelist(water_rects) > -1:
                continue
            else:
                food.append(Food(x, y, 20))
        return food
