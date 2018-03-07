'''This script goes along the blog post
"Building powerful image classification models using very little data"
from blog.keras.io.
It uses data that can be downloaded at:
https://www.kaggle.com/c/dogs-vs-cats/data
In our setup, we:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created cats/ and dogs/ subfolders inside train/ and validation/
- put the cat pictures index 0-999 in data/train/cats
- put the cat pictures index 1000-1400 in data/validation/cats
- put the dogs pictures index 12500-13499 in data/train/dogs
- put the dog pictures index 13500-13900 in data/validation/dogs
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''

import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
from keras.backend.tensorflow_backend import set_session
import os.path
import argparse
from model import model
from keras.callbacks import ModelCheckpoint, Callback
import time

# Restrict GPU memory
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.visible_device_list = "0"
set_session(tf.Session(config=config))

parser = argparse.ArgumentParser()
parser.add_argument("--batch_size", "-b", type=int, help="batch size", default=20)
parser.add_argument("--epochs", "-e", type=int, help="number of epochs", default=10)
parser.add_argument("--num_train", "-t", type=int, help="number of training data", default=6000)
parser.add_argument("--num_val", "-v", type=int, help="number of validation data", default=2400)
parser.add_argument("--node_id", "-n", type=str, help="id of node", default=0)
parser.add_argument("--task_id", "-k", type=str, help="id of task", default=0)
args = parser.parse_args()
# dimensions of our images.
img_width, img_height = 150, 150

# train_data_dir = '../data/train'
# validation_data_dir = '../data/validation'
train_data_dir = './data/'+args.node_id+'/tasks/'+args.task_id+'/data/train'
validation_data_dir = './data/'+args.node_id+'/tasks/'+args.task_id+'/data/validation'
nb_train_samples = args.num_train
nb_validation_samples = args.num_val

batch_size = args.batch_size
epochs = args.epochs # originally 50

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = model(input_shape)

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# fname = 'tmp.h5'
fname = './data/'+args.node_id+'/tasks/'+args.task_id+'/model/tmp.h5'

if os.path.isfile(fname):
    model.load_weights(fname)
    print('weights loaded.')
else:
    print('No weights found. Start training.')

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# callback for printing out the total training time up to currently finished epoch
class TimeHistory(Callback):
    def on_train_begin(self, logs={}):
        self.times = 0.0
    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()
    def on_epoch_end(self, batch, logs={}):
        self.times = self.times + time.time() - self.epoch_time_start
        print(self.times)

checkpoint = ModelCheckpoint(fname, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
time_callback = TimeHistory()
callbacks_list = [checkpoint, time_callback]
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    callbacks=callbacks_list)

# model.save_weights(fname)

exit()