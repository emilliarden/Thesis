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
        self.original_food = Food.create_food_following_sinus(self.water) if random_food_distribution else Food.create_food(self.water)
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.current_best_genome = None
        self.current_best_genome_changed = False

    def create_population_from_genomes(self, genomes, new_gen):
        agents = []
        for genome in genomes:
            genome[1].fitness = 0 if genome[1].fitness is None else genome[1].fitness
            if self.current_best_genome is None or genome[1].fitness > self.current_best_genome.fitness:
                self.current_best_genome = genome[1]
                self.current_best_genome_changed = True
            else:
                self.current_best_genome_changed = False

        genomes = sorted(genomes, key=lambda x: x[1].fitness, reverse=True)
        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent()
            #agent.x = round(random.randint(0, WORLD_WIDTH) / SCALE_FACTOR) * SCALE_FACTOR
            #agent.y = round(random.randint(0, WORLD_HEIGHT) / SCALE_FACTOR) * SCALE_FACTOR
            agent.x = WORLD_WIDTH / 2
            agent.y = WORLD_HEIGHT / 2
            agent.genome = genome
            agent.genome.fitness = 0 if genome.fitness is None or new_gen else genome.fitness
            agent.nn = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
            agents.append(agent)
        return agents

    def create_winner_agent_from_genome(self, genome):
        agent = Agent()
        agent.x = WORLD_WIDTH / 2
        agent.y = WORLD_HEIGHT / 2
        agent.genome = genome
        agent.genome.fitness = 0
        agent.nn = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        return [agent]

    def reset_gen(self, genomes, new_gen=True):
        # self.population = self.create_population_from_genomes(genomes, new_gen)
        self.timestep = 0
        self.timesteps_without_progress = 0
        # self.robots_alive = len(self.population)
        self.food = dict.copy(self.original_food)
        # self.food = Food.create_random_food([])

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes, True)
        for i, agent in enumerate(self.population):
            self.reset_gen(genomes, False)
            while self.timestep < len(self.original_food) and len(self.food) > 0:
                if agent.out_of_bounds:
                    break

                self.timestep += 1
                self.timesteps_without_progress += 1
                agent.timesteps_alive += 1


                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                # SIMULATION
                new_pos = agent.move(self)


                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                if agent.timesteps_without_progress > 100:
                    agent.out_of_bounds = True

                # HITS OTHER ROBOT OR OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    agent.genome.fitness = 0

                if draw and i == 0:
                    self.screen.update_display(agent, self.timestep, self.food, [agent],
                                               self.neat_population.generation)
                    x = 42

    def simulate_winner(self, genome):
        self.population = self.create_winner_agent_from_genome(genome)
        input("Press enter to see winner..")

        for agent in self.population:
            self.reset_gen([genome], False)
            while self.timestep < 5000 and self.timesteps_without_progress < 100:
                if agent.out_of_bounds:
                    break

                self.timestep += 1
                self.timesteps_without_progress += 1
                agent.timesteps_alive += 1
                agent.timesteps_without_progress += 1

                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                # SIMULATION
                new_pos = agent.move(self)
                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                # HITS OTHER ROBOT OR OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    agent.genome.fitness = 0

                self.screen.update_display(agent, self.timestep, self.food, [agent],
                                           self.neat_population.generation)

    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def run_neat(self):
        if new_run:
            self.neat_population = neat.Population(self.config)
        else:
            self.neat_population = neat.Checkpointer.restore_checkpoint('test-978')

        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(
            neat.Checkpointer(filename_prefix=file_prefix, generation_interval=1))

        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, rounds_to_run)

        print("winner: " + str(winner))
        with open(file_prefix + "winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        with open(file_prefix + "winner.pkl", "rb") as f:
            genome = pickle.load(f)

        self.simulate_winner(genome)

        return winner


if __name__ == "__main__":
    file_prefix = "test-"

    config_path = "/Users/emilknudsen/Desktop/research/Simple/test_config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    random_food_distribution = True
    config.fitness_threshold = INITIAL_AMOUNT_FOOD if random_food_distribution else ((WORLD_WIDTH / SCALE_FACTOR) * (WORLD_HEIGHT / SCALE_FACTOR))
    #config.fitness_threshold = 1000
    rounds_to_run = 200000
    draw = True
    new_run = False

    simulation = Simulation(config)
    simulation.run_neat()
