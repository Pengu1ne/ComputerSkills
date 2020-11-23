import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

data = np.loadtxt('data.xyz')

x = data[:0]
y = data[:1]
z = data[:2]

plt.plot(x,y,z, label='Loaded from file!')

ax.plot_surface(x, y, z, color='b')
plt.show()
