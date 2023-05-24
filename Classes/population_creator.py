import glob

import neat
import pickle
from itertools import count
from copy import deepcopy
from configparser import ConfigParser
from Classes.constants import Constants, StartMode


def get_population_and_config_and_stats(constants, file_to_create_pop_from="", multi_heuristic=False):
    print(f"Creating and updating config!")

    print(f"Finding genome with fitness: " + str(constants.FITNESS_THRESH))
    print(f"And with allowed moves without progress: " + str(constants.ALLOWED_MOVES_WITHOUT_PROGRESS))
    config_parser = ConfigParser()
    config_parser.read(constants.CONFIG_PATH)
    config_parser.set("DefaultGenome", "num_inputs", str(constants.NUM_INPUTS))
    config_parser.set("NEAT", "fitness_threshold", str(constants.FITNESS_THRESH))
    config_parser.set("NEAT", "pop_size", str(constants.POPULATION_SIZE))
    with open(constants.CONFIG_PATH, "w+") as f:
        config_parser.write(f)


    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         constants.CONFIG_PATH)


    print(f"Creating population!")
    if constants.START_MODE == StartMode.New:
        neat_population = neat.Population(config)
    elif constants.START_MODE == StartMode.Winner:
        neat_population = create_pop_from_pkl(config, file_to_create_pop_from, multi_heuristic=multi_heuristic)
    else:
        neat_population = neat.Checkpointer.restore_checkpoint(file_to_create_pop_from)
        neat_population.config.fitness_threshold = constants.FITNESS_THRESH

    neat_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_population.add_reporter(stats)
    neat_population.add_reporter(neat.Checkpointer(filename_prefix=constants.FILE_PREFIX, generation_interval=100))

    return neat_population, config, stats


def create_pop_from_pkl(config, pkl_path, multi_heuristic):
    print(f"Load the last best network!")
    p = neat.Population(config, initial_state=(0, 0, 0))
    if not multi_heuristic:
        population = create_pop(config, pkl_path)
    else:
        population = create_pop_multiple_genomes(config, pkl_path)
    species = config.species_set_type(config.species_set_config, p.reporters)
    generation = 0
    species.speciate(config, population, generation)
    p.population = population
    p.species = species
    p.generation = generation

    return p


def create_pop(config, pkl_path):
    with open(pkl_path, "rb") as f:
        genome = pickle.load(f)

    genome_indexer = count(1)
    new_genomes = {}
    for i in range(config.pop_size):
        key = next(genome_indexer)
        tmp_genome = deepcopy(genome)
        tmp_genome.key = key
        new_genomes[key] = tmp_genome
    return new_genomes


def create_pop_multiple_genomes(config, folder_path):
    genome_indexer = count(10)
    new_genomes = {}

    for file in glob.glob(folder_path + '/winner*.pkl'):
        with open(file, "rb") as f:
            genome = pickle.load(f)
        for i in range(5):
            key = next(genome_indexer)
            tmp_genome = deepcopy(genome)
            tmp_genome.key = key
            new_genomes[key] = tmp_genome

    return new_genomes
