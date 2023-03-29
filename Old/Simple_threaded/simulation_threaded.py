import neat
import pickle
from configparser import ConfigParser

from Old.Simple_threaded.population_creator import create_population
from Old.Simple_threaded.Classes.food import Food
from Old.Simple_threaded.Classes.agent import Agent
from Old.Simple_threaded.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, FoodDistribution, WORLD_SQUARES, StartMode, \
    SensingMode, get_number_of_inputs


class Simulation:
    def __init__(self, config, food):
        self.neat_population = None
        self.water = []
        self.original_food = food
        self.food = dict.copy(self.original_food)
        self.population = None
        self.config = config
        self.current_best_genome = None
        self.current_best_genome_changed = False

    def simulate_one_at_a_time(self, genome, config):
        f = Food.get_food_from_food_distribution(food_distribution)
        agent = Agent(genome, config, f, sensing_mode)
        while agent.timesteps_alive < WORLD_SQUARES and len(agent.food) > 0:
        # SIMULATION-----------------------------------------------------------------------------
            # CHECK IF AGENT OUT OF BOUNDS
            if agent.timesteps_without_progress > 100:
                agent.out_of_bounds = True

            if agent.out_of_bounds:
                break



            # MOVE AGENT
            new_pos = agent.move()

            # CHECK IF MOVE GATHERS FOOD
            if new_pos in agent.food:
                agent.genome.fitness += agent.food[new_pos].energy
                agent.food.pop(new_pos)

            # CHECK IF MOVE IS OUT OF BOUNDS
            if new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                agent.out_of_bounds = True
                #agent.py.genome.fitness = 0

            # INCREMENT TIMESTEPS
            agent.timesteps_alive += 1
            agent.timesteps_without_progress += 1
            agent.genome.fitness += 0.1

        return agent.genome.fitness

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

        pe = neat.ThreadedEvaluator(20, self.simulate_one_at_a_time)
        winner = self.neat_population.run(pe.evaluate, 300)

        stats.save()

        print("winner: " + str(winner))
        with open(file_prefix + "winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        return winner


if __name__ == "__main__":
    sensing_mode = SensingMode.Box
    draw = False
    run = StartMode.Winner
    number_of_inputs = get_number_of_inputs(sensing_mode)

    food_distribution = FoodDistribution.Random
    food = Food.get_food_from_food_distribution(food_distribution)
    fitness_threshold = len(food)

    file_prefix = "random_food-"
    config_path = "/Old/Simple/config.txt"
    config_parser = ConfigParser()
    config_parser.read(config_path)
    config_parser.set("DefaultGenome", "num_inputs", str(number_of_inputs))
    # config_parser.set("DefaultGenome", "num_hidden", str(int(number_of_inputs/2)))
    config_parser.set("NEAT", "fitness_threshold", str(fitness_threshold))
    with open(config_path, "w+") as f:
        config_parser.write(f)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    simulation = Simulation(config, food)
    simulation.run_neat()
