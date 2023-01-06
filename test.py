import numpy as np

x1 = 0
x2 = 1
y1 = 0
y2 = 1
alpha1 = 0
alpha2 = 0

alpha1_rad = alpha1 / 180 * np.pi
alpha2_rad = alpha2 / 180 * np.pi

ratio1 = np.sin(np.pi - alpha1_rad) / np.cos(np.pi - alpha2_rad)
ratio2 = np.cos(np.pi - alpha1_rad) / np.sin(np.pi - alpha2_rad)

y_c = (y2 * ratio1 - y1) / (ratio1 - 1)
x_c = (x1 - x2 * ratio2) / (1 - ratio2)

print("x_c")
print(x_c)
print("y_c")
print(y_c)