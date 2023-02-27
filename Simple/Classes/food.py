from numpy import random
import pygame
from Simple.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH, INITIAL_AMOUNT_FOOD


class Food:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.size = SCALE_FACTOR
        self.energy = energy

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, SCALE_FACTOR, SCALE_FACTOR)
        rect.centerx = self.x
        rect.centery = self.y
        return rect


    def create_food(water_rects):
        food_dict = dict()
        for x in range(0, WORLD_WIDTH+1, SCALE_FACTOR):
            for y in range(0, WORLD_HEIGHT+1, SCALE_FACTOR):
                if y == WORLD_HEIGHT/2:
                    continue
                food_dict[(x, y)] = Food(x, y, 1)
        return food_dict

    def create_random_food(water_rects):
        food_dict = dict()
        while len(food_dict) < INITIAL_AMOUNT_FOOD:
            x = round(random.randint(0, WORLD_WIDTH) / SCALE_FACTOR) * SCALE_FACTOR
            y = round(random.randint(0, WORLD_HEIGHT) / SCALE_FACTOR) * SCALE_FACTOR
            food_dict[(x, y)] = Food(x, y, 1)
        return food_dict
