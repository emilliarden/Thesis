import random
import neat
from neat.reporting import ReporterSet
import pygame
import pickle

from Simple.Classes.food import Food
from Simple.Classes.screen import Screen
from Simple.Classes.agent import Agent
from Simple.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH, WATER_COLOR, FOOD_COLOR, FOOD2_COLOR, \
    TEXT_COLOR, BACKGROUND_COLOR, INITIAL_POPULATION_SIZE, INITIAL_AMOUNT_FOOD, SENSING_DISTANCE


class Simulation:
    def __init__(self, config):
        pygame.init()
        self.screen = Screen()
        self.neat_population = None
        self.water = []
        self.original_food = Food.create_food(self.water) if normal_food_distribution else Food.create_random_food(
            self.water)
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.current_best_robot = None

    def create_population_from_genomes(self, genomes, new_gen):
        agents = []
        for genome in genomes:
            genome[1].fitness = 0 if genome[1].fitness is None else genome[1].fitness
        genomes = sorted(genomes, key=lambda x: x[1].fitness, reverse=True)
        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent()
            # agent.x = round(random.randint(0, WORLD_WIDTH) / SCALE_FACTOR) * SCALE_FACTOR
            agent.x = WORLD_WIDTH / 2
            agent.y = WORLD_HEIGHT / 2
            agent.genome = genome
            agent.genome.fitness = 0 if genome.fitness is None or new_gen else genome.fitness
            agent.nn = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(agent)
        return agents

    def create_winner_agent_from_genome(self, genome):
        agent = Agent()
        agent.x = WORLD_WIDTH / 2
        agent.y = WORLD_HEIGHT / 2
        agent.genome = genome
        agent.genome.fitness = 0
        agent.nn = neat.nn.FeedForwardNetwork.create(genome, config)
        return [agent]

    def reset_for_next_gen(self, genomes, new_gen=True):
        # self.population = self.create_population_from_genomes(genomes, new_gen)
        self.timestep = 0
        self.timesteps_without_progress = 0
        # self.robots_alive = len(self.population)
        self.food = dict.copy(self.original_food)

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes, True)
        for i, agent in enumerate(self.population):
            self.reset_for_next_gen(genomes, False)
            while self.timestep < 5000 and self.timesteps_without_progress < 500:
                if agent.out_of_bounds:
                    break

                self.timestep += 1
                self.timesteps_without_progress += 1

                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        checkpointer = neat.Checkpointer()
                        checkpointer.save_checkpoint(config=config, population=self.neat_population,
                                                     species_set=self.neat_population.species,
                                                     generation=self.neat_population.generation)
                        quit()

                # SIMULATION
                new_pos = agent.move(self)

                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                # HITS OTHER ROBOT OR OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    #agent.genome.fitness += -100

                if draw and i == 0:
                    self.screen.update_display(agent, self.timestep, self.food, [agent],
                                               self.neat_population.generation)
                    x = 42



    def simulate_winner(self, genome):
        self.population = self.create_winner_agent_from_genome(genome)
        input("Press enter to see winner..")

        for agent in self.population:

            while self.timestep < 5000 and self.timesteps_without_progress < 500:
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                if agent.out_of_bounds:
                    break
                # SIMULATION
                self.timestep += 1
                self.timesteps_without_progress += 1

                new_pos = agent.move(self)

                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                # HITS OTHER ROBOT OR OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True

                self.screen.update_display(agent, self.timestep, self.food, [agent],
                                               self.neat_population.generation)

    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def run_neat(self):
        if new_run:
            self.neat_population = neat.Population(self.config)
        else:
            self.neat_population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-399')

        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(neat.Checkpointer(100))

        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, rounds_to_run)
        #print("winner: " + str(winner))
        with open("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        with open("winner.pkl", "rb") as f:
            genome = pickle.load(f)

        self.simulate_winner(genome)

        return winner
        quit()


if __name__ == "__main__":
    config_path = "/Users/emilknudsen/Desktop/research/Simple/test_config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    normal_food_distribution = False
    config.fitness_threshold = INITIAL_AMOUNT_FOOD*0.8 if not normal_food_distribution else ((WORLD_WIDTH/SCALE_FACTOR)*(WORLD_HEIGHT/SCALE_FACTOR))*0.8
    #config.fitness_threshold = 25
    rounds_to_run = 200000
    draw = True
    new_run = False

    simulation = Simulation(config)
    simulation.run_neat()
