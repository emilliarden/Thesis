import copy
import pygame
import pickle

from Classes.food import Food, FoodCreater
from Classes.screen import Screen
from Classes.agent import Agent
from Classes.constants import Constants


class SimulationSingle:
    def __init__(self, constants, neat_population, config):
        pygame.init()
        self.constants = constants
        self.screen = Screen(self.constants)
        self.neat_population = neat_population
        self.original_food = self.constants.FOOD_DICT
        self.original_water = self.constants.WATER_DICT
        self.water = dict.copy(self.original_water)
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.best_agents_fitness = -1
        self.best_agents_fitness_last_gen = -1
        self.best_agent_changed = False

    def create_population_from_genomes(self, genomes):
        agents = []
        genomes = sorted(genomes, key=lambda x: 0 if x[1].fitness is None else x[1].fitness, reverse=True)
        self.best_agents_fitness_last_gen = 0 if genomes[0][1].fitness is None or all(ele[1].fitness == genomes[0][1].fitness for ele in genomes) else genomes[0][1].fitness
        if self.best_agents_fitness_last_gen > self.best_agents_fitness:
            self.best_agents_fitness = self.best_agents_fitness_last_gen
            self.best_agent_changed = True
        else:
            self.best_agent_changed = False



        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent(genome=genome, constants=self.constants, config=self.config)
            agent.genome.fitness = 0
            agents.append(agent)
        return agents

    def reset_gen(self):
        self.food = copy.copy(self.original_food)

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes)
        for i, agent in enumerate(self.population):
            self.reset_gen()
            while agent.timesteps_alive < self.constants.WORLD_SQUARES + self.constants.ALLOWED_MOVES_WITHOUT_PROGRESS and len(self.food) > 0 and not agent.out_of_bounds:
            #while agent.energy > 0 and len(self.food) > 0 and not agent.out_of_bounds:
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                # SIMULATION-----------------------------------------------------------------------------
                new_pos = agent.move(self)

                # CHECK IF MOVE GATHERS FOOD
                if new_pos in self.food:
                    agent.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    if agent.energy < self.constants.ALLOWED_MOVES_WITHOUT_PROGRESS:
                        agent.energy += 1

                    self.food.pop(new_pos)

                if new_pos in self.water:
                    agent.out_of_bounds = True

                # CHECK IF MOVE IS OUT OF BOUNDS
                if (new_pos[0] > self.constants.WORLD_WIDTH or new_pos[0] < 0 or
                    new_pos[1] > self.constants.WORLD_HEIGHT or new_pos[1] < 0) or \
                        agent.energy < 1:
                    agent.out_of_bounds = True



                # DRAW
                if self.constants.DRAW and i == 0 and (self.best_agent_changed or self.neat_population.generation % 100 == 0):
                    self.screen.update_display(agent, agent.timesteps_alive, self.food, self.water, [agent],
                                               self.neat_population.generation)

                # INCREMENT TIMESTEPS
                agent.timesteps_alive += 1
                agent.timesteps_without_progress += 1
                agent.energy -= 1
                #agent.genome.fitness += 0.1



    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def simulate(self, rounds_to_run=None):
        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, rounds_to_run)
        return winner
