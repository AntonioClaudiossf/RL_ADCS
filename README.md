# RL_ADCS
This repository is tracking my undergraduate thesis work in electrical engineering.
### Requirements :
This project was created and tested using the following settings :
```
Python 3.8.18
Ubuntu 22.04.3
python package ml-agents 0.28.0
unity ml-agents 2.2.1
```
Inside your favorite python virtual environment run the following bash command to pip install all the required python package :

```
./scripts/install_commands.sh
```

If everything is set correctly, you should be good to go !

The test files are written in python and accept a list of arguments to specify what to evaluate. Every arguments for the python scripts are documented. Simply run

```
python3 "name_script".py -h
```

### Enviromment

To perform the attitude control of a satelite in space, we usually apply torques on its axes so that it is placed in the desired orientation. To apply torque are commonly used reaction wheels.
<p align="center">
  <img src="/ressources/trainenvironment.png" width=40% />
</p>
<p align="center">
</p>
It was considered a simplified assembly with 3 reaction wheels aligned to the main axes of the satellite, as shown in the figure below.
<p align="center">
  <img src="/ressources/RW3.png" width=40% />
</p>
<p align="center">
</p>

### Agent

To perform the training was used as input information the quaternion of the current attitude of the satellite (size 4), the quaternion of the desired attitude (size 4), the quaternion of the attitude error (size 4) and the angular speed (size 3) of the satelite in the three axes.

As a result in the output layer of the neural network we have a vector (size 3) with values that are multiplied by a constant to convert into torque.

You can train a new model using:
```
mlagents-learn config/AttitudeSatellite.yaml --run-id={run_id} --env=envs/TRAINING_RL --num-envs={Number_Envs} {--no-graphics}
```


where run_id is the agent’s name. By default it will generate results in "results/run_id" using the PPO implementation of ml-agents for training. The {Number_Envs} is the number of environments that will be used during training. The argument {--no-graphics} does not show visually the training environment window, if you want to visually monitor remove this command. The Hyper-parameters are specified in yaml files inside the config folder at the root of the repository.

Example usage:
```
mlagents-learn config/AttitudeSatellite.yaml --run-id=agenterl --env=envs/TRAINING_RL --num-envs=16 --no-graphics
```

### Results :
#### Training

The PPO method was used for agent training, the result of the mean cumulative reward during training can be observed below:
<p align="center">
  <img src="/ressources/result_train_reward.png" width=50% />
</p>
<p align="center">
</p>

#### Test Episode
You can test your agent after training using the following command:
```
python3 scripts/run_test_model.py -s {scenario} -c {controller_typer} -id {run_id}
```

where {scenario} can be one of 3 different scenarios "1", "2" or "3" for testing. The {controller_typer} specifies whether the test will be performed with the PD controller "PD" or with the RL Agent "RL". Finally, {run_id} is the same one used in the previous command in training. With this command will be shown the test of the environment visually and at the end is generated some graphics that will be saved in: "ressources/images".

Example usage:
```
python3 scripts/run_test_model.py -s 2 -c RL -id agenterl
```

Below can be observed the pointing peformance of the satellite being controlled by the neural network (on the right side) and the PD controller (on the left side). The continuous lines represent the desired orientation, while the dashed lines represent the orientation of the satelite.
<p align="center">
  <img src="ressources/images/Cenario_1/Quaternion_Cenario_1_PD.png" width="30%"/> <img src="ressources/images/Cenario_1/Quaternion_Cenario_1_RL.png" width="30%"/> 
</p>
<p align="center">
</p>

The test videos are just below.

<p align="center">
  <img src="ressources/images/Cenario_1/Quaternion_Cenario_1_PD.png" width="40%"/> <img src="ressources/images/Cenario_1/Quaternion_Cenario_1_RL.png" width="40%"/> 
</p>
<p align="center">
</p>
### https://github.com/AntonioClaudiossf/RL_ADCS/results/videos/

