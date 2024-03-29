import json
import matplotlib.pyplot as plt

file_path = f"./results/AttitudeSatellite13/run_logs/training_status.json"

with open(file_path, 'r') as file:
    data = json.load(file)

# Extraindo os checkpoints
checkpoints = data["AttitudeSatellite"]["checkpoints"]

# Extraindo as informações relevantes
steps = [checkpoint["steps"] for checkpoint in checkpoints]
rewards = [checkpoint["reward"] for checkpoint in checkpoints]

print(len(steps))

# Plotando o gráfico
plt.plot(steps, rewards, linestyle='-')
plt.title('Reward')
plt.xlabel('Step')
plt.ylabel('Mean cumulative reward')
plt.savefig('recompensa_vs_step_teste13.png')
#plt.grid(True)
plt.show()
