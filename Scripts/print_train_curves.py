import json
import matplotlib.pyplot as plt


file_path = "training_status 1.json"  # Substitua pelo caminho real do seu arquivo
with open(file_path, 'r') as file:
    data = json.load(file)

# Extraindo os checkpoints
checkpoints = data["AttitudeSatellite"]["checkpoints"]

# Extraindo as informações relevantes
steps = [checkpoint["steps"] for checkpoint in checkpoints]
rewards = [checkpoint["reward"] for checkpoint in checkpoints]

# Plotando o gráfico
plt.plot(steps, rewards, linestyle='-')
plt.title('Reward')
plt.xlabel('Step')
plt.ylabel('Mean cumulative reward')
plt.savefig('recompensa_vs_step_teste02.png')
#plt.grid(True)
plt.show()
