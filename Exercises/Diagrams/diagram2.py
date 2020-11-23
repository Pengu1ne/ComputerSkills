import matplotlib.pyplot as plt
import numpy as np
from scipy import *

#x1 = range(-10,0)
#y1 = [-1.0/value for value in x1]
x2 = range(1,11)
y2 = [-1.0/value for value in x2]
x0 = range(1,11)
y0 = [0*value for value in x0]

plt.xlabel('r')
plt.ylabel('V(r)')
plt.title('Potential of hydrogen like atom')
#plt.plot(x1,y1, color='green', label='Potential')
plt.plot(x2,y2, color='green', label='Potential')
plt.plot(x0,y0, color='black', linestyle='-')
plt.legend()
plt.show()
