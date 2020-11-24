'''
In this exercise I practice Python classes and convert integer to Roman numbers
The exercise is found from the internet:
https://www.w3resource.com/python-exercises/class-exercises/
'''

import numpy as np
import matplotlib.pyplot as plt

class int2rom:
  def int_to_rom(self, num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']

    rom_num = ''
    i = 0
    while num > 0:
      for _ in range(num // val[i]):
        rom_num += syb[i]
        num -= val[i]
      i += 1
    return rom_num

print(int2rom().int_to_rom(1))
print(int2rom().int_to_rom(1504))
