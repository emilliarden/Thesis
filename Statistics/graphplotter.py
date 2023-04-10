import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob



def compare_neat_with_full_fullarena():
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [8.50, 3.50]

    headers = ['Max']

    files_full = glob.glob("Full_Arena/full_direct/*.csv")
    files_neat = glob.glob("Full_Arena/fs_neat_nohidden/*.csv")

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


    frame_full = pd.concat(li_full, axis=1, ignore_index=True)
    frame_full.fillna(method='ffill', inplace=True)
    frame_full['Mean'] = frame_full.mean(axis=1)
    column_names_full.append("Mean")
    frame_full.columns = column_names_full

    ax = frame_full["Mean"].plot(title='Max Fitness Each generation (full arena full_direct)', label="xxxxx")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.axhline(y=1440, color='r', linestyle='--')


#-----------------------------------------------------

    frame_neat = pd.concat(li_neat, axis=1, ignore_index=True)
    frame_neat.fillna(method='ffill', inplace=True)
    frame_neat['Mean'] = frame_neat.mean(axis=1)
    column_names_neat.append("Mean")
    frame_neat.columns = column_names_neat
    print(frame_neat)

    ax = frame_neat["Mean"].plot(title='Max Fitness Each Generation (full arena fs_neat_nohidden)', label="yyyyyy")
    #ax.set_xlabel("Generation")
    #ax.set_ylabel("Fitness")
    #ax.axhline(y=1440, color='r', linestyle='--')

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
    ax.axhline(y=1152, color='purple', linestyle='--')
    ax.axhline(y=1280, color='purple', linestyle='--')

    # -----------------------------------------------------
    plt.show()




if __name__ == "__main__":
    compare_unfull_80()
    #compare_neat_with_full_fullarena()
