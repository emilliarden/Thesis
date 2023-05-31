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


def create_pop_and_find_winner(constants, rounds_to_run=None, winner_file="", multi_heuristic=False):
    neat_population, config, stats = get_population_and_config_and_stats(constants, winner_file, multi_heuristic=multi_heuristic)
    if constants.START_TYPE == StartType.Single:
        simulation = SimulationSingle(constants, neat_population, config)
    elif constants.START_TYPE == StartType.Competition:
        simulation = SimulationCompetition(constants, neat_population, config)
    elif constants.START_TYPE == StartType.IvI:
        simulation = SimulationIvI(constants, neat_population, config)

    try:
        best_genome = simulation.simulate(rounds_to_run=rounds_to_run)
        print("winner: " + str(best_genome))
        with open("winner.pkl", "wb") as f:
            pickle.dump(best_genome, f)
            f.close()

    finally:
        stats.save()


def move_and_delete_files(filename):
    # Move winner Genome
    path = r"/Users/emilknudsen/Desktop/Thesis/Statistics/CatastrophicForgetting/Corners"


    if os.path.exists("winner.pkl"):
        src_path = "winner.pkl"
        dst_path = path + "/winner" + str(filename) + ".pkl"
        shutil.move(src_path, dst_path)

    # Move stats
    src_path = "fitness_history.csv"
    dst_path = path + "/fitness_history" + str(filename) + ".csv"
    shutil.move(src_path, dst_path)

    # Remove unnecessary files
    os.remove("species_fitness.csv")
    os.remove("speciation.csv")



if __name__ == "__main__":
    start_mode = StartMode.Winner
    start_type = StartType.Single
    sensing_mode = SensingMode.BoxDiff
    food_distribution = FoodDistribution.Corners
    draw = True

    constants = Constants(draw=draw, sensing_mode=sensing_mode, start_mode=start_mode,
                          food_distribution=food_distribution, start_type=start_type)

    #create_pop_and_find_winner(constants=constants, rounds_to_run=4000, winner_file='/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/D)CornersWithWater/TrainedOnQuarter/winner6.pkl', multi_heuristic=False)
    #exit(0)

    for file in glob.glob("/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnCornersThenHalfWater/winner*.pkl"):
    #for i in range(10):

        file_length = len(file) - file.rfind('/')
        last_char_in_filename = len(file)-1
        if file_length == 12:
             counter = file[last_char_in_filename-4]
        else:
            counter = file[last_char_in_filename-5] + file[last_char_in_filename-4]
        try:
            create_pop_and_find_winner(constants=constants, rounds_to_run=1, winner_file=file, multi_heuristic=False)
        finally:
            move_and_delete_files(counter)




