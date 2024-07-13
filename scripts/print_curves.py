import matplotlib.pyplot as plt
import numpy as np
import argparse
import matplotlib.gridspec as gridspec
from matplotlib import rcParams


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", type=int, default=1, help="Scenario 1, 2 or 3")
#parser.add_argument("-c", "--controller", type=str, default="PD", help="Controller type PD or RL")
args = parser.parse_args()


#Dir to save plots
path_images = f"./ressources/images/Cenario_{args.scenario}/"
path_pdfs = f"./ressources/pdfs/Cenario_{args.scenario}/"




#Save numpy txt to print the graphics
obs_quaternion_PD = np.loadtxt(path_images+f"Quaternion_Obs_Cenario_{args.scenario}_PD")
obs_quaternion_RL = np.loadtxt(path_images+f"Quaternion_Obs_Cenario_{args.scenario}_RL")

des_quaternion    = np.loadtxt(path_images+f"Quaternion_Des_Cenario_{args.scenario}_PD")

step_euler_angles_PD = np.loadtxt(path_images+f"Euler_Ang_Cenario_{args.scenario}_PD")
step_euler_angles_RL = np.loadtxt(path_images+f"Euler_Ang_Cenario_{args.scenario}_RL")

Torque_PD = np.loadtxt(path_images+f"Torque_Cenario_{args.scenario}_PD")
Torque_RL = np.loadtxt(path_images+f"Torque_Cenario_{args.scenario}_RL")

angular_vel_PD = np.loadtxt(path_images+f"Veloc_Ang_Cenario_{args.scenario}_PD")
angular_vel_RL = np.loadtxt(path_images+f"Veloc_Ang_Cenario_{args.scenario}_RL")

x_perfs = np.arange(0,len(obs_quaternion_PD)*0.1,0.1)





#Plot and save Euler Angles
rcParams['figure.figsize'] = 7, 4
colors_wc = ['r','g','b']
euler_indice = ['$\phi$','$\Theta$','$\psi$']
angle = ['roll', 'pitch', 'yaw']
#fig, axs = plt.subplots(2,2, layout='constrained')

for i in range(0,3):
	plt.plot(x_perfs,step_euler_angles_PD[:,i],color = colors_wc[i], label = f"{euler_indice[i]}"+"$_{PD}$")
	plt.plot(x_perfs,step_euler_angles_RL[:,i],'--',color = colors_wc[i], label = f"{euler_indice[i]}"+"$_{RL}$")
	plt.xlabel('Tempo (s)')
	plt.ylabel("Ângulo $(graus)$")
	plt.legend()
	plt.grid()
	plt.savefig(path_images+f"Euler_Ang_new_Cenario_{args.scenario}_{angle[i]}.png", bbox_inches='tight', dpi=200)
	plt.savefig(path_pdfs+f"Euler_Ang_new_Cenario_{args.scenario}_{angle[i]}.pdf", format='pdf', bbox_inches='tight')
	plt.show()
	plt.clf()



#Plot and save angular velocity
rcParams['figure.figsize'] = 7, 4
colors_wc = ['r','g','b']
wc_indice = ['x','y','z']
for i in range(0,3):   
	plt.plot(x_perfs,angular_vel_PD[:,i],color = colors_wc[i], label = f"$\omega_{wc_indice[i]}$"+"$_{-PD}$")
	plt.plot(x_perfs,angular_vel_RL[:,i],'--',color = colors_wc[i], label = f"$\omega_{wc_indice[i]}$"+"$_{-RL}$")
	plt.xlabel('Tempo (s)')
	plt.ylabel("Velocidade $(rad/s)$")
	plt.legend()
	plt.grid()
	plt.savefig(path_images+f"Veloc_Ang_new_Cenario_{args.scenario}_{angle[i]}.png", bbox_inches='tight', dpi=200)
	plt.savefig(path_pdfs+f"Veloc_Ang_new_Cenario_{args.scenario}_{angle[i]}.pdf", format='pdf', bbox_inches='tight')
	plt.show()
	plt.clf()



#Plot and save control torque
rcParams['figure.figsize'] = 7, 4
colors_T = ['r','g','b']
T_indice = ['x','y','z']
for i in range(0,3):    
	plt.plot(x_perfs,Torque_PD[:,i]*1000,color = colors_wc[i], label = f"$T_{T_indice[i]}$"+"$_{-PD}$")
	plt.plot(x_perfs,Torque_RL[:,i]*1000,'--',color = colors_wc[i], label = f"$T_{T_indice[i]}$"+"$_{-RL}$")
	plt.xlabel('Tempo (s)')
	plt.ylabel("Torque $(mNm)$")
	plt.legend()
	plt.grid()
	plt.savefig(path_images+f"Torque_new_Cenario_{args.scenario}_{angle[i]}.png", bbox_inches='tight', dpi=200)
	plt.savefig(path_pdfs+f"Torque_new_Cenario_{args.scenario}_{angle[i]}.pdf", format='pdf', bbox_inches='tight')
	plt.show()
	plt.clf()
plt.close()

#Plot and ave Quaternions
rcParams['figure.figsize'] = 8, 3
colors_q = ['blue', 'orange', 'green', 'red','black']
q_indice = ['x', 'y', 'z', 'w']
fig, axs = plt.subplots(2, 2, layout='constrained')
k=0
for i in range(0,2):
	for j in range(0,2):
		axs[i,j].plot(x_perfs, obs_quaternion_PD[:,k], color = colors_q[k],  label = f"$q_{q_indice[k]}$"+"$_{-PD}$")
		axs[i,j].plot(x_perfs, obs_quaternion_RL[:,k], '--',color = colors_q[k],  label = f"$q_{q_indice[k]}$"+"$_{-RL}$")
		axs[i,j].plot(x_perfs, des_quaternion[:,k], linewidth = 0.6,color = colors_q[4])
		axs[i,j].set_xlabel('Tempo (s)')
		axs[i,j].set_ylabel('Quatérnion value',fontsize=8)
		axs[i,j].legend()
		k+=1
plt.savefig(path_images+f"Quaternion_new_Cenario_{args.scenario}.png", bbox_inches='tight', dpi=200)
plt.savefig(path_pdfs+f"Quaternion_new_Cenario_{args.scenario}.pdf", format='pdf', bbox_inches='tight')
plt.show()
