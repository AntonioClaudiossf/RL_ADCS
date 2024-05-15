import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

file_path = f"./ressources/images/Cenario_4/"

mean_rew_S1 = np.loadtxt(file_path+"mre_1_RL.txt",delimiter=',')
mean_rew_S2 = np.loadtxt(file_path+"mre_2_RL.txt")
mean_rew_S3 = np.loadtxt(file_path+"mre_3_RL.txt")

rmse_S1 = np.loadtxt(file_path+"RMSE_1_RL.txt",delimiter=',')
rmse_S2 = np.loadtxt(file_path+"RMSE_2_RL.txt")
rmse_S3 = np.loadtxt(file_path+"RMSE_3_RL.txt")

overShoot_S1 = np.loadtxt(file_path+"overShoot_1_RL.txt",delimiter=',')
overShoot_S2 = np.loadtxt(file_path+"overShoot_2_RL.txt")
overShoot_S3 = np.loadtxt(file_path+"overShoot_3_RL.txt")

steps = np.arange(0,len(mean_rew_S1))

# Plot the reward
rcParams['figure.figsize'] = 10, 7
plt.plot(steps, mean_rew_S1, color = 'b' ,linewidth = 2,label = "roll 1")
plt.plot(steps, mean_rew_S1, color = 'r' ,linewidth = 2,label = "pitch 1")
plt.plot(steps, mean_rew_S1, color = 'g' ,linewidth = 2,label = "yaw 1")
plt.xlabel('Step')
plt.ylabel('Recompensa acumulada média')
plt.legend(loc = "upper left")
plt.grid()
plt.savefig('ressources/images/Cenario_4/mean_rew_sats.png')
#plt.savefig('ressources/result_train_reward.pdf')
plt.clf()

plt.plot(steps, rmse_S1[:,0], color = 'b' ,linewidth = 2,label = "roll 1")
plt.plot(steps, rmse_S1[:,1], color = 'r' ,linewidth = 2,label = "picth 1")
plt.plot(steps, rmse_S1[:,2], color = 'g' ,linewidth = 2,label = "yaw 1")
plt.xlabel('Step')
plt.ylabel('rmse')
plt.legend(loc = "upper right")
plt.grid()
plt.savefig('ressources/images/Cenario_4/rmse_sats.png')
plt.clf()

plt.plot(steps, overShoot_S1[:,0], color = 'b' ,linewidth = 2,label = "roll 1")
plt.plot(steps, overShoot_S1[:,1], color = 'r' ,linewidth = 2,label = "picth 1")
plt.plot(steps, overShoot_S1[:,2], color = 'g' ,linewidth = 2,label = "yaw 1")
plt.xlabel('Step')
plt.ylabel('overshoot')
plt.legend(loc = "upper right")
plt.grid()
plt.savefig('ressources/images/Cenario_4/overshoot_sats.png')

plt.show()
