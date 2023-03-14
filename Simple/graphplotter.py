import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ['Fitness', 'Generation']

df = pd.read_csv('fitness_history.csv', names=headers, usecols=[0], sep=' ')
print(df)

ax = df.plot(title='Fitness per generation (full arena)')
ax.set_xlabel("Generation")
ax.set_ylabel("Fitness")

plt.show()
