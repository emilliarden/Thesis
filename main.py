import pickle
import shutil
import os

from Classes.population_creator import get_population_and_config_and_stats
from Classes.food import Food, Food_Creater
from Classes.constants import Constants, FoodDistribution, StartMode, SensingMode, StartType
from Classes.simulation_single import SimulationSingle
from Classes.simulation_competition import SimulationCompetition


def create_pop_and_find_winner(constants, rounds_to_run=None):
    neat_population, config, stats = get_population_and_config_and_stats(constants,
                                                                         '/Users/emilknudsen/Desktop/research/Statistics/Full_Arena/config_fs_neat_nohidden/winner8.pkl')

    if constants.START_TYPE == StartType.Single:
        simulation = SimulationSingle(constants, neat_population, config)
    elif constants.START_TYPE == StartType.Competition:
        simulation = SimulationCompetition(constants, neat_population, config)

    best_genome = simulation.simulate(rounds_to_run=rounds_to_run)

    stats.save()

    print("winner: " + str(best_genome))
    with open("winner.pkl", "wb") as f:
        pickle.dump(best_genome, f)
        f.close()


def move_and_delete_files(index):
    # Move winner Genome
    src_path = "winner.pkl"
    dst_path = r"Statistics/Unfull_Arena/80_percent/TrainedOnFull/fs_neat_nohidden/winner" + str(index) + ".pkl"
    shutil.move(src_path, dst_path)

    # Move stats
    src_path = "fitness_history.csv"
    dst_path = r"Statistics/Unfull_Arena/80_percent/TrainedOnFull/fs_neat_nohidden/fitness_history" + str(index) + ".csv"
    shutil.move(src_path, dst_path)

    # Remove unnecessary files
    #os.remove("species_fitness.csv")
    #os.remove("speciation.csv")



if __name__ == "__main__":
    start_mode = StartMode.Winner
    start_type = StartType.Single
    sensing_mode = SensingMode.Box
    food_distribution = FoodDistribution.Unfull_80
    draw = False

    constants = Constants(draw=draw, sensing_mode=sensing_mode, start_mode=start_mode,
                          food_distribution=food_distribution, start_type=start_type)

    for i in range(10):
        create_pop_and_find_winner(constants=constants, rounds_to_run=1000)
        move_and_delete_files(i)


