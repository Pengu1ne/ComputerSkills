import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

x,y = np.loadtxt('ex1.xy', delimiter=' ', unpack=True)

plt.plot(x,y, label = 'TEST')
plt.ylabel('test')
plt.xlabel('test')
plt.axis([-9, 9, -1, 10])

plt.show()
