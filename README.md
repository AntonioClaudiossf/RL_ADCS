# RL_ADCS
This repository is tracking my undergraduate thesis work in electrical engineering.
### Requirements :
This project was created and tested using the following settings :
```
Python 3.10.12
Ubuntu 22.04.3
python package ml-agents 1.0.0
unity ml-agents 3.0.0
```

### Enviromment

To perform the attitude control of a satelite in space we usually apply torques in their so that it is placed in the desired orientation. To apply torque are commonly used reaction wheels.
<p align="center">
  <img src="/results/images/Screenshot from 2023-11-19 21-49-45.png" width=40% />
</p>
<p align="center">
</p>
It was considered a simplified assembly with 3 reaction wheels aligned to the main axes of the satellite, as shown in the figure below.
<p align="center">
  <img src="/results/images/Screenshot from 2023-11-19 21-46-34.png" width=40% />
</p>
<p align="center">
</p>

### Agent

To perform the training was used as input information the torque value that applied to the satelite (size 3), the desired quaternion (size 4), the current quaternion (size 4) of the satelite and the angular velocity (size 3) of the satelite in the three axes.

As a result in the output layer of the neural network we have a vector (size 3) with values that are multiplied by a constate to convert to torque.

### Results :
#### Training
The ppo method was used for agent training, the result of the average reward during training can be observed below:
<p align="center">
  <img src="/results/images/recompensa_vs_step_teste02.png" width=40% />
</p>
<p align="center">
</p>

#### Test Episode
Below can be observed the peformance of satellite pointing being controlled by the neural network. The dashed lines represent the desired orientation, while the continuous lines represent the orientation of the satelite.
<p align="center">
  <img src="/results/images/quaternion_values_teste01.png" width=70% />
</p>
<p align="center">
</p>

https://github.com/AntonioClaudiossf/RL_ADCS/results/videos/62f1603d-a2be-41f6-ab12-f5731e188956

