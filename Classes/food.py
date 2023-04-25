from numpy import random
from enum import Enum
import pygame


class FoodDistribution(Enum):
    Full = 1
    Unfull_80 = 2
    Unfull_60 = 3
    Unfull_40 = 4
    Unfull_20 = 5
    Corners = 6
    Clusters = 7
    Circle = 8
    Spiral = 9
    Water = 10
    CornersWithWater = 11
    Unfull_80_Water = 12
    Unfull_60_Water = 13
    Unfull_40_Water = 14
    Unfull_20_Water = 15
    Cross = 16
    SpiralWithWater = 17
    HalfWater = 18
    HalfWaterHalfFood = 19
    HalfFull = 20
class Food:
    def __init__(self, x, y, energy, scale_factor):
        self.x = x
        self.y = y
        self.size = scale_factor
        self.energy = energy

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.centerx = self.x
        rect.centery = self.y

        return rect


class FoodCreater:
    def __init__(self, food_distribution, start_position, world_width, world_height, scale_factor, world_squares):
        self.food_distribution = food_distribution
        self.START_POSITION = start_position
        self.WORLD_WIDTH = world_width
        self.WORLD_HEIGHT = world_height
        self.SCALE_FACTOR = scale_factor
        self.WORLD_SQUARES = world_squares

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
        elif self.food_distribution == FoodDistribution.Unfull_80_Water:
            return self.unfull_arena_water(0.8)
        elif self.food_distribution == FoodDistribution.Unfull_60_Water:
            return self.unfull_arena_water(0.6)
        elif self.food_distribution == FoodDistribution.Unfull_40_Water:
            return self.unfull_arena_water(0.4)
        elif self.food_distribution == FoodDistribution.Unfull_20_Water:
            return self.unfull_arena_water(0.2)

        elif self.food_distribution == FoodDistribution.Clusters:
            return self.clusters_arena()
        elif self.food_distribution == FoodDistribution.Corners:
            return self.corners_arena()
        elif self.food_distribution == FoodDistribution.Spiral:
            return self.spiral_arena(water=False)
        elif self.food_distribution == FoodDistribution.SpiralWithWater:
            return self.spiral_arena(water=True)
        elif self.food_distribution == FoodDistribution.Water:
            return self.water_arena()
        elif self.food_distribution == FoodDistribution.CornersWithWater:
            return self.corners_arena_with_water()
        elif self.food_distribution == FoodDistribution.Cross:
            return self.cross_arena()
        elif self.food_distribution == FoodDistribution.HalfWater:
            return self.half_water_arena()
        elif self.food_distribution == FoodDistribution.HalfWaterHalfFood:
            return self.half_water_arena(half_food=True)
        elif self.food_distribution == FoodDistribution.HalfFull:
            return self.half_full_arena()

    def full_arena(self):
        water_dict = dict()
        food_dict = dict()
        for x in range(0, self.WORLD_WIDTH, self.SCALE_FACTOR):
            for y in range(0, self.WORLD_HEIGHT, self.SCALE_FACTOR):
                if (x, y) != self.START_POSITION:
                    food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
        return food_dict, water_dict

    def half_full_arena(self):
        water_dict = dict()
        food_dict = dict()
        for x in range(0, self.WORLD_WIDTH+1, self.SCALE_FACTOR*2):
            for y in range(0, self.WORLD_HEIGHT+1, self.SCALE_FACTOR*2):
                if (x, y) != self.START_POSITION:
                    food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
        return food_dict, water_dict

    def unfull_arena(self, percentage):
        random.seed(42)
        water_dict = dict()
        food_dict = dict()
        while len(food_dict) < self.WORLD_SQUARES * percentage:
            x = round(random.randint(0, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            y = round(random.randint(0, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            if (x, y) != self.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        return food_dict, water_dict

    def unfull_arena_water(self, percentage):
        random.seed(2)
        water_dict = dict()
        food_dict = dict()
        while len(food_dict) < self.WORLD_SQUARES * percentage:
            x = round(random.randint(0, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            y = round(random.randint(0, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            if (x, y) != self.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        for x in range(0, self.WORLD_WIDTH, self.SCALE_FACTOR):
            for y in range(0, self.WORLD_HEIGHT, self.SCALE_FACTOR):
                if (x, y) in food_dict or (x, y) == self.START_POSITION:
                    continue
                else:
                    water_dict[(x, y)] = 1

        return food_dict, water_dict

    def corners_arena_with_water(self):
        random.seed(42)
        amount_per_corner = 3
        water_dict = dict()
        food_dict = dict()
        topleft = [(round(random.randint(0, self.WORLD_WIDTH * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR,
                    round(random.randint(0, self.WORLD_HEIGHT * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _ in
                   range(amount_per_corner)]
        topright = [(round(
            random.randint(self.WORLD_WIDTH * 0.75, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR,
                     round(random.randint(0, self.WORLD_HEIGHT * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                    in range(amount_per_corner)]
        bottomleft = [(round(random.randint(0, self.WORLD_WIDTH * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR, round(
            random.randint(self.WORLD_HEIGHT * 0.75, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                      in range(amount_per_corner)]
        bottomright = [(round(
            random.randint(self.WORLD_WIDTH * 0.75, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR, round(
            random.randint(self.WORLD_HEIGHT * 0.75, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                       in range(amount_per_corner)]

        for (x, y) in topleft + topright + bottomleft + bottomright:
            food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        for (x, y) in food_dict.keys():
            surrounding_squares = self.get_surrounding_coordinates((x, y))
            surrounding_squares.pop(random.randint(0, len(surrounding_squares) - 1))
            surrounding_squares.pop(random.randint(0, len(surrounding_squares) - 1))
            surrounding_squares.pop(random.randint(0, len(surrounding_squares) - 1))
            surrounding_squares.pop(random.randint(0, len(surrounding_squares) - 1))

            for (sx, sy) in surrounding_squares:
                if (sx, sy) in food_dict or sx == 640 and sy == 800:
                    continue
                water_dict[(sx, sy)] = 1

        return food_dict, water_dict

    def corners_arena(self):
        random.seed(42)
        water_dict = dict()
        food_dict = dict()
        topleft = [(round(random.randint(0, self.WORLD_WIDTH * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR,
                    round(random.randint(0, self.WORLD_HEIGHT * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _ in
                   range(5)]
        topright = [(round(
            random.randint(self.WORLD_WIDTH * 0.75, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR,
                     round(random.randint(0, self.WORLD_HEIGHT * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                    in range(5)]
        bottomleft = [(round(random.randint(0, self.WORLD_WIDTH * 0.25) / self.SCALE_FACTOR) * self.SCALE_FACTOR, round(
            random.randint(self.WORLD_HEIGHT * 0.75, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                      in range(5)]
        bottomright = [(round(
            random.randint(self.WORLD_WIDTH * 0.75, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR, round(
            random.randint(self.WORLD_HEIGHT * 0.75, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR) for _
                       in range(5)]

        for (x, y) in topleft + topright + bottomleft + bottomright:
            food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        return food_dict, water_dict

    def clusters_arena(self):
        random.seed(42)
        water_dict = dict()
        food_dict = dict()
        while len(food_dict) < 0.2 * self.WORLD_SQUARES:
            x = round(random.randint(0, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            y = round(random.randint(0, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            if (x, y) not in food_dict:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
                for j in range(25):
                    dx = round(random.randint(-30, 30) / self.SCALE_FACTOR) * self.SCALE_FACTOR
                    dy = round(random.randint(-30, 30) / self.SCALE_FACTOR) * self.SCALE_FACTOR
                    while (x + dx, y + dy) in food_dict or x + dx < 0 or x + dx > 800 or y + dy < 0 or y + dy > 800:
                        dx = round(random.randint(-30, 30) / self.SCALE_FACTOR) * self.SCALE_FACTOR
                        dy = round(random.randint(-30, 30) / self.SCALE_FACTOR) * self.SCALE_FACTOR
                    x += dx
                    y += dy
                    food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
        return food_dict, water_dict

    def spiral_arena(self, water):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        number_of_points_in_direction = 1
        water_dict = dict()
        food_dict = dict()
        x, y = self.START_POSITION
        # food_dict[(x, y)] = Food(x, y, 1, self.constants)
        run = True
        while run:
            for i in range(1, number_of_points_in_direction + 1):
                x = x + (directions[(number_of_points_in_direction - 1) % 4][0] * self.SCALE_FACTOR)
                y = y + (directions[(number_of_points_in_direction - 1) % 4][1] * self.SCALE_FACTOR)
                if x > self.WORLD_WIDTH or x < 0 or y > self.WORLD_HEIGHT or y < 0:
                    run = False
                    continue
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
            number_of_points_in_direction += 1

        if water:
            for x in range(0, self.WORLD_WIDTH, self.SCALE_FACTOR):
                for y in range(0, self.WORLD_HEIGHT, self.SCALE_FACTOR):
                    if (x, y) in food_dict or (x, y) == self.START_POSITION:
                        continue
                    else:
                        water_dict[(x, y)] = 1

        return food_dict, water_dict

    def water_arena(self):
        random.seed(42)
        water_dict = dict()
        food_dict = dict()
        while len(food_dict) < self.WORLD_SQUARES * 0.5:
            x = round(random.randint(0, self.WORLD_WIDTH) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            y = round(random.randint(0, self.WORLD_HEIGHT) / self.SCALE_FACTOR) * self.SCALE_FACTOR
            if (x, y) != self.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
        return food_dict, water_dict

    def cross_arena(self):
        food_dict = dict()
        water_dict = dict()
        for x in range(0, self.WORLD_WIDTH, self.SCALE_FACTOR):
            y = self.WORLD_HEIGHT / 2
            if (x, y) != self.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        for y in range(0, self.WORLD_HEIGHT, self.SCALE_FACTOR):
            x = self.WORLD_WIDTH / 2
            if (x, y) != self.START_POSITION:
                food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)

        for x in range(0, self.WORLD_WIDTH, self.SCALE_FACTOR):
            for y in range(0, self.WORLD_HEIGHT, self.SCALE_FACTOR):
                if (x, y) in food_dict or (x, y) == self.START_POSITION:
                    continue
                else:
                    water_dict[(x, y)] = 1

        return food_dict, water_dict

    def half_water_arena(self, half_food=False):
        food_dict = dict()
        water_dict = dict()
        counter = 0

        for x in range(0, self.WORLD_WIDTH+1, self.SCALE_FACTOR):
            for y in range(0, self.WORLD_HEIGHT+1, self.SCALE_FACTOR):
                if (x, y) == self.START_POSITION:
                    continue
                elif y % 80 == 0 or x == 0 or x == self.WORLD_WIDTH:
                    if not half_food or (half_food and counter % 2 == 0):
                        food_dict[(x, y)] = Food(x, y, 1, self.SCALE_FACTOR)
                else:
                    water_dict[(x, y)] = 1
            counter += 1
        return food_dict, water_dict

    def get_surrounding_coordinates(self, coord):
        x, y = coord
        surrounding_coords = [(x - self.SCALE_FACTOR, y - self.SCALE_FACTOR), (x, y - self.SCALE_FACTOR),
                              (x + self.SCALE_FACTOR, y - self.SCALE_FACTOR),
                              (x - self.SCALE_FACTOR, y), (x + self.SCALE_FACTOR, y),
                              (x - self.SCALE_FACTOR, y + self.SCALE_FACTOR), (x, y + self.SCALE_FACTOR),
                              (x + self.SCALE_FACTOR, y + self.SCALE_FACTOR)]
        return surrounding_coords
