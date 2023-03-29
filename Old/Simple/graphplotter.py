import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = [7.50, 3.50]

    headers = ['Max', 'Mean']

    files = ['Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history_same_random_food1.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history2.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history3.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history4.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history6.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history7.csv',
             'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history8.csv']

    files = ['/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange3_ArenaFull_RandomPos/fitness_history_same_random_food1.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange3_ArenaFull_RandomPos/fitness_history2.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange3_ArenaFull_RandomPos/fitness_history3.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange3_ArenaFull_RandomPos/fitness_history4.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange3_ArenaFull_RandomPos/fitness_history5.csv']

    files = ['/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange4_ArenaRandom_RandomPos/fitness_history_no_bonus_on_alive.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange4_ArenaRandom_RandomPos/fitness_history_bonus_on_alive.csv']

    files = ['/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange?_ArenaRandom/fitness_history1.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange?_ArenaRandom/fitness_history2.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange?_ArenaRandom/fitness_history3.csv',
             '/Users/emilknudsen/Desktop/research/Simple/Statistics_SenseBox_SensingRange?_ArenaRandom/fitness_history4.csv',
             ]

    column_names = []
    for i in range(1, len(files)+1):
        column_names.append('Run ' + str(i))

    #column_names.append("Mean")

    li = []

    for filename in files:
        df = pd.read_csv(filename, names=headers, usecols=[0,1], sep=' ')
        li.append(df)


    frame = pd.concat(li, axis=0, ignore_index=True)
    #frame = frame.fillna(1599)
    #frame['Mean'] = frame.mean(axis=1)
    #frame.columns = column_names
    #frame = frame.replace(1599, np.nan)

    #df = pd.read_csv('Statistics/fitness_history_same_random_food1.csv', names=headers, usecols=[0], sep=' ')
    print(frame)

    ax = frame.plot(title='Mean fitness per generation (5.000 new random food.py every gen)')
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")

    plt.show()
