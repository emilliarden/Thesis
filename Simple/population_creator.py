import neat
import pickle
from neat.reporting import ReporterSet
from itertools import count
from copy import deepcopy


def create_population(config, food, file_prefix):
    print(f"Load the last best network!")
    p = neat.Population(config, initial_state=(0, 0, 0))
    population = create_pop(config, file_prefix)
    species = config.species_set_type(config.species_set_config, p.reporters)
    generation = 0
    species.speciate(config, population, generation)
    p.population = population
    p.species = species
    p.generation = generation

    return p


def create_pop(config, file_prefix):
    with open("/Users/emilknudsen/Desktop/research/Simple/random_food_random_pos-winner.pkl", "rb") as f:
        genome = pickle.load(f)

    genome_indexer = count(1)
    new_genomes = {}
    for i in range(config.pop_size):
        key = next(genome_indexer)
        tmp_genome = deepcopy(genome)
        tmp_genome.key = key
        new_genomes[key] = tmp_genome
    return new_genomes
