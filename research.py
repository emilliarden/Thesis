import copy
import math
import random

import pygame

from Classes import Robot, Food, Water
from Classes.Constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH

WATER_COLOR = (0, 30, 255)
FOOD_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)


def setup_screen():
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    pygame.display.set_caption('Evolution')
    screen.fill(BACKGROUND_COLOR)
    return screen

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


def simulate(screen, population, food, water):
    food_rects = [f.rect for f in food]
    roundsWithoutProgress = 0
    min_food = 500

    for timestep in range(50000):
        # TO QUIT PYGAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # TO ENSURE FOOD IS AVAILABLE
        if len(food_rects) < min_food:
            food_rects.append(Food(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT)))

        #SIMULATION
        for agent in population:
            #CHECK IF REPRODUCE
            if agent.energy >= 200:
                new_agent = copy.copy(agent)
                new_agent.mutate()
                new_agent.x = random.randint(0, 800)
                new_agent.y = random.randint(0, 800)
                population.append(new_agent)

            agent_current_rect = agent.rect
            input_to_nn = agent.sense(food_rects, water_rects, population, timestep)
            nn_output = agent.nn.get_output(input_to_nn)
            agent_next_rect = agent.get_robot_rect_from_move(nn_output)
            other_robots = population[:].remove(agent)
            other_robots_rects = [agent.rect for agent in other_robots]
            if agent_next_rect.collidelist(other_robots_rects) == -1:
                agent_current_rect = agent_next_rect
                agent.move_robot(nn_output)
                agent.energy -= 1

            if agent_current_rect.collidelist(food_rects) > -1:
                roundsWithoutProgress = 0
                agent.energy += 20
                food_rects.pop(agent_current_rect.collidelist(food_rects))
            if agent_current_rect.collidelist(water_rects) > -1 or agent_current_rect.centerx > WORLD_WIDTH or agent_current_rect.centerx < 0 or agent_current_rect.centery > WORLD_HEIGHT or agent_current_rect.centery < 0:
                agent.out_of_bounds = True
                population.remove(agent)
        
        roundsWithoutProgress += 1
        screen.fill(BACKGROUND_COLOR)
        draw_food(screen, food_rects)
        draw_water(screen, water_rects)
        update_text(screen, timestep, sorted(population, key=lambda x: x.energy, reverse=True)[0], len(population))
        for i in range(len(population)):
            pygame.draw.rect(screen, population[i].color, population[i].rect)
            pygame.draw.line(screen, population[i].color, population[i].get_direction_line()[0], population[i].get_direction_line()[1], 5)
        pygame.display.update()

    


def draw_food(screen, food_rects):
    for f in food_rects:
        pygame.draw.rect(screen, FOOD_COLOR, f)

def draw_water(screen, water):
    for w in water:
        pygame.draw.rect(screen, WATER_COLOR, w)

def update_text(screen, timestep, best_robot, numberOfAgents):
    text = font.render("Timestep: " + str(timestep), True, TEXT_COLOR )
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 20
    screen.blit(text, text_rect)

    text = font.render("Current best robot: " + str(best_robot.energy), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 40
    screen.blit(text, text_rect)

    text = font.render("Robots: " + str(numberOfAgents), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 60
    screen.blit(text, text_rect)



if __name__ == "__main__":
    screen = setup_screen()
    water_rects = [Water().rect for x in range(10)]
    food_locations = Food.create_food(water_rects)
    population = create_initial_pop(20)
    best_robot = population[0]
    simulate(screen, population, food_locations, water_rects)
    pygame.quit()
