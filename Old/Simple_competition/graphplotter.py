import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    headers = ['Mean Fitness', 'Generation']

    files = ['/Users/emilknudsen/Desktop/research/Simple_competition/Statistics/fitness_history_same_random_food1.csv',
             '/Users/emilknudsen/Desktop/research/Simple_competition/Statistics/fitness_history_different_random_food.csv',
             '/Users/emilknudsen/Desktop/research/Simple_competition/Statistics/fitness_history_random_food_trained_agents.csv',
             '/Users/emilknudsen/Desktop/research/Simple_competition/Statistics/fitness_history_random_food_trained_agents.csv',

             ]



    column_names = []
    for i in range(1, len(files)+1):
        column_names.append('Run ' + str(i))

    column_names.append("Mean")

    li = []

    for filename in files:
        df = pd.read_csv(filename, names=headers, usecols=[1], sep=' ')
        li.append(df)


    frame = pd.concat(li, axis=1, ignore_index=True)
    # frame = frame.fillna(1599)
    # frame['Mean'] = frame.mean(axis=1)
    # frame.columns = column_names
    # frame = frame.replace(1599, np.nan)

    #df = pd.read_csv('Statistics/fitness_history_same_random_food1.csv', names=headers, usecols=[0], sep=' ')
    print(frame)

    ax = frame.plot(title='Mean fitness per generation (full arena competition)')
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")

    plt.show()
