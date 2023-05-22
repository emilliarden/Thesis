from enum import Enum
from Classes.food import FoodCreater, FoodDistribution

class Constants:
    def __init__(self, sensing_mode, start_mode, food_distribution, start_type, draw):
        self.SCALE_FACTOR = 40
        self.WORLD_HEIGHT = 840
        self.WORLD_WIDTH = 840
        self.MIDDLE_COORD = (self.WORLD_WIDTH/2-self.SCALE_FACTOR/2, self.WORLD_HEIGHT/2-self.SCALE_FACTOR/2)
        self.WORLD_SQUARES = self.WORLD_WIDTH/self.SCALE_FACTOR*self.WORLD_HEIGHT/self.SCALE_FACTOR
        self.WATER_COLOR = (0, 157, 196)
        self.FOOD_COLOR = (124, 252, 0)
        self.FOOD2_COLOR = (195, 0, 195)
        self.TEXT_COLOR = (255, 165, 0)
        self.TEXT_COLOR2 = (255, 0, 255)
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.LINE_COLOR = (255, 255, 255)
        self.SENSING_DISTANCE = 3
        self.START_POSITION = self.get_start_pos(food_distribution)
        #self.START_POSITION = (0, 0)
        self.CONFIG_PATH = "config.txt"
        self.FILE_PREFIX = ""
        self.SENSING_MODE = sensing_mode
        self.START_MODE = start_mode
        self.START_TYPE = start_type
        self.FOOD_DISTRIBUTION = food_distribution
        self.FOOD_CREATER = FoodCreater(food_distribution=food_distribution, start_position=self.START_POSITION, world_width=self.WORLD_WIDTH, world_height=self.WORLD_HEIGHT, scale_factor=self.SCALE_FACTOR, world_squares=self.WORLD_SQUARES, middle_coord=self.MIDDLE_COORD)
        self.FOOD_DICT, self.WATER_DICT = FoodCreater.get_food(self.FOOD_CREATER)
        self.DRAW = draw
        self.POPULATION_SIZE = 10 if self.START_TYPE == StartType.Competition else 100
        self.FITNESS_THRESH = len(self.FOOD_DICT) #* self.get_fitness_threshold(self.FOOD_DISTRIBUTION)
        self.NUM_INPUTS = self.get_number_of_inputs()
        self.ALLOWED_MOVES_WITHOUT_PROGRESS = max(round(self.WORLD_SQUARES - self.FITNESS_THRESH), round(self.WORLD_SQUARES * 0.1))

    def get_number_of_inputs(self):
        number_of_inputs = 0
        if self.SENSING_MODE == SensingMode.Box:
            for i in range(1, self.SENSING_DISTANCE + 1):
                number_of_inputs += (i * 8) * 3
        elif self.SENSING_MODE == SensingMode.BoxDiff:
            for i in range(1, self.SENSING_DISTANCE + 1):
                number_of_inputs += (i * 8)
        # elif self.SENSING_MODE == SensingMode.Cross:
        #     number_of_inputs = (4 * self.SENSING_DISTANCE)
        # elif self.SENSING_MODE == SensingMode.Pyramid:
        #     if self.SENSING_DISTANCE == 4:
        #         number_of_inputs = 40
        #     elif self.SENSING_DISTANCE == 3:
        #         number_of_inputs = 24

        return number_of_inputs + 7

    def get_start_pos(self, food_distribution):
        food_distribution_with_start_pos_middle = [FoodDistribution.SpiralWithWater, FoodDistribution.Spiral,
                                                   FoodDistribution.Cross, FoodDistribution.Corners,
                                                   FoodDistribution.SpaceBetweenFood, FoodDistribution.CornersWithWater,
                                                   FoodDistribution.SpiralWithWater2, FoodDistribution.Unfull_25
                                                   #FoodDistribution.Full,
                                                   ]
        if food_distribution in food_distribution_with_start_pos_middle:
            return (self.WORLD_WIDTH/2-self.SCALE_FACTOR/2, self.WORLD_HEIGHT/2-self.SCALE_FACTOR/2)
        else:
            return (0, 0)

    def get_fitness_threshold(self, food_distribution):
        food_distributions_that_need_100 = [FoodDistribution.SpiralWithWater, FoodDistribution.Spiral,
                                            FoodDistribution.Cross, FoodDistribution.Corners,
                                            FoodDistribution.SpaceBetweenFood, FoodDistribution.HalfWaterHalfFood,
                                            FoodDistribution.TwoEndsWaterMiddle, FoodDistribution.Full, FoodDistribution.Unfull_20,
                                            FoodDistribution.Unfull_60, FoodDistribution.CornersWithWater, FoodDistribution.Unfull_80,
                                            FoodDistribution.HalfFull]

        if food_distribution in food_distributions_that_need_100:
            return 1
        else:
            return 0.9









class StartMode(Enum):
    New = 1
    Checkpoint = 2
    Winner = 3


class SensingMode(Enum):
    Box = 1
    Cross = 2
    Pyramid = 3
    BoxDiff = 4


class StartType(Enum):
    Single = 1
    Competition = 2
    IvI = 3


class ContentOfSquare(Enum):
    Food = 1
    Water = -1
    Empty = 0
    OutsideArena = -2
    OtherRobot = -3


