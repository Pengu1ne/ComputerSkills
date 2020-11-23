'''
We create a RGB converter. In other words, this code converts RGB to Hex and vice versa.
'''

def rgb_hex():
  invalid_msg = 'Error. The value you try to convert is invalid.'
  
  red = int(input('Define the amount of red: '))
  if red < 0 or red > 225:
    print(invalid_msg)
    return

  green = int(input('Define the amount of green: '))
  if green < 0 or green > 225:
    print(invalid_msg)
    return

  blue = int(input('Define the amount of blue: '))
  if blue < 0 or blue > 225:
    print(invalid_msg)
    return
  
  val = (red << 16) + (green << 8) + blue
  print('The color in hexadecimal is %s' % (hex(val)[2:].upper()))

def hex_rgb():
  invaliv_msg = 'Error. The value you try to convert is invalid.'
  
  hex_value = input('Define the hexadecimal value: ')
  if len(hex_value) != 6:
    print(invalid_msg)
    return
  else:
    hex_value = int(hex_value, 16)

  two_hex_digits = 2**8

  blue = hex_value % two_hex_digits
  
  hex_value = hex_value >> 8
  green = hex_value % two_hex_digits

  hex_value = hex_value >> 8
  red = hex_value % two_hex_digits

  print('The RGB values are: %s(R), %s(G), %s(B)' % (red, green, blue))

def convert():
  while True:
    option = input('Select 1 to convert RGB to hex, 2 to convert hex to RGB, and X to exit: ')
    if option == '1':
      print('----RGB to Hex----')
      rgb_hex()

    elif option == '2':
      print('----Hex to RGB----')
      hex_rgb()

    elif option == 'x' or option == 'X':
      print('Exiting program.')
      break

    else:
      print('Error. Invalid choice.')
      return

convert()
