'''
More exercises on classes. This time, triangle.
The exercise can be found from:
https://www.w3resource.com/python-exercises/class-exercises/
'''

import numpy as np
import matplotlib.pyplot as plt

class triangle:
  def __init__(self, angle1, angle2, angle3):
    self.angle1 = angle1
    self.angle2 = angle2
    self.angle3 = angle3

  number_of_sides = 3

  def check_angles(self):
    if self.angle1 + self.angle2 + self.angle3 == 180:
      return True
    else:
      return False

my_triangle = (triangle(90,30,60))

print(my_triangle.number_of_sides)
print(my_triangle.check_angles())
