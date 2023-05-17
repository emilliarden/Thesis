from Classes.constants import Constants
from Classes.food import FoodDistribution
from Classes.screen import Screen

if __name__ == "__main__":
    start_mode = None
    start_type = None
    sensing_mode = None
    food_distribution = FoodDistribution.QuarterFull
    draw = False

    constants = Constants(draw=draw, sensing_mode=sensing_mode, start_mode=start_mode,
                          food_distribution=food_distribution, start_type=start_type)

    screen = Screen(constants)
    screen.draw_arena(constants.FOOD_DICT, constants.WATER_DICT)
