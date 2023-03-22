import copy
import neat
import pygame
import pickle
from configparser import ConfigParser

from population_creator import create_population
from Simple.Classes.food import Food
from Simple.Classes.screen import Screen
from Simple.Classes.agent import Agent
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, FoodDistribution, WORLD_SQUARES, StartMode, SensingMode, \
    get_number_of_inputs


class Simulation:
    def __init__(self, config, food):
        pygame.init()
        self.screen = Screen()
        self.neat_population = None
        self.water = []
        self.original_food = food
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.current_best_genome = None
        self.current_best_genome_changed = False

    def create_population_from_genomes(self, genomes, new_gen):
        agents = []
        self.current_best_genome_changed = False
        for genome in genomes:
            genome[1].fitness = 0 if genome[1].fitness is None else genome[1].fitness
            if self.current_best_genome is None or genome[1].fitness > self.current_best_genome.fitness:
                self.current_best_genome = copy.copy(genome[1])
                self.current_best_genome_changed = True

        genomes = sorted(genomes, key=lambda x: x[1].fitness, reverse=True)
        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent(genome, config, sensing_mode)
            agent.genome.fitness = 0 if genome.fitness is None or new_gen else genome.fitness
            agents.append(agent)
        return agents

    def reset_gen(self, new_food):
        self.timestep = 0
        self.timesteps_without_progress = 0
        if new_food:
            self.original_food = Food.get_food_from_food_distribution(food_distribution)
        self.food = copy.copy(self.original_food)

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes, True)
        self.reset_gen(True)
        for i, agent in enumerate(self.population):
            self.reset_gen(False)
            while self.timestep < WORLD_SQUARES and len(self.food) > 0:
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

    # SIMULATION-----------------------------------------------------------------------------
                # CHECK IF AGENT OUT OF BOUNDS
                if agent.timesteps_without_progress > 100:
                    agent.out_of_bounds = True
                    agent.genome.fitness -= agent.genome.fitness * (self.timestep/WORLD_SQUARES)


                if agent.out_of_bounds:
                    break

                # MOVE AGENT
                new_pos = agent.move(self)
                # if new_pos not in agent.py.visited_squares:
                #     agent.py.genome.fitness += 0.1
                # else:
                #     agent.py.genome.fitness += -0.1

                # agent.py.visited_squares.add(new_pos)

                # CHECK IF MOVE GATHERS FOOD
                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                # CHECK IF MOVE IS OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    agent.genome.fitness -= agent.genome.fitness * (self.timestep/WORLD_SQUARES)
                    #agent.py.genome.fitness = 0

                # DRAW
                if draw and i == 0:
                    self.screen.update_display(agent, self.timestep, self.food, [agent],
                                               self.neat_population.generation)

                # INCREMENT TIMESTEPS
                self.timestep += 1
                self.timesteps_without_progress += 1
                agent.timesteps_alive += 1
                agent.timesteps_without_progress += 1
                agent.genome.fitness += 0.1

    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def run_neat(self):
        if run == StartMode.New:
            self.neat_population = neat.Population(self.config)
        elif run == StartMode.Winner:
            self.neat_population = create_population(self.config, food, 'test-')
        else:
            self.neat_population = neat.Checkpointer.restore_checkpoint('random_food_random_pos-1413')
            self.neat_population.config.fitness_threshold = fitness_threshold

        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(neat.Checkpointer(filename_prefix=file_prefix, generation_interval=10))

        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, 500)

        stats.save()

        print("winner: " + str(winner))
        with open(file_prefix + "winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        return winner


if __name__ == "__main__":
    sensing_mode = SensingMode.Box
    draw = False
    run = StartMode.New
    number_of_inputs = get_number_of_inputs(sensing_mode)

    food_distribution = FoodDistribution.Full
    food = Food.get_food_from_food_distribution(food_distribution)
    fitness_threshold = len(food)


    file_prefix = "random_food_random_pos-"
    config_path = "/Users/emilknudsen/Desktop/research/Simple/config.txt"
    config_parser = ConfigParser()
    config_parser.read(config_path)
    config_parser.set("DefaultGenome", "num_inputs", str(number_of_inputs))
    #config_parser.set("DefaultGenome", "num_hidden", str(int(number_of_inputs/2)))
    config_parser.set("NEAT", "fitness_threshold", str(fitness_threshold))
    with open(config_path, "w+") as f:
        config_parser.write(f)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    simulation = Simulation(config, food)
    simulation.run_neat()
