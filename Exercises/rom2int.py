'''
In this exercise, I go through classes and how to turn roman numbers to integers.
The exercise can be found from:
https://www.w3resource.com/python-exercises/class-exercises/
'''

import numpy as np
import matplotlib.pyplot as plt

class rom2int:
  def rom_to_int(self,s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M':1000}
    int_val = 0
    for i in range(len(s)):
      if i > 0 and rom_val[s[i]] > rom_val[s[i-1]]:
        int_val += ronm_val[s[i]] - 2 * rom_val[s[i - 1]]
      else:
        int_val += rom_val[s[i]]
    return int_val

print(rom2int().rom_to_int('C'))
print(rom2int().rom_to_int('MDIIII'))
