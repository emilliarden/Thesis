from enum import Enum

class Constants:
    def __init__(self, sensing_mode, start_mode, food_distribution, start_type, draw):
        self.SCALE_FACTOR = 20
        self.WORLD_HEIGHT = 800
        self.WORLD_WIDTH = 800
        self.WORLD_SQUARES = self.WORLD_WIDTH/self.SCALE_FACTOR*self.WORLD_HEIGHT/self.SCALE_FACTOR
        self.WATER_COLOR = (0, 157, 196)
        self.FOOD_COLOR = (0, 154, 23)
        self.FOOD2_COLOR = (195, 0, 195)
        self.TEXT_COLOR = (255, 165, 0)
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.SENSING_DISTANCE = 3
        self.START_POSITION = (self.WORLD_WIDTH/2, self.WORLD_HEIGHT/2)
        self.CONFIG_PATH = "config.txt"
        self.FILE_PREFIX = ""
        self.SENSING_MODE = sensing_mode
        self.START_MODE = start_mode
        self.START_TYPE = start_type
        self.FOOD_DISTRIBUTION = food_distribution
        self.DRAW = draw
        self.POPULATION_SIZE = 100 if self.START_TYPE == StartType.Single else 10
        self.FITNESS_THRESH = self.get_fitness_threshold()
        self.NUM_INPUTS = self.get_number_of_inputs()
        self.ALLOWED_MOVES_WITHOUT_PROGRESS = round(self.WORLD_SQUARES - self.FITNESS_THRESH)

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

    def get_fitness_threshold(self):
        if self.FOOD_DISTRIBUTION == FoodDistribution.Full:
            return self.WORLD_SQUARES * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Unfull_80:
            return self.WORLD_SQUARES * 0.8 * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Unfull_60:
            return self.WORLD_SQUARES * 0.6 * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Unfull_40:
            return self.WORLD_SQUARES * 0.4 * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Unfull_20:
            return self.WORLD_SQUARES * 0.2 * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Clusters:
            return self.WORLD_SQUARES * 0.5 * 0.9
        elif self.FOOD_DISTRIBUTION == FoodDistribution.Corners:
            return 10000000 * 0.9







class FoodDistribution(Enum):
    Full = 1
    Unfull_80 = 2
    Unfull_60 = 3
    Unfull_40 = 4
    Unfull_20 = 5
    Corners = 6
    Clusters = 7
    Circle = 8


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


class ContentOfSquare(Enum):
    Food = 1
    OtherRobot = 2
    Empty = 3
    OutsideArena = 4


