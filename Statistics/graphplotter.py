import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import glob

from Classes.constants import Constants
from Classes.food import FoodDistribution
from visualize import draw_net, draw_net_without_all_nodes
import neat
import pickle


def get_amount_of_lines_to_shift(filename):
    number_to_look_for = 0
    for i in filename:
        if i.isdigit():
            number_to_look_for = number_to_look_for * 10 + int(i)

    pathToPreviousFile = '/Users/emilknudsen/Desktop/research/Statistics/Full_Arena/fs_neat/middle/fitness_history' + str(
        number_to_look_for) + '.csv'
    df = pd.read_csv(pathToPreviousFile, usecols=[0], sep=' ')
    return len(df.index)


def create_df_with_mean_and_stddev(folder):
    files = glob.glob(folder + "/*.csv")

    column_names_full = []
    for i in range(1, len(files) + 1):
        column_names_full.append('Run ' + str(i - 1))

    new_list = []
    for filename in files:
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        new_list.append(df)

    # full_direct -----------------------------------------------------
    new_frame = pd.concat(new_list, axis=1, ignore_index=True)
    new_frame.fillna(method='ffill', inplace=True)
    standard_deviation = new_frame.std(axis=1)
    new_frame['Mean'] = new_frame.mean(axis=1)
    new_frame['Standard deviation'] = standard_deviation

    return new_frame


def compare_two_runs(new_folder, pretrained_folder, random_folder, constants):
    mean_finishing_point_for_successfull_runs = 559  # 558,4

    new_dataframe = create_df_with_mean_and_stddev(new_folder)
    pretrained_dataframe = create_df_with_mean_and_stddev(pretrained_folder)
    random_dataframe = create_df_with_mean_and_stddev(random_folder)

    data_frames = [new_dataframe, pretrained_dataframe, random_dataframe]
    # NEW, PRETRAINED, RANDOM COLORS:
    colors = [('#CC4F1B', '#FF9848'), ('#1B2ACC', '#089FFF'), ('#3F7F4C', '#7EFF99')]
    labels = ['Direct', 'Incremental (base case)', 'Random']

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    for i, df in enumerate(data_frames):
        x = list(range(0, len(df['Mean']))) if i == 0 or i == 2 else list(
            range(mean_finishing_point_for_successfull_runs,
                  mean_finishing_point_for_successfull_runs + len(df['Mean'])))
        y = df['Mean']
        std_dev = df['Standard deviation']

        if i != 2:
            plt.plot(x, y, color=colors[i][0], label=labels[i])
            plt.fill_between(x=x,
                             y1=y - std_dev,
                             y2=y + std_dev,
                             alpha=0.5, edgecolor=colors[i][0], facecolor=colors[i][1])

    # ---------------------------------------------------
    title = "50% Environment"
    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title(title, fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="lower right")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(14, 8)
    plt.savefig("Environment_graphs/" + title + ".svg")
    plt.savefig("Environment_graphs/" + title + ".png")
    plt.show()


def show_all_runs(new_folder, pretrained_folder, random_folder, constants):
    new_files = glob.glob(new_folder + "/*.csv")
    pretrained_files = glob.glob(pretrained_folder + "/*.csv")
    file_random = glob.glob(random_folder + "/*.csv")

    oranges = cm.get_cmap('Oranges')
    blues = cm.get_cmap('Blues')
    random_color = '#3F7F4C'

    # insert random file into dataframe
    # for i, filename in enumerate(file_random):
    #     df = pd.read_csv(filename, usecols=[0], sep=' ')
    #     x = list(range(0, len(df)))
    #     y = df
    #     plt.plot(x, y, color=random_color, label='Random ' + str(i + 1))

    # insert direct files into dataframe
    for i, filename in enumerate(new_files):
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        x = list(range(0, len(df)))
        y = df
        plt.plot(x, y, color=oranges(oranges.N - (20 * i)), label='Direct ' + str(i + 1))

    # insert random file into dataframe
    for i, filename in enumerate(pretrained_files):
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        lines_to_shift = get_amount_of_lines_to_shift(filename)
        x = list(range(lines_to_shift, lines_to_shift + len(df)))
        y = df
        plt.plot(x, y, color=blues(blues.N - (20 * i)), label='Incremental ' + str(i + 1))

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    title = "50% Environment"

    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title(title, fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="lower right")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(14, 8)
    plt.savefig("Environment_graphs/" + title + ".svg")
    plt.savefig("Environment_graphs/" + title + ".png")
    plt.show()



def create_genome_graph(winner_file, filename):
    # create genome from pkl
    with open(winner_file, "rb") as f:
        genome = pickle.load(f)

    # get config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         '/Users/emilknudsen/Desktop/research/config.txt')

    draw_net_without_all_nodes(config, genome, view=True, show_disabled=False, filename=filename)


if __name__ == "__main__":
    constants = Constants(None, None, FoodDistribution.HalfFull, None, None)

    show_all_runs('/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/HalfFull/New',
                     '/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/HalfFull/TrainedOnFullMiddle',
                     '/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/SpaceBetweenFood/Random',
                     constants)
    # create_df_with_mean_and_stddev('/Users/emilknudsen/Desktop/research/Statistics/Full_Arena/fs_neat/topleft')

    # compare_neat_with_full_fullarena()
    # base_case_all_runs()
    # create_genome_graph('/Users/emilknudsen/Desktop/research/winner.pkl', filename="test")
