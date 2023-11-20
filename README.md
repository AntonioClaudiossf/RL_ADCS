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

It was considered a simplified assembly with 3 reaction wheels aligned to the main axes of the satellite, as shown in the figure below.

![Screenshot from 2023-11-19 21-46-34](https://github.com/AntonioClaudiossf/RL_ADCS/results/images/121523096/81f2f2c8-daa3-4f1f-b4de-2674b10c8688)


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

