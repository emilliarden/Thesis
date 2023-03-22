import copy
import math
import random
import neat
import pygame

from Advanced.Classes.food import Food
from Advanced.Classes.agent import Agent
from Advanced.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH
from Advanced.Classes.kd_tree import QuadTree

WATER_COLOR = (0, 157, 196)
FOOD_COLOR = (34, 139, 34)
FOOD2_COLOR = (195, 0, 195)
TEXT_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)

INITIAL_POPULATION_SIZE = 10
INITIAL_AMOUNT_FOOD = 400



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
    robots = [Agent() for x in range(population_size)]
    x_startpos = 0
    for r in robots:
        r.x = x_startpos
        r.y = WORLD_HEIGHT/2
        r.q = random.random()
        x_startpos += 40
    return robots

def adjust_food_environment(timestep, food_rects, population):
    food_to_add = []
    min_food = INITIAL_AMOUNT_FOOD #if len(population) < 50  else INITIAL_AMOUNT_FOOD*5
    if timestep % 250 == 0:
        food_to_add.append(Food(random.randint(0, WORLD_WIDTH/5), random.randint(0, WORLD_HEIGHT/5), 40))
        food_to_add.append(Food(random.randint(WORLD_WIDTH*0.8, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT/5), 40))
        food_to_add.append(Food(random.randint(WORLD_WIDTH*0.8, WORLD_WIDTH), random.randint(WORLD_HEIGHT*0.8, WORLD_HEIGHT), 40))
        food_to_add.append(Food(random.randint(0, WORLD_WIDTH/5), random.randint(WORLD_HEIGHT*0.8, WORLD_HEIGHT), 40))

    if len(food_rects) < min_food:
        diff = min_food - len(food_rects)
        for _ in range(diff):
            food_to_add.append(Food(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT), 20))

    return food_to_add



def simulate(screen, population, food, water, quad_tree):
    food_rects = [f.get_rect() for f in food]
    timestep = 0
    oldest_robot = population[0]
    clock = pygame.time.Clock()

    while timestep < 50000:
        # TO QUIT PYGAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if len(population) < INITIAL_POPULATION_SIZE:
            for i in range(INITIAL_POPULATION_SIZE - len(population)):
                population.append(oldest_robot.create_offspring())


            # population = create_initial_pop(INITIAL_POPULATION_SIZE)
            # food.py = Food.create_random_food(water_rects, INITIAL_AMOUNT_FOOD)
            # food_rects = [f.rect for f in food.py]
            # timestep = 0

        timestep += 1
        # TO ENSURE FOOD IS AVAILABLE
        extra_food = adjust_food_environment(timestep, food_rects, population)
        food.extend(extra_food)
        food_rects.extend([e_f.get_rect() for e_f in extra_food])
        for f in extra_food:
            quad_tree.add(f.get_rect().center)

        #SIMULATION
        for agent in population:
            #CHECK IF REPRODUCE
            if agent.age > 1000  and len(population) < 80:
                population.append(agent.create_offspring())
                agent.energy -= agent.energy/2

            agent_current_rect = agent.get_rect()
            other_robots = list(population)
            other_robots.remove(agent)
            input_to_nn = agent.sense(food_rects, water, other_robots, quad_tree)
            nn_output = agent.nn.get_output(input_to_nn)

            #GET NEXT MOVE
            agent.set_motor_speeds(nn_output)
            agent_next_rect = agent.simulation_step_rect()
            other_robots_rects = [agent.get_rect() for agent in other_robots]

            if pygame.Rect.collidelist(agent_next_rect, other_robots_rects) == -1:
                agent.simulation_step()
                agent_current_rect = agent.get_rect()
                #agent.py.move_robot(nn_output)

            collides_with_food_at_position = pygame.Rect.collidelist(agent_current_rect, food_rects)
            while collides_with_food_at_position > -1:
                agent.energy += food[collides_with_food_at_position].energy
                quad_tree.remove(food_rects[collides_with_food_at_position].center)
                food_rects.pop(collides_with_food_at_position)
                food.pop(collides_with_food_at_position)

                collides_with_food_at_position = pygame.Rect.collidelist(agent_current_rect, food_rects)

            if agent_current_rect.collidelist(water_rects) > -1 or agent_current_rect.centerx > WORLD_WIDTH or agent_current_rect.centerx < 0 or agent_current_rect.centery > WORLD_HEIGHT or agent_current_rect.centery < 0:
                agent.out_of_bounds = True
                population.remove(agent)
                continue

            agent.energy -= 1
            agent.age += 1
            if agent.energy < 0:
                population.remove(agent)
                continue

        rank_of_robots = sorted(population, key=lambda x: x.age, reverse=True)
        oldest_robot = rank_of_robots[0] if len(rank_of_robots) > 0 else Agent()
        #update_display(food.py, timestep, oldest_robot, clock)

def update_display(food, timestep, oldest_robot, clock):
    screen.fill(BACKGROUND_COLOR)
    draw_food(screen, food)
    draw_water(screen, water_rects)
    for i in range(len(population)):
        pygame.draw.rect(screen, population[i].color, population[i].get_rect())
        sensing_points = population[i].get_sensing_points()
        pygame.draw.polygon(screen, population[i].color, sensing_points, 1)
        # pygame.draw.rect(screen, population[i].color, population[i].sensing_rect, 1)
    update_text(screen, timestep, oldest_robot, len(population), len(food), clock)
    clock.tick()
    pygame.display.update()


def draw_food(screen, food):
    for f in food:
        if f.energy < 40:
            pygame.draw.rect(screen, FOOD_COLOR, f.get_rect())
        else:
            pygame.draw.rect(screen, FOOD2_COLOR, f.get_rect())

def draw_water(screen, water):
    for w in water:
        pygame.draw.rect(screen, WATER_COLOR, w)

def update_text(screen, timestep, oldest_robot, numberOfAgents, amountOffood, clock):
    text = font.render("Timestep: " + str(timestep), True, TEXT_COLOR )
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 20
    screen.blit(text, text_rect)

    text = font.render("Age of oldest robot: " + str(oldest_robot.age), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 40
    screen.blit(text, text_rect)

    text = font.render("Robots: " + str(numberOfAgents), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 60
    screen.blit(text, text_rect)

    text = font.render("Food: " + str(amountOffood), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 80
    screen.blit(text, text_rect)

    text = font.render("FPS: " + str(clock.get_fps().__round__(1)), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomleft = WORLD_WIDTH-100, 20
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, (255, 0, 0), (oldest_robot.get_rect().topleft[0]-7.5, oldest_robot.get_rect().topleft[1]-7.5, SCALE_FACTOR+15, SCALE_FACTOR+15), 2, border_radius=1)

def eval_genomes(genomes, config):
    pass


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-20')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    config_path = "/Users/emilknudsen/Desktop/research/Advanced/NEAT/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation
                         , config_path)

    screen = setup_screen()
    # water_rects = [Water().rect for x in range(10)]
    water_rects = []
    food_objects = Food.create_random_food(water_rects, INITIAL_AMOUNT_FOOD)
    quad_tree = QuadTree([(0, 0), (WORLD_WIDTH, WORLD_HEIGHT)])
    for f in food_objects:
        quad_tree.add(f.get_rect().center)

    population = create_initial_pop(INITIAL_POPULATION_SIZE)
    best_robot = population[0]
    simulate(screen, population, food_objects, water_rects, quad_tree)
