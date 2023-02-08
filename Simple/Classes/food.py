from numpy import random
import pygame
from Advanced.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH


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
        food_dict = dict()
        for x in range(0, WORLD_WIDTH, SCALE_FACTOR):
            for y in range(0, WORLD_HEIGHT, SCALE_FACTOR):
                if y == WORLD_HEIGHT/2:
                    continue
                food_dict[(x, y)] = Food(x, y, 1)
        return food_dict

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
