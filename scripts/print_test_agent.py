import re
import numpy as np
import matplotlib.pyplot as plt

# Define regular expressions to extract values
action_pattern = re.compile(r"Action :\s*\[([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+)\]")
quat_pattern = re.compile(r"Actual_quat :\s*\[([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+)\]")
des_quat_pattern = re.compile(r"Des_quat :\s*\[([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+)\]")
w_cubsat_pattern = re.compile(r"w_cubsat :\s*\[([-0-9.e]+), ([-0-9.e]+), ([-0-9.e]+)\]")

# Read the text file
with open('log1.txt', 'r') as file:
    content = file.read()

# Extract values using regular expressions
action_matches = action_pattern.findall(content)
quat_matches = quat_pattern.findall(content)
des_quat_matches = des_quat_pattern.findall(content)
w_cubsat_matches = w_cubsat_pattern.findall(content)

# Determine the number of samples dynamically
num_samples = len(action_matches)

# Initialize numpy arrays
action_array = np.zeros((num_samples, 3))
actual_quat_array = np.zeros((num_samples, 4))
des_quat_array = np.zeros((num_samples, 4))
w_cubsat_array = np.zeros((num_samples, 3))

# Populate numpy arrays with extracted values
for i in range(num_samples):
    action_array[i] = np.array([float(x) for x in action_matches[i]])
    actual_quat_array[i] = np.array([float(x) for x in quat_matches[i]])
    des_quat_array[i] = np.array([float(x) for x in des_quat_matches[i]])
    w_cubsat_array[i] = np.array([float(x) for x in w_cubsat_matches[i]])

# Print the numpy arrays

print("Action Array:")
print(action_array)

print("\nActual Quaternion Array:")
print(actual_quat_array)

print("\nDesired Quaternion Array:")
print(des_quat_array)

print("\nAngular Velocity (w_cubsat) Array:")
print(w_cubsat_array)

print(len(actual_quat_array))

plt.plot(np.arange(0, 718 * 0.02, 0.02), w_cubsat_array, linestyle='-')
#plt.plot(np.arange(0, 718 * 0.02, 0.02), des_quat_array, linestyle='--',label='Des_q')
plt.title('Agular velocities')
plt.xlabel('time(s)')
plt.ylabel('w (rad/s)')
plt.legend()
plt.savefig('Angular_velocities_values_test01.png')
#plt.grid(True)
plt.show()



