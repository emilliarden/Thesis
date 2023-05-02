import copy
import pygame
import pickle

from Classes.food import Food, FoodCreater
from Classes.screen import Screen
from Classes.competition_agent import CompetitionAgent
from Classes.constants import Constants

class SimulationIvI:
    def __init__(self, constants, neat_population, config):
        self.constants = constants
        self.screen = Screen(self.constants)
        self.neat_population = neat_population
        self.original_food = self.constants.FOOD_DICT
        self.original_water = self.constants.WATER_DICT
        self.water = dict.copy(self.original_water)
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.best_agent_genome = None
        self.best_agent = None
        self.timestep = 0

    def create_best_agent_from_genome(self, best_agent_genome):
        agent = CompetitionAgent(genome=best_agent_genome, constants=self.constants, config=self.config)
        agent.genome.fitness = 0
        agent.x = 0
        agent.y = self.constants.WORLD_HEIGHT/2 + self.constants.SCALE_FACTOR/2
        return agent

    def create_population_from_genomes(self, genomes):
        agents = []
        genomes = sorted(genomes, key=lambda x: 0 if x[1].fitness is None else x[1].fitness, reverse=True)

        for i, (genome_id, genome) in enumerate(genomes):
            agent = CompetitionAgent(genome=genome, constants=self.constants, config=self.config)
            agent.genome.fitness = 0
            agent.x = 0
            agent.y = self.constants.WORLD_HEIGHT/2 - self.constants.SCALE_FACTOR/2
            agents.append(agent)

        return agents

    def reset_gen(self):
        self.food = copy.copy(self.original_food)
        self.timestep = 0
        self.best_agent = self.create_best_agent_from_genome(self.best_agent_genome)

    def simulate_IvI(self, genomes):
        agents_won_against_best = []
        self.population = self.create_population_from_genomes(genomes)
        for i, agent in enumerate(self.population):
            self.reset_gen()
            IvI_pop = [agent, self.best_agent]
            while self.timestep < self.constants.WORLD_SQUARES and len(self.food) > 0 and len(IvI_pop) > 0:
                self.timestep += 1
                for a in IvI_pop:
                    # TO QUIT PYGAME
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()

                    if a.out_of_bounds:
                        IvI_pop.remove(a)

                    # SIMULATION-----------------------------------------------------------------------------
                    new_pos = a.move(self)


                    # CHECK IF MOVE GATHERS FOOD
                    if new_pos in self.food:
                        a.genome.fitness += self.food[new_pos].energy
                        a.energy += 1
                        self.food.pop(new_pos)

                    if new_pos in self.water:
                        a.out_of_bounds = True

                    # CHECK IF MOVE IS OUT OF BOUNDS
                    if (new_pos[0] > self.constants.WORLD_WIDTH or new_pos[0] < 0 or
                        new_pos[1] > self.constants.WORLD_HEIGHT or new_pos[1] < 0) or \
                            a.energy < 1:
                        a.out_of_bounds = True

                    # DRAW
                    if self.constants.DRAW and len(IvI_pop) > 0 and self.neat_population.generation % 50 == 0:
                        self.screen.update_display(agent, self.timestep, self.food, self.water, IvI_pop,
                                                   self.neat_population.generation)

                    # INCREMENT TIMESTEPS
                    a.timesteps_alive += 1
                    a.energy -= 1
                    #agent.genome.fitness += 0.1
            if agent.genome.fitness > self.best_agent.genome.fitness:
                agents_won_against_best.append(agent)

            if self.constants.DRAW and self.neat_population.generation % 50 == 0:
                print('ROUND: ' + str(i))
                if agent.genome.fitness > self.best_agent.genome.fitness:
                    print('New genome won!')
                else:
                    print('Best agent won!')
                print('Score------')
                print('New genome: ' + str(agent.genome.fitness))
                print('Best genome: ' + str(self.best_agent.genome.fitness))
                print()
                print()

        if len(agents_won_against_best) > 0:
            self.set_new_best_genome(agents_won_against_best)




    def set_new_best_genome(self, agents_won):
        best = None
        for a in agents_won:
            if best is None or best.genome.fitness < a.genome.fitness:
                best = a

        self.best_agent_genome = best.genome
        self.best_agent = self.create_best_agent_from_genome(self.best_agent_genome)

    def eval_genomes(self, genomes, config):
        self.best_agent_genome = genomes[0][1]
        self.best_agent = self.create_best_agent_from_genome(self.best_agent_genome)
        self.simulate_IvI(genomes)

    def simulate(self, rounds_to_run=None):
        winner = self.neat_population.run(self.eval_genomes, rounds_to_run)
        return winner
