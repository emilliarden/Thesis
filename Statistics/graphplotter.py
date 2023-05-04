import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from visualize import draw_net, draw_net_without_all_nodes
import neat
import pickle



def compare_neat_with_full_fullarena():
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [8.50, 3.50]

    headers = ['Max']

    files_full = glob.glob("Full_Arena/full_direct/middle/*.csv")
    files_neat = glob.glob("Full_Arena/fs_neat/topleft/*.csv")

    column_names_full = []
    for i in range(1, len(files_full) + 1):
        column_names_full.append('Run ' + str(i-1))

    column_names_neat = []
    for i in range(1, len(files_neat) + 1):
        column_names_neat.append('Run ' + str(i-1))

    li_full = []
    for filename in files_full:
        df = pd.read_csv(filename, names=headers, usecols=[0], sep=' ')
        li_full.append(df)

    li_neat = []
    for filename in files_neat:
        df = pd.read_csv(filename, names=headers, usecols=[0], sep=' ')
        li_neat.append(df)

    # full_direct -----------------------------------------------------
    frame_full = pd.concat(li_full, axis=1, ignore_index=True)
    frame_full.fillna(method='ffill', inplace=True)
    frame_full['Mean'] = frame_full.mean(axis=1)
    #frame_full['Mean'].mask(frame_full['Mean'] >= 1440, np.nan, inplace=True)



    # fs_neat -----------------------------------------------------

    frame_neat = pd.concat(li_neat, axis=1, ignore_index=True)
    frame_neat.fillna(method='ffill', inplace=True)
    frame_neat['Mean'] = frame_neat.mean(axis=1)
    #frame_neat['Mean'].mask(frame_neat['Mean'] >= 1440, np.nan, inplace=True)

    # random --------------------------------------------------------------
    random_df = pd.read_csv('/Users/emilknudsen/Desktop/research/Statistics/Full_Arena/random_run/fitness_history0.csv', names=headers, usecols=[0], sep=' ')
    random_df = pd.concat([random_df, random_df], axis=0, ignore_index=True)
    #----------------------------------------------------------------------
    mean_frame = pd.concat([frame_neat['Mean'], frame_full['Mean'], random_df], axis=1, ignore_index=True)
    mean_frame.columns = ['FS_Neat', 'Fully Connected', 'Random']
    ax = mean_frame.plot(title='Base case (start position = middle)')
    print(mean_frame)

    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    #ax.axhline(y=396, color='purple', linestyle='--')
    ax.axhline(y=440, color='purple', linestyle='--')

    plt.show()



def base_case_all_runs():
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [8.50, 3.50]

    files_neat = glob.glob("Full_Arena/fs_neat/middle/*.csv")
    files_fullyconnected = glob.glob("Full_Arena/full_direct/middle/*.csv")
    file_random = glob.glob("Full_Arena/random_run/*.csv")
    shades_of_red = ['#ff0000', '#d70000', '#c60000', '#b70000', '#9b0000', '#ff0000', '#d70000', '#c60000', '#b70000', '#9b0000']
    shades_of_green = ['#22b600', '#26cc00', '#7be382', '#006400', '#009c1a', '#22b600', '#26cc00', '#7be382', '#006400', '#009c1a']
    random_color = '#22ff00'

    color_dict = dict()
    column_names = []

    for i in range(1, len(files_neat) + 1):
        column_name = 'FS_Neat ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_green[i - 1]

    for i in range(1, len(files_fullyconnected) + 1):
        column_name = 'Fully Connected ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_red[i - 1]

    column_name = 'Random'
    column_names.append(column_name)
    color_dict[column_name] = random_color

    li = []
    for filename in files_neat + files_fullyconnected + file_random:
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        li.append(df)

    frame = pd.concat(li, axis=1, ignore_index=True)
    frame.columns = column_names

    print(frame)
    ax = frame.plot(title='Base case each run separately', color=color_dict)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.axhline(y=440, color='purple', linestyle='--')

    # -----------------------------------------------------
    plt.show()


def compare_unfull_80():
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [8.50, 3.50]

    files_pretrained = glob.glob("Unfull_Arena/80_percent/TrainedOnFull/fs_neat_nohidden/*.csv")
    files_new = glob.glob("Unfull_Arena/80_percent/New_fs_neat_nohidden/*.csv")
    shades_of_red = ['#ff0000', '#d70000', '#c60000', '#b70000', '#9b0000']
    shades_of_green = ['#22b600', '#26cc00', '#7be382', '#006400', '#009c1a']


    color_dict = dict()
    column_names = []
    for i in range(1, len(files_pretrained) + 1):
        column_name = 'Pretrained ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_green[i-1]

    for i in range(1, len(files_new) + 1):
        column_name = 'New ' + str(i)
        column_names.append(column_name)
        color_dict[column_name] = shades_of_red[i-1]





    li = []
    for filename in files_pretrained + files_new:
        df = pd.read_csv(filename, usecols=[0], sep=' ')
        li.append(df)

    frame = pd.concat(li, axis=1, ignore_index=True)
    frame.columns = column_names

    ax = frame.plot(title='Max fitness (80% food)', color=color_dict)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.axhline(y=396, color='purple', linestyle='--')
    ax.axhline(y=440, color='purple', linestyle='--')

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
    #compare_unfull_80()
    compare_neat_with_full_fullarena()
    #base_case_all_runs()
    #create_genome_graph('/Users/emilknudsen/Desktop/research/winnerCross.pkl', filename="test")
