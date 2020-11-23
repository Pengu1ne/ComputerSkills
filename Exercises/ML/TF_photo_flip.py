#####     Intro

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D

num_classes = 2
resnet_weights_path = '../input/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

my_new_model.layers[0].trainable = False

my_new_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

# Set up code code checking
#from learntools.core import binder
#binder.bind(globals())
#from learntools.deep_learning.exercise_5 import *
#print("Setup Complete")



#####     Fit model using data augmentation

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

img_size = 224

# Specify the values for all arguments to data_generator_with_aug
data_gen_with_aug = ImageDataGenerator(preprocessing_function=preporcess_input,
                                       horizontal_flip = True,
                                       width_shift_range = 0.1,
                                       height_shift_range = 0.1)

data_gen_no_aug = ImageDataGenerator(preprocessing_function=preprocess_input)



#####     Choosing the aug_model

#specify which type of ImageDataGenerator above is to load in tarining
train_gen = data_gen_with_aug.flow_from_directory(
                                   directory='../input/dogs-gone-sideways/images/train',
                                   target_size=('img_size, img_size'),
                                   class_mode='categorical')

# Specify which type of ImageDataGenerator above is to load in validation data
val_gen = data_gen_no_aug.flow_from_directory(
                                   directory='../input/dogs-gone-sideways/images/val',
                                   target_size=(img_size, img_size),
                                   class_mode='categorical')

my_new_model.fit_generator(train_gen,
                           epochs = 3,
                           steps_per_epoch=19,
                           validation_data=val_gen)
