import random
import neat
import pygame

from Advanced.Classes.food import Food
from Advanced.Classes.neat_agent import Agent
from Advanced.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH
from Advanced.Classes.kd_tree import QuadTree

WATER_COLOR = (0, 157, 196)
FOOD_COLOR = (34, 139, 34)
FOOD2_COLOR = (195, 0, 195)
TEXT_COLOR = (255, 165, 0)
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 20)
neat_population = None

INITIAL_POPULATION_SIZE = 10
INITIAL_AMOUNT_FOOD = 800


def setup_screen():
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    pygame.display.set_caption('Evolution')
    #screen.fill(BACKGROUND_COLOR)
    return screen


def create_initial_pop(population_size):
    robots = [Agent() for x in range(population_size)]
    x_startpos = 0
    for r in robots:
        r.x = x_startpos
        r.out_of_bounds = False
        r.y = WORLD_HEIGHT/2
        r.q = random.random()
        x_startpos += 40
    return robots


def create_population_from_genomes(genomes):
    agents = []
    for i, (genome_id, genome) in enumerate(genomes):
        agent = Agent()
        agent.x = 40 * i
        agent.y = WORLD_HEIGHT / 2
        agent.q = random.random()
        agent.genome = genome
        agent.genome.fitness = 0
        agent.nn = neat.nn.FeedForwardNetwork.create(genome, config)
        agents.append(agent)
    return agents



def simulate(genomes):
    water = []
    food = Food.create_food(water)
    quad_tree = QuadTree([(0, 0), (WORLD_WIDTH, WORLD_HEIGHT)])
    for f in food:
        quad_tree.add(f.get_rect().center)

    food_rects = [f.get_rect() for f in food]
    population = create_population_from_genomes(genomes)

    timestep = 0
    timesteps_without_progress = 0
    oldest_robot = population[0]
    clock = pygame.time.Clock()


    while timestep < 5000 and timesteps_without_progress < 500:
        # TO QUIT PYGAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        timestep += 1

        #SIMULATION
        for agent in population:
            if agent.out_of_bounds:
                continue

            agent_current_rect = agent.get_rect()
            other_robots = list(population)
            other_robots.remove(agent)
            input_to_nn = agent.sense(food_rects, water, other_robots, quad_tree)
            nn_output = agent.nn.activate(input_to_nn)
            #nn_output = agent.nn.get_output(input_to_nn)

            #GET NEXT MOVE
            agent.set_motor_speeds(nn_output)
            agent_next_rect = agent.simulation_step_rect()
            other_robots_rects = [agent.get_rect() for agent in other_robots]

            if pygame.Rect.collidelist(agent_next_rect, other_robots_rects) == -1:
                agent.simulation_step()
                agent_current_rect = agent.get_rect()

            collides_with_food_at_position = pygame.Rect.collidelist(agent_current_rect, food_rects)
            while collides_with_food_at_position > -1:
                timesteps_without_progress = 0
                agent.energy += food[collides_with_food_at_position].energy
                agent.genome.fitness += food[collides_with_food_at_position].energy
                quad_tree.remove(food_rects[collides_with_food_at_position].center)
                food_rects.pop(collides_with_food_at_position)
                food.pop(collides_with_food_at_position)
                collides_with_food_at_position = pygame.Rect.collidelist(agent_current_rect, food_rects)

            if agent_current_rect.collidelist(water) > -1 or agent_current_rect.centerx > WORLD_WIDTH or agent_current_rect.centerx < 0 or agent_current_rect.centery > WORLD_HEIGHT or agent_current_rect.centery < 0:
                agent.out_of_bounds = True
                continue
        timesteps_without_progress += 1
        rank_of_robots = sorted(population, key=lambda x: x.genome.fitness, reverse=True)
        oldest_robot = rank_of_robots[0] if len(rank_of_robots) > 0 else Agent()
        update_display(population, food, timestep, oldest_robot, clock)

def update_display(population, food, timestep, oldest_robot, clock):
    screen.fill(BACKGROUND_COLOR)
    draw_food(food)
    for i in range(len(population)):
        pygame.draw.rect(screen, population[i].color, population[i].get_rect())
        sensing_points = population[i].get_sensing_points()
        pygame.draw.polygon(screen, population[i].color, sensing_points, 1)
        # pygame.draw.rect(screen, population[i].color, population[i].sensing_rect, 1)
    update_text(screen, timestep, oldest_robot, len(population), len(food), clock)
    clock.tick()
    pygame.display.update()


def draw_food(food):
    for f in food:
        if f.energy < 40:
            pygame.draw.rect(screen, FOOD_COLOR, f.get_rect())
        else:
            pygame.draw.rect(screen, FOOD2_COLOR, f.get_rect())

def draw_water(water):
    for w in water:
        pygame.draw.rect(screen, WATER_COLOR, w)

def update_text(screen, timestep, oldest_robot, numberOfAgents, amountOffood, clock):
    text = font.render("Timestep: " + str(timestep), True, TEXT_COLOR )
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 20
    screen.blit(text, text_rect)

    text = font.render("Energy for best robot: " + str(oldest_robot.genome.fitness), True, TEXT_COLOR)
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

    text = font.render("Generation: " + str(neat_population.generation), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomleft = 0, 100
    screen.blit(text, text_rect)

    text = font.render("FPS: " + str(clock.get_fps().__round__(1)), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomleft = WORLD_WIDTH-100, 20
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, (255, 0, 0), (oldest_robot.get_rect().topleft[0]-7.5, oldest_robot.get_rect().topleft[1]-7.5, SCALE_FACTOR+15, SCALE_FACTOR+15), 2, border_radius=1)

def eval_genomes(genomes, config):
    simulate(genomes)


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-20')
    global neat_population
    neat_population = neat.Population(config)
    neat_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_population.add_reporter(stats)
    neat_population.add_reporter(neat.Checkpointer(1))
    winner = neat_population.run(eval_genomes, 50)
    print(winner)


if __name__ == "__main__":
    config_path = "/Advanced/NEAT/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation
                         , config_path)

    screen = setup_screen()
    # water_rects = [Water().rect for x in range(10)]

    run_neat(config)
