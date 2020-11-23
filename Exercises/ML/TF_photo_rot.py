#####     Specify the model

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D

num_classes = 2
resnet_weights_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

# Indicate wether the first layer should be trained/changed or not.

my_new_model.layers[0].trainable = False


#####      Compile the model

my_new_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])


#####     Fit model

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorlfow.keras.preprocessing.image import ImageDataGenerator

img_size = 224
data_gen = ImageDataGenerator(preprocess_input)

train_generator = data_gen.flow_from_directory(
                               directory='..input/dogs-gone-sideways(images/train',
                               target_size=(img_size, img_size),
                               batch_size=10,
                               class_mode='categorical')

validation_gen = data_gen.flow_from_directory(
                              directory='../input/dogs-gone-sideways/images/val',
                              target_size=(img_size, img_size),
                              class_mode='categorical')

# fit_stats below saves some statistics describing how model fitting went
# the key role of the following line is how it changes my_new_model by fitting to data

fit_stats = my_new_model.fit_gen(train_gen, steps_per_epoch=3,
                                 validation_data=validation_gen, validation_steps=1)
