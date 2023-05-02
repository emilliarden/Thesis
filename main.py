import pickle
import shutil
import os
import glob

from Classes.population_creator import get_population_and_config_and_stats
from Classes.constants import Constants, StartMode, SensingMode, StartType
from Classes.food import FoodDistribution
from Classes.simulation_single import SimulationSingle
from Classes.simulation_competition import SimulationCompetition
from Classes.simulation_1v1 import SimulationIvI


def create_pop_and_find_winner(constants, rounds_to_run=None, winner_file=""):
    neat_population, config, stats = get_population_and_config_and_stats(constants, winner_file)
    if constants.START_TYPE == StartType.Single:
        simulation = SimulationSingle(constants, neat_population, config)
    elif constants.START_TYPE == StartType.Competition:
        simulation = SimulationCompetition(constants, neat_population, config)
    elif constants.START_TYPE == StartType.IvI:
        simulation = SimulationIvI(constants, neat_population, config)

    try:
        best_genome = simulation.simulate(rounds_to_run=rounds_to_run)
        print("winner: " + str(best_genome))
        with open("winnerCross.pkl", "wb") as f:
            pickle.dump(best_genome, f)
            f.close()

    finally:
        stats.save()




def move_and_delete_files(filename):
    # Move winner Genome
    if os.path.exists("winner.pkl"):
        src_path = "winner.pkl"
        dst_path = r"Statistics/Unfull_Arena/20_percent/New/fs_neat/winner" + str(filename) + ".pkl"
        shutil.move(src_path, dst_path)

    # Move stats
    src_path = "fitness_history.csv"
    dst_path = r"Statistics/Unfull_Arena/20_percent/New/fs_neat/fitness_history" + str(filename) + ".csv"
    shutil.move(src_path, dst_path)

    # Remove unnecessary files
    os.remove("species_fitness.csv")
    os.remove("speciation.csv")



if __name__ == "__main__":
    start_mode = StartMode.New
    start_type = StartType.Single
    sensing_mode = SensingMode.BoxDiff
    food_distribution = FoodDistribution.Unfull_20
    draw = True

    constants = Constants(draw=draw, sensing_mode=sensing_mode, start_mode=start_mode,
                          food_distribution=food_distribution, start_type=start_type)

    #create_pop_and_find_winner(constants=constants, rounds_to_run=5000, winner_file='')
    #exit(0)
    #counter = 0

    #for file in glob.glob("Statistics/Unfull_Arena/40_percent/TrainedOn60/fs_neat/*.pkl"):
    for i in range(5):
        try:
            create_pop_and_find_winner(constants=constants, rounds_to_run=5000, winner_file='')
        finally:
            move_and_delete_files(i)
        #counter += 1




