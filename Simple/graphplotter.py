import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ['Fitness', 'Generation']

files = ['Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history1.csv',
         'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history2.csv',
         'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history3.csv',
         'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history4.csv',
         'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history5.csv',
         'Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history6.csv']

column_names = []
for i in range(1, len(files)+1):
    column_names.append('Run ' + str(i))

column_names.append("Mean")

li = []

for filename in files:
    df = pd.read_csv(filename, names=headers, usecols=[0], sep=' ')
    li.append(df)


frame = pd.concat(li, axis=1, ignore_index=True)
frame = frame.fillna(1599)
frame['Mean'] = frame.mean(axis=1)
frame.columns = column_names
frame = frame.replace(1599, np.nan)

#df = pd.read_csv('Statistics_SenseBox_SensingRange3_ArenaFull/fitness_history1.csv', names=headers, usecols=[0], sep=' ')
print(frame)

ax = frame.plot(title='Fitness per generation (full arena)')
ax.set_xlabel("Generation")
ax.set_ylabel("Fitness")

plt.show()
