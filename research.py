import pygame
import time
import random
import copy
import math
from classes import Robot, Food, Water
from numpy.random import rand
from numpy.random import randint

SCALE_FACTOR = 10

WORLD_HEIGHT = 800
WORLD_WIDTH = 800
WATER_COLOR =       (0,0,255)
FOOD_COLOR =        (0,255,0)
BACKGROUND_COLOR =  (0,0,0)
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)


def setup_screen():
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    pygame.display.set_caption('Evolution')
    screen.fill(BACKGROUND_COLOR)
    return screen


# crossover two parents to create two children
def crossover(r1, r2, r_cross=0.90):
	# children are copies of parents by default
    c1 = copy.copy(r1)
    c1.fitness = -1000
    c1.foodGathered = 0
    c2 = copy.copy(r2)
    c2.fitness = -1000
    c2.foodGathered = 0

    # check for recombination
    if rand() < r_cross:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(r1.moves)-2)
            # perform crossover
            c1.set_moves(r1.moves[:pt] + r2.moves[pt:])
            c2.set_moves(r2.moves[:pt] + r1.moves[pt:])
    return [c1, c2]


def create_next_generation(robots):
    res = []
    best_amount = math.floor(len(robots)*0.1)
    mutate_amount = math.floor(len(robots)*0.8)
    random_amount = math.floor(len(robots)*0.1)

    for i in range(best_amount):
        robots[i].foodGathered = 0
        res.append(robots[i])
    for _ in range(mutate_amount):
        new_robot = copy.deepcopy(robots[0])
        new_robot.mutate()
        res.append(new_robot)
    for _ in range(random_amount):
        res.append(Robot())

    random.shuffle(res)

    x_startpos = 0
    for r in res:
        r.x = x_startpos
        r.y = WORLD_HEIGHT/2
        x_startpos += 40

    return res


def create_initial_pop(population_size):
    robots = [Robot() for x in range(population_size)]
    x_startpos = 0
    for r in robots:
        r.x = x_startpos
        r.y = WORLD_HEIGHT/2
        x_startpos += 40
    return robots


def simulate_generation(screen, robots, food_locations, water_locations, generation, best_robot):
    foods = food_locations.copy()
    food_rects = [f.rect for f in foods]
    current_robot_rects = []
    robot_colors = []
    

    for i in range(800):
        for r in robots:
            input_to_nn = r.sense(food_rects, robots)
            r.move_robot(r.nn.get_output(input_to_nn))
            robots_current_rect = pygame.Rect(r.x, r.y, r.size, r.size)
            current_robot_rects.append(robots_current_rect)
            robot_colors.append(r.color)
            if (robots_current_rect.collidelist(food_rects) > 0):
                r.foodGathered += 1
                food_rects.pop(robots_current_rect.collidelist(food_rects))
                # screen.fill(BACKGROUND_COLOR)
                # draw_food(screen, food_rects)
        
        
        screen.fill(BACKGROUND_COLOR)
        draw_food(screen, food_rects)
        update_text(screen, generation, best_robot, len(robots))
        for i in range(len(current_robot_rects)):
             pygame.draw.rect(screen, robot_colors[i], current_robot_rects[i])
        pygame.display.update()
        current_robot_rects = []
        robot_colors = []

    


def draw_food(screen, food_rects):
    for f in food_rects:
        pygame.draw.rect(screen, FOOD_COLOR, f)

def draw_water(screen, water):
    for w in water:
        pygame.draw.polygon(screen, WATER_COLOR, w.points )

def update_text(screen, generation, best_robot_last_gen, numberOfAgents):
    text = font.render("Generation: " + str(generation), True, (255,165,0))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0,20
    screen.blit(text, text_rect)

    text = font.render("Best weight LG: " + str([(round(x.weight,2),round(x.bias,2)) for x in best_robot_last_gen.nn.input_layer]) + " - " + str((round(best_robot_last_gen.nn.output_layer[0].weight,2),round(best_robot_last_gen.nn.output_layer[0].bias,2))), True, (255,165,0))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0,40
    screen.blit(text, text_rect)

    text = font.render("Best fitness LG: " + str(best_robot_last_gen.foodGathered), True, (255,165,0))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0,60
    screen.blit(text, text_rect)

    text = font.render("Robots: " + str(numberOfAgents), True, (255,165,0))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0,80
    screen.blit(text, text_rect)


    
    


if __name__ == "__main__":
    screen = setup_screen()
    food_locations = [Food(x,y) for x in range(10, WORLD_WIDTH-10, SCALE_FACTOR) for y in range(10, WORLD_HEIGHT-10, SCALE_FACTOR) ]
    water_locations = [Water() for x in range(10)]
    current_gen = create_initial_pop(20)
    best_robot_in_last_gen = current_gen[0]
    best_robot = current_gen[0]
    
    for i in range(500):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        simulate_generation(screen, current_gen, food_locations, water_locations, i, best_robot_in_last_gen)
        current_gen_sorted = sorted(current_gen, key=lambda x: x.foodGathered, reverse=True)
        current_gen_average_fitness = sum(r.foodGathered for r in current_gen_sorted)/len(current_gen_sorted)
        print("Generation " + str(i) + "'s average fitness: " + str(current_gen_average_fitness))
        best_robot_in_last_gen = copy.copy(current_gen_sorted[0])
        # if (best_robot_in_generation.foodGathered > best_robot.foodGathered):
        #     best_robot = best_robot_in_generation
        current_gen = create_next_generation(current_gen_sorted)
    




    # next_population = create_next_generation(best_robots)
    # best_robot_in_next_population = simulate_population(screen, next_population, food_locations)
    # simulate_one_robot(screen, best_robot_in_next_population, food_locations)
    # best = find_best_robot(best_robots)
    # simulate_one_robot(screen, best, food_locations)
    s = 1
    pygame.quit()
