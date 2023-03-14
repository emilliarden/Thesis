import copy
import neat
import pygame
import pickle

from population_creator import create_population
from Simple.Classes.food import Food
from Simple.Classes.screen import Screen
from Simple.Classes.agent import Agent
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, FoodDistribution, WORLD_SQUARES, StartMode


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
            agent = Agent(genome, config)
            agent.genome.fitness = 0 if genome.fitness is None or new_gen else genome.fitness
            agents.append(agent)
        return agents

    def create_winner_agent_from_genome(self, genome):
        agent = Agent(genome, config)
        agent.genome = genome
        agent.genome.fitness = 0
        agent.nn = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        return [agent]

    def reset_gen(self):
        self.timestep = 0
        self.timesteps_without_progress = 0
        self.food = dict.copy(self.original_food)

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes, True)
        for i, agent in enumerate(self.population):
            self.reset_gen()
            while self.timestep < WORLD_SQUARES and len(self.food) > 0:
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

    # SIMULATION-----------------------------------------------------------------------------
                # CHECK IF AGENT OUT OF BOUNDS
                if agent.timesteps_without_progress > 100:
                    agent.out_of_bounds = True

                if agent.out_of_bounds:
                    break

                # MOVE AGENT
                new_pos = agent.move(self)

                # CHECK IF MOVE GATHERS FOOD
                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    agent.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                # CHECK IF MOVE IS OUT OF BOUNDS
                if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    agent.genome.fitness = 0

                # DRAW
                if draw and i == 0:
                    self.screen.update_display(agent, self.timestep, self.food, [agent],
                                               self.neat_population.generation)
                    x = 42

                # INCREMENT TIMESTEPS
                self.timestep += 1
                self.timesteps_without_progress += 1
                agent.timesteps_alive += 1
                agent.timesteps_without_progress += 1

    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def run_neat(self):
        if run == StartMode.New:
            self.neat_population = neat.Population(self.config)
        elif run == StartMode.Winner:
            self.neat_population = create_population(self.config, food, 'test-')
        else:
            self.neat_population = neat.Checkpointer.restore_checkpoint('test-1867')

        self.neat_population.config.fitness_threshold = fitness_threshold
        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(neat.Checkpointer(filename_prefix=file_prefix, generation_interval=10))

        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, None)

        stats.save()

        print("winner: " + str(winner))
        with open(file_prefix + "winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        return winner


if __name__ == "__main__":
    file_prefix = "test-"
    config_path = "/Users/emilknudsen/Desktop/research/Simple/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    food_distribution = FoodDistribution.Full

    food = Food.get_food_from_food_distribution(food_distribution)
    fitness_threshold = len(food) - 10
    config.fitness_threshold = fitness_threshold
    draw = True
    run = StartMode.Winner

    simulation = Simulation(config, food)
    simulation.run_neat()
