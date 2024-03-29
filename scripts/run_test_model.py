
from mlagents.trainers.torch.encoders import VectorInput
from mlagents.trainers.torch.layers import LinearEncoder
from mlagents.trainers.torch.action_model import ActionModel
from mlagents_envs.base_env import ActionSpec
from unity_env_gym import make_unity_env
import torch
import numpy as np
import glob
import os
import re
import matplotlib.pyplot as plt
from matplotlib import rcParams
import argparse
from mlagents.torch_utils import default_device

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num_test_episode", type=int, default=1, help="number of episode of tests per checkpoints")
parser.add_argument("-f", "--freq_test_models", type=int, default=2, help="skip checkpoints every freq_test_models")
args = parser.parse_args()

rcParams['figure.figsize'] = 10, 7
num_test_episode = args.num_test_episode
freq_test_models = args.freq_test_models
freq_chkpt = 0.05 #1e6 steps
linspace = freq_test_models * freq_chkpt

@torch.no_grad()
def test_agent_rl(nb_test_episodes):
    rewards_episode = []
    reward_history = []
    obs_history = []
    for episode in range(nb_test_episodes):
        obs = env.reset()
        done = False 
        while not done: 
            env.render()
            with torch.no_grad(): 
                norm_obs = vector_input(torch.FloatTensor(obs).to(default_device()))
                encoding = body(norm_obs)
                action,_,_ = action_head.forward(encoding,torch.full((AGENT_HIDDEN_DIM,), False, dtype=bool))
                action = (torch.clamp(action.continuous_tensor, -3, 3)/3).squeeze(0)
            next_obs, rew, done, _ = env.step(action.cpu())
            rewards_episode.append(rew)
            obs_history.append(obs)
            obs = next_obs 
			
        reward_history.append(np.sum(rewards_episode))
        rewards_episode = []
    return np.mean(reward_history), np.std(reward_history),np.vstack(obs_history)

def bubbleSort(arr):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            return
    return arr

action_size = ActionSpec.create_continuous(3)

nn_obs_dim = 11

robot_idx = 1
task_idx = 1

SOURCE_ROBOT_NAME = 1
AGENT_HIDDEN_DIM = 225
PREFIX = "Behavior-*.pt"


# First we test performance, then we test average cumulative reward
perfs_dict = {}

# Outter loop for recording either test performance or avg rwd

# We test performance on the test environment

print()
print("-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*")
print("-*-*-*-*-* TEST PERFORMANCE -*-*-*-*-*-")
print("-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*")
print()
ENV_NAME = f"./envs/RL_ADCS_3RW.x86_64"

# Middle loop for testing every possible model type (unn, vanilla rl, finetuned models)

print(f"========== TESTING ATTITUDE CONTROL 3WR MODEL ==========")

RES_DIR_PATH = f"./results/attitude_satellite_teste_13/AttitudeSatellite/"

use_bases = False

# Retrieve every models from the checkpoint folder for tests
files_name = glob.glob(RES_DIR_PATH)
print("files names:/n")
print(files_name)
if files_name == []:
    print(f"/!\ /!\ {RES_DIR_PATH} not found /!\ /!\ ")

# Glob does not return file names in chronological order so need to sort
# Use regexp for retrieving step number in the checkpoint name
#steps = bubbleSort([int(re.search('(?<=Behavior-).*?(?=.pt)',step).group(0)) for step in files_name])

#print("* Total number of checkpoint : ",len(steps))


perfs_dict["rl"+"_1"] = []

# Inner loop to test chkpt (one every two)
#for step in steps[::freq_test_models] :
step = 6000207
print(f"-- step {step} --")

# ======= LOAD MODEL =======
vector_input = VectorInput(input_size = nn_obs_dim, normalize = True)
vector_input.load_state_dict(torch.load(RES_DIR_PATH+f"vector_input-{step}.pth", map_location=torch.device(default_device())),strict = True)

body = LinearEncoder(
    input_size=nn_obs_dim,
    num_layers=3,
    hidden_size=AGENT_HIDDEN_DIM,
)
body.load_state_dict(torch.load(RES_DIR_PATH+f"body_endoder-{step}.pth", map_location=torch.device(default_device())),strict = True)

action_head = ActionModel(AGENT_HIDDEN_DIM,action_size,tanh_squash=False,deterministic=True)

action_head.load_state_dict(torch.load(RES_DIR_PATH+f"action_model-{step}.pth", map_location=torch.device(default_device())),strict = True)
print("action_head")
print(action_head)
# ===========================

# Load unity environment
env = make_unity_env(ENV_NAME, worker_id = 30, no_graphics = False, time_scale = 1.0)

# test for num_test_episode
step_perf, step_std,step_obs = test_agent_rl(num_test_episode)

#perfs_dict[mode+"_"+str(i)].append(step_perf)

#print("perf : ",step_perf)
#print()
env.close()
'''' for ate aqui'''

# os makdir
#if not os.path.exists(SAVE_PERFS_DIR):
#    os.makedirs(SAVE_PERFS_DIR)
#np.savetxt(SAVE_PERFS_DIR+mode+"_"+str(i)+".txt", np.array(perfs_dict[mode+"_"+str(i)]))

obs_quaternion = step_obs[:,:4]
des_quaternion = step_obs[:,4:8]
angular_vel = step_obs[:,8:]
x_perfs = np.arange(0,len(step_obs)*0.02,0.02)

colors = ['blue', 'orange', 'green', 'red']

fig, axs = plt.subplots(4, 1, layout='constrained')
for i in range(0,4):
	axs[i].plot(x_perfs, obs_quaternion[:,i], '--',color = colors[i],  label = f"q{i}_obs")
	axs[i].plot(x_perfs, des_quaternion[:,i],      color = colors[i],  label = f"q{i}_des")
	axs[i].set_xlabel('time(s)')
	axs[i].set_ylabel('Quaternio value')
	axs[i].legend()
'''
axs[1].plot(x_perfs, obs_quaternion[:,1], '-', color='orange',label = "q1_obs")
axs[1].plot(x_perfs, des_quaternion[:,1],      color='orange',label = "q1_des")
axs[1].legend()

axs[2].plot(x_perfs, obs_quaternion[:,2], '--',color='green', label = "q2_obs")
axs[2].plot(x_perfs, des_quaternion[:,2],      color='green', label = "q2_des")
axs[2].legend()

axs[3].plot(x_perfs, obs_quaternion[:,3], '--',color='red',   label = "q3_obs")
axs[3].plot(x_perfs, des_quaternion[:,3],      color='red',   label = "q3_des")
axs[3].legend()
plt.grid()'''
#plt.plot(x_perfs,obs_quaternion, '--', label = "q_obs")
#plt.plot(x_perfs,des_quaternion, label = "q_obs")
plt.show()
"""
# add a perf of 0 for the 0-step
plt.plot(x_perfs,np.concatenate(([0],perfs_dict["rl_0"]), axis = 0), '--r', label = "Performance PPO")
plt.plot(x_perfs,np.concatenate(([0],perfs_dict["unn_0"]), axis = 0), '--b', label = "Performance UNN")

# start at 1 because we don't have chckpt for 0 step
plt.plot(x_perfs[1:],np.array(perfs_dict["rl_1"])/max_rwd, '-r', label = "Average reward PPO")
plt.fill_between(x_perfs[1:], (np.array(perfs_dict["rl_1"])-np.array(std_dict["rl_1"]))/max_rwd, (np.array(perfs_dict["rl_1"])+np.array(std_dict["rl_1"]))/max_rwd, alpha=0.35, edgecolor='r', facecolor='r')
plt.plot(x_perfs[1:],np.array(perfs_dict["unn_1"])/max_rwd,'-b', label = "Average reward UNN")
plt.fill_between(x_perfs[1:], (np.array(perfs_dict["unn_1"])-np.array(std_dict["unn_1"]))/max_rwd, (np.array(perfs_dict["unn_1"])+np.array(std_dict["unn_1"]))/max_rwd, alpha=0.35, edgecolor='b', facecolor='b')

if "unn_ft_braccio_0" in perfs_dict and "unn_ft_braccio_1" in perfs_dict :
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_braccio_0"])],perfs_dict["unn_ft_braccio_0"], '--g', label = "UNN fine tuned from Braccio")
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_braccio_1"])],np.array(perfs_dict["unn_ft_braccio_1"])/max_rwd,'-g', label = "UNN fine tuned from Braccio")
    plt.fill_between(x_perfs[:len(perfs_dict["unn_ft_braccio_1"])], (np.array(perfs_dict["unn_ft_braccio_1"])-np.array(std_dict["unn_ft_braccio_1"]))/max_rwd, (np.array(perfs_dict["unn_ft_braccio_1"])+np.array(std_dict["unn_ft_braccio_1"]))/max_rwd, alpha=0.35, edgecolor='g', facecolor='g')

if "unn_ft_panda_0" in perfs_dict and "unn_ft_panda_1" in perfs_dict :
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_panda_0"])],perfs_dict["unn_ft_panda_0"], '--k', label = "UNN fine tuned from Panda")
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_panda_1"])],np.array(perfs_dict["unn_ft_panda_1"])/max_rwd,'-k', label = "UNN fine tuned from Panda")
    plt.fill_between(x_perfs[:len(perfs_dict["unn_ft_panda_1"])], (np.array(perfs_dict["unn_ft_panda_1"])-np.array(std_dict["unn_ft_panda_1"]))/max_rwd, (np.array(perfs_dict["unn_ft_panda_1"])+np.array(std_dict["unn_ft_panda_1"]))/max_rwd, alpha=0.35, edgecolor='k', facecolor='k')

if "unn_ft_ur10_0" in perfs_dict and "unn_ft_ur10_1" in perfs_dict :
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_ur10_0"])],perfs_dict["unn_ft_ur10_0"], '--y', label = "UNN fine tuned from UR10")
    plt.plot(x_perfs[:len(perfs_dict["unn_ft_ur10_1"])],np.array(perfs_dict["unn_ft_ur10_1"])/max_rwd,'-y', label = "UNN fine tuned from UR10")
    plt.fill_between(x_perfs[:len(perfs_dict["unn_ft_ur10_1"])], (np.array(perfs_dict["unn_ft_ur10_1"])-np.array(std_dict["unn_ft_ur10_1"]))/max_rwd, (np.array(perfs_dict["unn_ft_ur10_1"])+np.array(std_dict["unn_ft_ur10_1"]))/max_rwd, alpha=0.35, edgecolor='y', facecolor='y')



plt.xlabel('Number of training steps (1e6)', fontsize=20)
plt.ylabel("Performance / Normalized average cumulative rewards", fontsize=20)
#plt.title(f"Performance and learning curves for the {SOURCE_ROBOT_NAME} robot on task", fontsize=18)
plt.legend(loc="lower right", fontsize=20)
#plt.savefig(SAVE_PERFS_DIR+'perfs.png', bbox_inches='tight', dpi=199)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()"""
