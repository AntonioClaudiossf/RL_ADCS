import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

file_path = f"./results/AttitudeSatellite_reward.json"

with open(file_path, 'r') as file:
    data = np.array(json.load(file))

# Extract the checkpoints
#checkpoints = data["AttitudeSatellite"]["checkpoints"]

# Extract the steps and reward values
#steps = [checkpoint["steps"] for checkpoint in checkpoints]
#rewards = [checkpoint["reward"] for checkpoint in checkpoints]
rewards = data[:,2]
steps = data[:,1]

# Plot the reward
rcParams['figure.figsize'] = 7, 4
plt.plot(steps, rewards, color = 'b' ,linewidth = 2)
#plt.title('Reward')
plt.xlabel('Step')
plt.ylabel('Recompensa acumulada média')
plt.ylim([-60,10])
plt.grid()
plt.savefig('ressources/result_train_reward.png')
plt.savefig('ressources/result_train_reward.pdf')
#plt.grid(True)
plt.show()
