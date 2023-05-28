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

    pathToPreviousFile = '/Users/emilknudsen/Desktop/research/Statistics/Runs/Base_Case/fs_neat/middle_new_config/fitness_history' + str(
        number_to_look_for) + '.csv'
    df = pd.read_csv(pathToPreviousFile, usecols=[0], sep=' ')

    #pathToPreviousFile2 = '/Users/emilknudsen/Desktop/research/Statistics/Runs/Less_Food/HalfFull/TrainedOnFullMiddle_new_config/fitness_history' + str(
    #    number_to_look_for) + '.csv'
    #df2 = pd.read_csv(pathToPreviousFile2, usecols=[0], sep=' ')

    #pathToPreviousFile3 = '/Users/emilknudsen/Desktop/research/Statistics/Runs/Less_Food/QuarterFull/TrainedOnFullHalf/fitness_history' + str(
        #number_to_look_for) + '.csv'
    #df3 = pd.read_csv(pathToPreviousFile3, usecols=[0], sep=' ')



    return len(df.index) #+ len(df2.index)# + len(df3.index)


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


def compare_two_runs(new_folder, pretrained_folder, constants, title):
    #mean_finishing_for_middle_full_old_config = 559  # 558,4 for old_config middle full arena

    #mean finishing for topleft_full
    mean_finishing_point_for_full_new_config_topleft = 0

    #mean generation when trained on middle position in full arena
    mean_finishing_point_for_full= 351  #351,2 for new_config middle full arena

    #mean generation when pretrained on full to be able to complete half = 11
    mean_finishing_point_for_full_then_half = mean_finishing_point_for_full + 30 #29,6 from full to half

    #mean generation when pretrained on full, then half to be able to complete quarter = 294
    mean_finishing_point_for_full_then_half_then_quarter = mean_finishing_point_for_full_then_half + 294

    mean_finishing_point_for_successfull_runs = mean_finishing_point_for_full


    new_dataframe = create_df_with_mean_and_stddev(new_folder)
    pretrained_dataframe = create_df_with_mean_and_stddev(pretrained_folder)

    data_frames = [new_dataframe, pretrained_dataframe]
    # NEW, PRETRAINED, RANDOM COLORS:
    colors = [('#CC4F1B', '#FF9848'), ('#1B2ACC', '#089FFF')]
    labels = ['Direct', 'Incremental']

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    for i, df in enumerate(data_frames):



        x = list(range(0, len(df['Mean']))) if i == 0 else \
            list(range(mean_finishing_point_for_successfull_runs, len(df['Mean'])+mean_finishing_point_for_successfull_runs))
        y = df['Mean'] if i == 0 or i == 2 else df['Mean'].head(len(df['Mean']))
        std_dev = df['Standard deviation'] if i == 0 else df['Standard deviation'].head(len(df['Standard deviation']))

        plt.plot(x, y, color=colors[i][0], label=labels[i])
        plt.fill_between(x=x,
                         y1=y - std_dev,
                         y2=y + std_dev,
                         alpha=0.5, edgecolor=colors[i][0], facecolor=colors[i][1])

    # ---------------------------------------------------
    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title(title, fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="lower right")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(14, 8)
    plt.savefig("Graphs/" + title + ".svg")
    plt.savefig("Graphs/" + title + ".png")
    plt.show()


def compare_multiple_runs(constants, title, direct_folder=None, base_case=None, half=None, quarter=None, corners=None, quarterWater=None):
    direct_frame = create_df_with_mean_and_stddev(direct_folder) if direct_folder is not None else []
    base_case_frame = create_df_with_mean_and_stddev(base_case) if base_case is not None else []
    fifty_percent_frame = create_df_with_mean_and_stddev(half) if half is not None else []
    twentyfive_percent_frame = create_df_with_mean_and_stddev(quarter) if quarter is not None else []
    corners_frame = create_df_with_mean_and_stddev(corners) if corners is not None else []
    quarterWater_frame = create_df_with_mean_and_stddev(quarterWater) if quarterWater is not None else []
    #random_food_frame = create_df_with_mean_and_stddev(random_food)


    data_frames = [direct_frame, base_case_frame, fifty_percent_frame, twentyfive_percent_frame, corners_frame, quarterWater_frame]
    increment = [0, 351, 157, 548, 827, 1109]
    max_gens = 3000
    # NEW, PRETRAINED, RANDOM COLORS:
    colors = [('#CC4F1B', '#FF9848'), ('#1B2ACC', '#089FFF'), ('#f740df', '#f786e8'),
              ('#00e600', '#80ff80'), ('#000000', '#828282'), ('#ffff00', '#ffff80')]
    labels = ['Direct', 'Incremental (Base case)', 'Incremental (50% environment)',
              'Incremental (25% environment)', 'Incremental (Corner clusters)', 'Incremental (25‰ with water)']

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]

    for i, df in enumerate(data_frames):
        x_from = increment[i]
        x_to = len(df['Mean']) + increment[i] if increment[i] + len(df['Mean']) <= 5000 else len(df['Mean'])
        x = list(range(x_from, x_to))
        y = df['Mean'] if increment[i] + len(df['Mean']) <= 5000 else df['Mean'].head(len(df['Mean'])-increment[i])
        std_dev = df['Standard deviation'] if increment[i] + len(df['Mean']) <= 5000 else df['Standard deviation'].head(len(df['Standard deviation'])-increment[i])

        plt.plot(x, y, color=colors[i][0], label=labels[i])
        plt.fill_between(x=x,
                         y1=y - std_dev,
                         y2=y + std_dev,
                         alpha=0.3, edgecolor=colors[i][0], facecolor=colors[i][1])

    # ---------------------------------------------------
    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title(title, fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="lower right")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(14, 8)
    plt.savefig("Graphs/" + title + ".svg")
    plt.savefig("Graphs/" + title + ".png")
    plt.show()



def show_all_runs(new_folder, pretrained_folder, constants, title):
    new_files = glob.glob(new_folder + "/*.csv")
    pretrained_files = glob.glob(pretrained_folder + "/*.csv")

    oranges = cm.get_cmap('Oranges')
    blues = cm.get_cmap('Blues')

    # insert pretrained file into dataframe
    for i, filename in enumerate(pretrained_files):
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        lines_to_shift = get_amount_of_lines_to_shift(filename)
        x = list(range(lines_to_shift, len(df)+lines_to_shift))
        y = df.head(len(df))
        plt.plot(x, y, color=blues(blues.N - (20 * i)), label='Incremental ' + str(i + 1))

        # insert direct files into dataframe
    for i, filename in enumerate(new_files):
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        x = list(range(0, len(df)))
        y = df
        plt.plot(x, y, color=oranges(oranges.N - (20 * i)), label='Direct ' + str(i + 1))

    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [15.50, 7.50]


    plt.xlabel("Generation", fontsize=18)
    plt.ylabel("Fitness", fontsize=16)
    plt.title(title, fontsize=16)
    plt.axhline(y=constants.FITNESS_THRESH, color='purple', linestyle='--', label='100% fitness')
    plt.legend(loc="lower right")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(14, 8)
    plt.savefig("Graphs/" + title + ".svg")
    plt.savefig("Graphs/" + title + ".png")
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
    constants = Constants(None, None, FoodDistribution.Cross, None, None)

    # compare_multiple_runs('/Users/emilknudsen/Desktop/research/Statistics/Runs/Complex/HalfWaterHalfFood/Direct',
    #                       '/Users/emilknudsen/Desktop/research/Statistics/Runs/Complex/HalfWaterHalfFood/TrainedOnFull',
    #                       '/Users/emilknudsen/Desktop/research/Statistics/Runs/Complex/HalfWaterHalfFood/TrainedOnFullHalf',
    #                       '/Users/emilknudsen/Desktop/research/Statistics/Runs/Complex/HalfWaterHalfFood/TrainedOnFullHalfQuarter2x',
    #                       '/Users/emilknudsen/Desktop/research/Statistics/Runs/Complex/HalfWaterHalfFood/TrainedOnFullHalfQuarterCorners',
    #                       constants,
    #                       'Test')


    compare_multiple_runs(constants, 'Cross environment',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/Direct',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnFull',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnHalf',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnQuarter',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnCorners',
                    '/Users/emilknudsen/Desktop/Thesis/Statistics/Runs/C)Complex/B)Cross/TrainedOnHalfWater'
                    )

    # base_case_all_runs()
    # create_genome_graph('/Users/emilknudsen/Desktop/research/winner.pkl', filename="test")
