'''
This code ciphers and dechipers messages through Enigma.

- Current version runs files with an explicit structure. More information on example file.
- To be added:
    --print message in more readable form

---Pengu1ne
'''


import time
alphabet = 'abcdefghijklmnopqrstuvwxyz'

''' Read the file line by line and turn it lower case '''
with open('test_iii.txt', 'r') as file:
    lines = file.readlines()

'''
Constants
'''
shift = int(lines[1])
msg = lines[5]
l = len(msg)-1
msg = msg[:l]
crypt = lines[0]
crypt = crypt[:6]

add_shift = []
for a in range(l):
    add_shift.append(shift+a)

''' 
The shift. Includes both encoding and decoding, thus, this part is called for 
different purposes later.
'''
def shift_letters(message):
    indexes = []
    new_msg = []

    if crypt == 'decode':
        for i in message:
            indexes.append(alphabet.find(i))

        for j in range(l):
            new_msg.append(alphabet[(indexes[j]-add_shift[j])%26])

    else:
        for i in message:
            indexes.append(alphabet.find(i))

        for j in range(l):
            new_msg.append(alphabet[(indexes[j]+add_shift[j])%26])

    return new_msg


''' 
Encoding i.e. running the message through rotors. The function calls previous 
function for shifted letters.
'''
def rotors_en():
    r       = 1
    shifted = shift_letters(msg)
    indexes = []
    rotored = []

    while r < 4:
        r +=1
        tobe_rotored = []

        '''
        The indexes are determined.
        '''
        if r == 2:
            indexes = []
            for i in shifted:
                indexes.append(alphabet.index(i))
        else:
            indexes = []
            for i in rotored:
                indexes.append(alphabet.index(i))

        '''
        Looping through rotors.
        '''
        for j in indexes:
            tobe_rotored.append(lines[r][j])
            rotored = tobe_rotored
    return rotored


'''
The decoding i.e.  going rotors backwards.
'''

def rotor_de():
    r       = 5
    indexes = []
    rotored = []

    while r > 2:
        r -=1
        tobe_rotored = []

        '''
        Determining indexes
        '''
        if r == 4:
            for i in msg:
                indexes.append(lines[r].index(i))
        else:
            indexes = []
            for i in rotored:
                indexes.append(lines[r].find(i))

        '''
        Going back through rotors
        '''
        for j in indexes:
            tobe_rotored.append(alphabet[j])
            rotored = tobe_rotored
    return rotored


''' 
Encode or decode 
'''
def read_msg():
    if crypt == 'decode':
        print('Decoding...')
        time.sleep(1)
        print('The decoded message is:')
        print(shift_letters(rotor_de()))
    elif crypt == 'encode':
        print('Encoding...')
        time.sleep(1)
        print('The encoded message is:')
        print(rotors_en())

''' Run the code - and the right answer for the test runs'''
read_msg()
#print(rotor_de())
#print(shifted_letters(rotor_de()))
