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
    best_amount = math.floor(len(robots)*0.2)
    mutate_amount = math.floor(len(robots)*0.8)
    # random_amount = math.floor(len(robots)*0.1)

    for i in range(best_amount):
        robots[i].foodGathered = 0
        res.append(robots[i])

    use_best = True
    for _ in range(mutate_amount):
        new_robot = copy.deepcopy(robots[0 if use_best else 1])
        new_robot.mutate()
        res.append(new_robot)
        use_best = not use_best

    # for _ in range(random_amount):
    #     res.append(Robot())

    random.shuffle(res)

    x_startpos = 0
    for r in res:
        r.x = x_startpos
        r.y = WORLD_HEIGHT/2
        r.out_of_bounds = False
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


def simulate_generation(screen, robots, food_locations, water_rects, generation, best_robot):
    foods = food_locations.copy()
    food_rects = [f.rect for f in foods]
    current_robot_rects = []
    current_robot_directions = []
    robot_colors = []
    roundsWithoutProgress = 0

    for i in range(800):
        if roundsWithoutProgress > 100:
            break
        for r in robots:
            if r.out_of_bounds == True:
                continue
            robots_current_rect = pygame.Rect(r.x, r.y, r.size, r.size)
            input_to_nn = r.sense(food_rects, water_rects, robots, i)
            nn_output = r.nn.get_output(input_to_nn)
            robots_next_rect = r.get_robot_rect_from_move(nn_output)
            bb = robots[:]
            bb.remove(r)
            qq = [pygame.Rect(rr.x, rr.y, rr.size, rr.size) for rr in bb]
            if robots_next_rect.collidelist(qq) == -1:
                robots_current_rect = robots_next_rect
                r.move_robot(r.nn.get_output(input_to_nn))


            current_robot_rects.append(robots_current_rect)
            current_robot_directions.append(r.get_direction_line())
            robot_colors.append(r.color)
            if robots_current_rect.collidelist(food_rects) > -1:
                roundsWithoutProgress = 0
                r.foodGathered += 1
                food_rects.pop(robots_current_rect.collidelist(food_rects))
            if robots_current_rect.collidelist(water_rects) > -1 or robots_current_rect.centerx > WORLD_WIDTH or robots_current_rect.centerx < 0 or robots_current_rect.centery > WORLD_HEIGHT or robots_current_rect.centery < 0:
                r.out_of_bounds = True
        
        roundsWithoutProgress += 1
        screen.fill(BACKGROUND_COLOR)
        draw_food(screen, food_rects)
        draw_water(screen, water_rects)
        update_text(screen, generation, best_robot, len(robots), i)
        for i in range(len(current_robot_rects)):
            pygame.draw.rect(screen, robot_colors[i], current_robot_rects[i])
            pygame.draw.line(screen, robot_colors[i], current_robot_directions[i][0], current_robot_directions[i][1], 5)
        pygame.display.update()
        current_robot_rects = []
        current_robot_directions = []
        robot_colors = []

    


def draw_food(screen, food_rects):
    for f in food_rects:
        pygame.draw.rect(screen, FOOD_COLOR, f)

def draw_water(screen, water):
    for w in water:
        pygame.draw.rect(screen, WATER_COLOR, w)

def update_text(screen, generation, best_robot_last_gen, numberOfAgents, timestep):
    text = font.render("Generation: " + str(generation), True, (255,165,0))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0,20
    screen.blit(text, text_rect)

    text = font.render("Timestep: " + str(timestep), True, (255,165,0))
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



def create_food(water_rects):
    food = []
    for x in range(10, WORLD_WIDTH-10, SCALE_FACTOR):
        for y in range(10, WORLD_HEIGHT-10, SCALE_FACTOR):
            food_rect = pygame.Rect(x, y, SCALE_FACTOR, SCALE_FACTOR)
            if food_rect.collidelist(water_rects) > -1:
                continue
            else:
                food.append(Food(x,y))
    return food


if __name__ == "__main__":
    screen = setup_screen()
    water_rects = [Water().rect for x in range(10)]
    food_locations = create_food(water_rects)
    
    current_gen = create_initial_pop(20)
    best_robot_in_last_gen = current_gen[0]
    best_robot = current_gen[0]
    
    for i in range(500):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        simulate_generation(screen, current_gen, food_locations, water_rects, i, best_robot_in_last_gen)
        current_gen_sorted = sorted(current_gen, key=lambda x: x.foodGathered, reverse=True)
        current_gen_average_fitness = sum(r.foodGathered for r in current_gen_sorted)/len(current_gen_sorted)
        print("Generation " + str(i) + "'s average fitness: " + str(current_gen_average_fitness))
        best_robot_in_last_gen = copy.copy(current_gen_sorted[0])
        # if (best_robot_in_generation.foodGathered > best_robot.foodGathered):
        #     best_robot = best_robot_in_generation
        current_gen = create_next_generation(current_gen_sorted)
    
    s = 1
    pygame.quit()
