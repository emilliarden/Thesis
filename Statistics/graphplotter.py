import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

from Classes.constants import Constants
from Classes.food import FoodDistribution
from visualize import draw_net, draw_net_without_all_nodes
import neat
import pickle

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
    new_dataframe = create_df_with_mean_and_stddev(new_folder)
    pretrained_dataframe = create_df_with_mean_and_stddev(pretrained_folder)
    random_dataframe = create_df_with_mean_and_stddev(random_folder)

    data_frames = [new_dataframe, pretrained_dataframe, random_dataframe]
    #NEW, PRETRAINED, RANDOM COLORS:
    colors = [('#CC4F1B', '#FF9848'), ('#1B2ACC', '#089FFF'), ('#3F7F4C', '#7EFF99')]
    labels = ['Direct', 'Incremental', 'Random']

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    for i, df in enumerate(data_frames):
        x = list(range(0, len(df)))
        y = df['Mean']
        std_dev = df['Standard deviation']

        plt.plot(x, df['Mean'], color=colors[i][0], label=labels[i])
        plt.fill_between(x=x,
                         y1=y - std_dev,
                         y2=y + std_dev,
                         alpha=0.5, edgecolor=colors[i][0], facecolor=colors[i][1])

    # ---------------------------------------------------
    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title("Spiral environment", fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="center right")
    plt.show()


def show_all_runs_two_folders(new_folder, pretrained_folder, random_folder, constants):
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    new_files = glob.glob(new_folder + "/*.csv")
    pretrained_files = glob.glob(pretrained_folder + "/*.csv")
    file_random = glob.glob(random_folder + "/*.csv")
    shades_of_red = ['#ff0000', '#d70000', '#c60000', '#b70000', '#9b0000', '#ff0000', '#d70000', '#c60000', '#b70000', '#9b0000']
    shades_of_green = ['#22b600', '#26cc00', '#7be382', '#006400', '#009c1a', '#22b600', '#26cc00', '#7be382', '#006400', '#009c1a']
    random_color = '#0000FF'

    color_dict = dict()
    column_names = []

    for i in range(1, len(new_files) + 1):
        column_name = 'New ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_green[i - 1]

    for i in range(1, len(pretrained_files) + 1):
        column_name = 'Pretrained ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_red[i - 1]

    column_name = 'Random'
    column_names.append(column_name)
    color_dict[column_name] = random_color

    li = []
    for filename in new_files + pretrained_files + file_random:
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        li.append(df)

    frame = pd.concat(li, axis=1, ignore_index=True)
    frame.columns = column_names


    print(frame)
    ax = frame.plot(title='', color=color_dict)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    # -----------------------------------------------------
    plt.show()

def create_genome_graph(winner_file, filename):
    #create genome from pkl
    with open(winner_file, "rb") as f:
        genome = pickle.load(f)

    #get config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, '/Users/emilknudsen/Desktop/research/config.txt' )

    draw_net_without_all_nodes(config, genome, view=True, show_disabled=False, filename=filename)


if __name__ == "__main__":
    constants = Constants(None, None, FoodDistribution.SpaceBetweenFood, None, None)

    compare_two_runs('/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/SpaceBetweenFood/New',
                     '/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/SpaceBetweenFood/TrainedOnFullMiddle',
                     '/Users/emilknudsen/Desktop/research/Statistics/Function_Distribution/SpaceBetweenFood/Random',
                     constants)
    #create_df_with_mean_and_stddev('/Users/emilknudsen/Desktop/research/Statistics/Full_Arena/fs_neat/topleft')

    #compare_neat_with_full_fullarena()
    #base_case_all_runs()
    #create_genome_graph('/Users/emilknudsen/Desktop/research/winner.pkl', filename="test")
