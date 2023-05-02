import copy
import neat
import pygame
import pickle
from configparser import ConfigParser

from Classes.food import Food, FoodCreater
from Classes.screen import Screen
from Classes.competition_agent import CompetitionAgent


class SimulationCompetition:
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


    def create_population_from_genomes(self, genomes):
        agents = []
        genomes = sorted(genomes, key=lambda x: 0 if x[1].fitness is None else x[1].fitness, reverse=True)
        for i, (genome_id, genome) in enumerate(genomes):
            agent = CompetitionAgent(genome=genome, constants=self.constants, config=self.config)
            agent.genome.fitness = 0
            agents.append(agent)
        return agents

    def reset_gen(self):
        self.timestep = 0
        self.food = copy.copy(self.original_food)

    def simulate_one_at_a_time(self, genomes):
        self.population = self.create_population_from_genomes(genomes)
        self.reset_gen()
        while self.timestep < self.constants.WORLD_SQUARES and len(self.food) > 0 and len(self.population) > 0:
            self.timestep += 1
            for i, agent in enumerate(self.population):
                # TO QUIT PYGAME
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

    # SIMULATION-----------------------------------------------------------------------------
                # CHECK IF AGENT OUT OF BOUNDS
                if agent.out_of_bounds:
                    self.population.remove(agent)
                    continue

                # MOVE AGENT
                new_pos = agent.move(self)

                # CHECK IF MOVE GATHERS FOOD
                if new_pos in self.food:
                    agent.timesteps_without_progress = 0
                    agent.genome.fitness += self.food[new_pos].energy
                    agent.energy += 1
                    self.food.pop(new_pos)

                # if new_pos in agent.previous_positions.queue:
                #     agent.genome.fitness -= 1

                # CHECK IF MOVE IS OUT OF BOUNDS
                if (new_pos[0] > self.constants.WORLD_WIDTH or new_pos[0] < 0 or
                    new_pos[1] > self.constants.WORLD_HEIGHT or new_pos[1] < 0) or \
                        agent.energy < 1:
                    agent.out_of_bounds = True
                    break

                # INCREMENT TIMESTEPS
                agent.timesteps_alive += 1
                agent.timesteps_without_progress += 1
                agent.energy -= 1
                # DRAW
            if self.constants.DRAW and len(self.population) > 0:
                self.screen.update_display(self.population[0], self.timestep, self.food, self.water, self.population,
                                           self.neat_population.generation)

    def eval_genomes_one_at_a_time(self, genomes, config):
        self.simulate_one_at_a_time(genomes)

    def simulate(self, rounds_to_run=None):
        winner = self.neat_population.run(self.eval_genomes_one_at_a_time, rounds_to_run)
        return winner

