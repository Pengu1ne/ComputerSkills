'''
An exercise in tensor flow. How to do DL program from scratch.
'''

#####     Preparation of data

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras

img_rows, img_cols = 28, 28
num_classes = 10

def prep_data(raw):
    y = raw[:,0]
    out_y = keras.utils.to_categorical(y, num_classes)

    x = raw[:,1:]
    num_imgs = raw.shape[0]
    out_x = x.reshape(num_imgs, img_rows, img_cols, 1)
    out_x = out_x / 225
    return out_x, out_y

fashion_file = "../input/fashionmnist/fashion-mnist_train.csv"
fashion_data = np.loadtxt(fashion_file, skiprows=1, delimiter=',')
x, y = prep_data(fashion_data)


#####     Start the model

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D

num_classes = 10

my_model = Sequential()


#####     Add the first  layer

my_model.add(Conv2D(12, activation='relu', kernel_size=3, input_shape=(img_rows, img_cols, 1)))

#####     Add the remaining layers

my_model.add(Conv2D(20, activation='relu', kernel_size=3))
my_model.add(Conv2D(20, activation='relu', kernel_size=3))
my_model.add(Flatten)
my_model.add(Dense(100, activation='relu'))
my_model.add(Dense(10, activation='softmax'))

#####     Compile the model

my_model.compile(loss=keras.losses.categorical_crossentropy, 
                 optimizer='adam', metrics=['accuracy'])

#####     Fit the model

my_model.fit(x, y, batch_size=128, epochs=2, validation_split=0.2)


#####     Second fashion model

my_second_model = Sequential()
my_second_model.add(Conv2D(12, activation='relu', kernel_size=3, input_shape=(128, 128, 1)))
# Changed kernel size
my_second_model.add(Conv(20, activation='relu', kernel_size=2))
my_second_model.add(Conv(20, activation='relu', kernel_size=2))
# Added an addition convolution 2D layer
my_second_model.add(Conv2D(20, activation='relu', kernel_size=2))
my_second_model.add(Flatten())
my_second_model.add(Dense(100, activation='relu'))
# It is important to change the last layer.
# First arg. matches num_classes.
#Softmax guarantees we get reasonable probabilities
my_second_model.add(Dense(10, activation='softmax'))

my_second_model.compile(loss='catecorigal_crossentropy', optimizer='adam', metrics=['accuracy'])

my_second_model.fit(x,y, batch_size=100, epochs=4, validation_split=0.2)
