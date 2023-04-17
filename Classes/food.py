from numpy import random
import pygame
from Classes.constants import Constants, FoodDistribution


class Food:
    def __init__(self, x, y, energy, constants):
        self.x = x
        self.y = y
        self.size = constants.SCALE_FACTOR
        self.energy = energy

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.centerx = self.x
        rect.centery = self.y

        return rect


class FoodCreater:
    def __init__(self, constants):
        self.constants = constants
        self.food_distribution = self.constants.FOOD_DISTRIBUTION

    def get_food(self):
        if self.food_distribution == FoodDistribution.Full:
            return self.full_arena()
        elif self.food_distribution == FoodDistribution.Unfull_80:
            return self.unfull_arena(0.8)
        elif self.food_distribution == FoodDistribution.Unfull_60:
            return self.unfull_arena(0.6)
        elif self.food_distribution == FoodDistribution.Unfull_40:
            return self.unfull_arena(0.4)
        elif self.food_distribution == FoodDistribution.Unfull_20:
            return self.unfull_arena(0.2)
        elif self.food_distribution == FoodDistribution.Clusters:
            return self.clusters_arena()
        elif self.food_distribution == FoodDistribution.Corners:
            return self.corners_arena()
        elif self.food_distribution == FoodDistribution.Spiral:
            return self.spiral_arena()

    def full_arena(self):
        food_dict = dict()
        for x in range(0, self.constants.WORLD_WIDTH, self.constants.SCALE_FACTOR):
            for y in range(0, self.constants.WORLD_HEIGHT, self.constants.SCALE_FACTOR):
                if (x, y) != self.constants.START_POSITION:
                    food_dict[(x, y)] = Food(x, y, 1, self.constants)
        return food_dict

    def unfull_arena(self, percentage):
        random.seed(42)
        food_dict = dict()
        while len(food_dict) < self.constants.WORLD_SQUARES * percentage:
            x = round(random.randint(0, self.constants.WORLD_WIDTH) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
            y = round(random.randint(0, self.constants.WORLD_HEIGHT) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
            if (x, y) != self.constants.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.constants)

        return food_dict

    def corners_arena(self):
        pass
        food_dict = dict()
        corner1 = random.random()


    def clusters_arena(self):
        random.seed(42)
        food_dict = dict()
        while len(food_dict) < 0.2 * self.constants.WORLD_SQUARES:
            x = round(random.randint(0, self.constants.WORLD_WIDTH) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
            y = round(random.randint(0, self.constants.WORLD_HEIGHT) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
            if (x, y) not in food_dict:
                food_dict[(x, y)] = Food(x, y, 1, self.constants)
                for j in range(25):
                    dx = round(random.randint(-30, 30) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
                    dy = round(random.randint(-30, 30) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
                    while (x + dx, y + dy) in food_dict or x + dx < 0 or x + dx > 800 or y + dy < 0 or y + dy > 800:
                        dx = round(random.randint(-30, 30) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
                        dy = round(random.randint(-30, 30) / self.constants.SCALE_FACTOR) * self.constants.SCALE_FACTOR
                    x += dx
                    y += dy
                    food_dict[(x, y)] = Food(x, y, 1, self.constants)
        return food_dict

    def spiral_arena(self):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        number_of_points_in_direction = 1
        food_dict = dict()
        x, y = self.constants.START_POSITION
        food_dict[(x, y)] = Food(x, y, 1, self.constants)
        while True:
            for i in range(1, number_of_points_in_direction+1):
                x = x + (directions[(number_of_points_in_direction-1) % 4][0] * self.constants.SCALE_FACTOR)
                y = y + (directions[(number_of_points_in_direction-1) % 4][1] * self.constants.SCALE_FACTOR)
                if x > self.constants.WORLD_WIDTH or x < 0 or y > self.constants.WORLD_HEIGHT or y < 0:
                    return food_dict
                food_dict[(x, y)] = Food(x, y, 1, self.constants)
            number_of_points_in_direction += 1




