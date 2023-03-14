from numpy import random
import pygame
from Simple.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH, INITIAL_AMOUNT_FOOD, START_POSITION,\
    FoodDistribution


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
        for x in range(0, WORLD_WIDTH, SCALE_FACTOR):
            for y in range(0, WORLD_HEIGHT, SCALE_FACTOR):
                if (x, y) == START_POSITION:
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

    def create_food_in_random_corner(water_rects):
        food_dict = dict()
        corner1 = random.random()
        corner2 = random.random()
        x_from = WORLD_WIDTH/2 if corner1 < 0.5 else 0
        x_to = WORLD_WIDTH if x_from == WORLD_WIDTH/2 else WORLD_WIDTH/2
        y_from = WORLD_HEIGHT/2 if corner2 < 0.5 else 0
        y_to = WORLD_HEIGHT if y_from == WORLD_WIDTH/2 else WORLD_HEIGHT/2
        for x in range(int(x_from), int(x_to+1), SCALE_FACTOR):
            for y in range(int(y_from), int(y_to+1), SCALE_FACTOR):
                food_dict[(x, y)] = Food(x, y, 1)
        return food_dict



    def create_food_in_circle(water_rects):
        import random
        import math
        food_dict = dict()
        circle_x = WORLD_WIDTH/2
        circle_y = WORLD_HEIGHT/2
        while len(food_dict) < 1:
            a = random.randint(0, 300) * 2 * math.pi
            r = 1 * math.sqrt(random.randint(0, 300))
            x = round((r * math.cos(a) + circle_x)/SCALE_FACTOR)*SCALE_FACTOR
            y = round((r * math.sin(a) + circle_y)/SCALE_FACTOR)*SCALE_FACTOR
            food_dict[(x, y)] = Food(x, y, 1)

        return food_dict

    def get_food_from_food_distribution(food_distribution):
        if food_distribution == FoodDistribution.Full:
            return Food.create_food([])

        elif food_distribution == FoodDistribution.Random:
            return Food.create_random_food([])

        elif food_distribution == FoodDistribution.Corner:
            return Food.create_food_in_random_corner([])

        elif food_distribution == FoodDistribution.Circle:
            return Food.create_food_in_circle([])

