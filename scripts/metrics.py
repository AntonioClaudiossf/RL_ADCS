import numpy as np
import math

def IAE(Euler_angles):
    len_steps = len(Euler_angles[:,0])
    roll_iae = np.sum(np.absolute(np.zeros(len_steps) - (Euler_angles[:,0]*math.pi/180.0)))
    pich_iae = np.sum(np.absolute(np.zeros(len_steps) - (Euler_angles[:,1]*math.pi/180.0)))
    yaw__iae = np.sum(np.absolute(np.zeros(len_steps) - (Euler_angles[:,2]*math.pi/180.0)))
    iae = np.array([roll_iae,pich_iae,yaw__iae])
    return iae

def SettlingTime(euler_angles):
    threshold = 0.02 #2%
    dt = 0.1
    euler_init = np.array([30,45,60])
    values_threshold = euler_init*threshold
    out_threshold = np.abs(euler_angles)>values_threshold
    #print(out_threshold)
    indice_roll = 0
    indice_picth = 0
    indice_yaw = 0
    last_true_r = 0
    last_true_p = 0
    last_true_y = 0

    for i in out_threshold[:,0]:
        indice_roll += 1
        if i:
            last_true_r = indice_roll

    for i in out_threshold[:,1]:
        indice_picth += 1
        if i:
            last_true_p = indice_picth
    for i in out_threshold[:,2]:
        indice_yaw += 1
        if i:
            last_true_y = indice_yaw

    setting_time = np.array([last_true_r,last_true_p,last_true_y])*dt
    return setting_time

def OverShoot(Euler_angles):
    euler_init = np.array([30,45,60])
    len_steps = len(Euler_angles[:,0])
    overshoot_r = (-np.min(Euler_angles[:,0])/(euler_init[0]))*100
    if overshoot_r<0:
        overshoot_r = 0
    overshoot_p = (-np.min(Euler_angles[:,1])/(euler_init[1]))*100
    if overshoot_p<0:
        overshoot_p = 0
    overshoot_y = (-np.min(Euler_angles[:,2])/(euler_init[2]))*100
    if overshoot_y<0:
        overshoot_y = 0
    overshoot = np.array([overshoot_r,overshoot_p,overshoot_y])

    return overshoot
