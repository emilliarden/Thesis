import random
import neat
import pygame

from Simple.Classes.food import Food
from Simple.Classes.screen import Screen
from Simple.Classes.agent import Agent
from Simple.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH, WATER_COLOR, FOOD_COLOR, FOOD2_COLOR,\
    TEXT_COLOR, BACKGROUND_COLOR, INITIAL_POPULATION_SIZE, INITIAL_AMOUNT_FOOD


class Simulation:
    def __init__(self, config):
        pygame.init()
        self.screen = Screen()
        self.neat_population = None
        self.water = []
        self.food = Food.create_food(self.water)
        self.population = None
        self.config = config
        self.current_best_robot = None

    def create_population_from_genomes(self, genomes, new_gen):
        agents = []
        space_between_agents = 40
            #round((WORLD_WIDTH/len(genomes))/SCALE_FACTOR)*SCALE_FACTOR
        random.shuffle(genomes)

        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent()
            agent.x = space_between_agents * i
            agent.y = WORLD_HEIGHT / 2
            agent.q = random.random()
            agent.genome = genome
            agent.genome.fitness = 0 if genome.fitness is None or new_gen else genome.fitness
            agent.nn = neat.nn.RecurrentNetwork.create(genome, config)
            agents.append(agent)
        return agents

    def create_winner_agent_from_genome(self, genome):
        agent = Agent()
        agent.x = WORLD_WIDTH/2
        agent.y = WORLD_HEIGHT/2
        agent.genome = genome
        agent.genome.fitness = 0
        agent.nn = neat.nn.FeedForwardNetwork.create(genome, config)
        return agent

    def reset_for_next_gen(self, genomes, new_gen=True):
        self.food = Food.create_food(self.water)
        if type(genomes) == list:
            self.population = self.create_population_from_genomes(genomes, new_gen)
        else:
            self.population = [self.create_winner_agent_from_genome(genomes)]

        self.timestep = 0
        self.timesteps_without_progress = 0
        self.robots_alive = len(self.population)


    def simulate(self, genomes, draw: bool = True):
        self.reset_for_next_gen(genomes, True)

        for iteration in range(6):
            self.reset_for_next_gen(genomes, False)

            while self.timestep < 10000 and self.timesteps_without_progress < 200 and self.robots_alive > 0:
                self.timestep += 1
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                #SIMULATION
                for agent in self.population:
                    if agent.out_of_bounds:
                        continue

                    new_pos = agent.move(self)
                    #agent.genome.fitness -= 1
                    #HITS FOOD
                    if new_pos in self.food:
                        self.timesteps_without_progress = 0
                        agent.genome.fitness += self.food[new_pos].energy
                        self.food.pop(new_pos)

                    list_without_self = list(filter(lambda a: a.out_of_bounds is False, self.population))
                    list_without_self.remove(agent)
                    if new_pos in set([a.get_center_coord() for a in list_without_self]):
                        agent.out_of_bounds = True
                        self.robots_alive -= 1
                        continue

                    #HITS OTHER ROBOT OR OUT OF BOUNDS
                    if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                        #agent.genome.fitness -= 10
                        agent.out_of_bounds = True
                        self.robots_alive -= 1
                        continue

                self.timesteps_without_progress += 1

                if draw and iteration > 4:
                    rank_of_robots = sorted(self.population, key=lambda x: x.genome.fitness, reverse=True)
                    best_robot = rank_of_robots[0] if len(rank_of_robots) > 0 else Agent()
                    self.screen.update_display(best_robot, self.timestep, self.food, self.population, self.neat_population.generation)

        for a in self.population:
            a.genome.fitness = a.genome.fitness / 5

    def simulate_winner(self, genome):
        self.reset_for_next_gen(genome, True)
        input("Press enter to see winner..")

        while self.timestep < 10000 and self.timesteps_without_progress < 200 and self.robots_alive > 0:
            self.timestep += 1
            # TO QUIT PYGAME
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # SIMULATION
            for agent in self.population:
                if agent.out_of_bounds:
                    continue

                new_pos = agent.move(self)
                # agent.genome.fitness -= 1
                # HITS FOOD
                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                list_without_self = list(filter(lambda a: a.out_of_bounds is False, self.population))
                list_without_self.remove(agent)
                if new_pos in set([a.get_center_coord() for a in list_without_self]):
                    agent.out_of_bounds = True
                    self.robots_alive -= 1
                    continue

                # HITS OTHER ROBOT OR OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    #agent.genome.fitness -= 1000
                    agent.out_of_bounds = True
                    self.robots_alive -= 1
                    continue

            self.timesteps_without_progress += 1

            rank_of_robots = sorted(self.population, key=lambda x: x.genome.fitness, reverse=True)
            best_robot = rank_of_robots[0] if len(rank_of_robots) > 0 else Agent()
            self.screen.update_display(best_robot, self.timestep, self.food, self.population,
                                       self.neat_population.generation)


    def eval_genomes(self, genomes, config):
        self.simulate(genomes, False)


    def run_neat(self, population = None):
        #self.neat_population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-999')

        self.neat_population = neat.Population(self.config)
        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(neat.Checkpointer(100))
        if population != None:
            self.neat_population.population = population

        winner = self.neat_population.run(self.eval_genomes, rounds_to_run)
        self.simulate_winner(winner)

        print(winner)
        return winner



if __name__ == "__main__":
    config_path = "/Users/emilknudsen/Desktop/research/Simple/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    simulation = Simulation(config)
    rounds_to_run = 300
    simulation.run_neat()


    # tenbest = []
    # for i in range(rounds_to_run):
    #     tenbest.append(simulation.run_neat())
    #
    # simulation.run_neat(tenbest)


