#####     Create image paths

import os
from os.path import join

hot_dog_image_dir = '../inout/hot_dog_not_hot_dog/seefood/train/hot_dog'
not_hot_dog_image_dir = '../input/hot_dog_not_hot_dog/seefood/train/not_hot_dog'

filenames_h = ['100288.jpg','127117.jpg']
filenames_n = ['823536.jpg','99890.jpg']

hot_dog_paths = [join(hot_dog_image_dir, filename) for filename in filenames_h]
not_hot_dog_paths = [join(not_hot_dog_image_dir, filename) for filename in filenames_n]

img_paths = hot_dog_paths + not_hot_dog_paths



#####     Run an example model

from IPython.display import Image, display
from learntools.deep_learning.decode_predictions import decode_predictions
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensroflow.keras.applications. import ResNet50
from tensorflow.keras.preprocessing.image import load_img, img_to_array

img_size = 224

def read_and_prep_images(img_paths, img_height=img_size, img_width=img_size):
    imgs = [load_img(img_path, target_size=(img_height, img_width)) for img_path in img_paths]
    img_array = np.array([img_to_array(img) for img in imgs])
    output = preprocess_input(img_array)
    return(output)

my_model = ResNet50(weights='../input/resnet/resnet50_weights_tf_dim_ordering_tf_kernels.h5')
test_data = read_and_prep_images(img_paths)
preds = my_model.predict(test_data)

most_likely_labels = decode_predictions(preds, top=3)



#####     Visualize predictions

for i,img_path in enumerate(img_paths):
    display(Image(img_path))
    print(most_likely_labels[i])



#####     Set up code checking

from learnools.core import binder
binder.bind(globals())
from learntools.deep_learning.exercise import *



#####     EXERSICE

decoded = decode_predictions(preds, top=1)
print(decoded)

def is_hot_dog(preds):
    decoded = decode_preditions(preds, top=1)

    labels = [d[0][1] for d in decoded]
    out = [l == 'hotdog' for l in labels]
    return out

def calc_accuracy(model, paths_to_imgs, paths_to_other_imgs):
    # We'll use the counts for denominator of acc. calculation
    num_images = len(paths_to_imgs)
    num_other_images = len(paths_to_other_imgs)

    image_data = read_and_prep_images(paths_to_imgs)
    preds_for_data = model.predict(image_data)
    # Summing list of binary variables gives a count of True Values
    num_correct_preds = sum(is_right(preds_for_data))

    other_img_data = read_and_prep_images(paths_to_other_imgs)
    preds_other_images = model.predict(other_image_data)
    # Number correct is the judged not to be hotdogs
    num_correct_other_preds = num_other_images - sum(is_right(preds_other_images))

    total_correct = num_correct_preds + num_correct_other_preds
    total_preds = num_images + num_other_images
    return total_correct / total_preds

my_model_accuracy = calc_accuracy(my_model, hot_dog_paths, not_hot_dog_paths)
print("Fraction correct in small test set: {}".format(my_model_accuracy))
