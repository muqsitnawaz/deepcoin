'''Train a recurrent convolutional network on the IMDB sentiment
classification task.
Gets to 0.8498 test accuracy after 2 epochs. 41s/epoch on K520 GPU.
Follow default! epoch num = 3 will overfit!
'''
from __future__ import print_function

from keras.preprocessing import sequence
from keras.utils.data_utils import get_file
import numpy as np
import os.path
import argparse
from model import model
from keras.callbacks import ModelCheckpoint, Callback
import time
from load_data import load_data

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--batch_size", "-b", type=int, help="batch size", default=30)
parser.add_argument("--epochs", "-e", type=int, help="number of epochs", default=2)
parser.add_argument("--num_train", "-t", type=int, help="number of training data", default=25000)
parser.add_argument("--num_val", "-v", type=int, help="number of validation data", default=25000)
args = parser.parse_args()

# Training
batch_size = args.batch_size
epochs = args.epochs
num_train = args.num_train
num_val = args.num_val

max_features = 20000
maxlen = 100
'''
Note:
batch_size is highly sensitive.
Only 2 epochs are needed as the dataset is very small.
'''

print('Loading data...')
train_dir = '../data/train/'
test_dir = '../data/validation/'
(x_train, y_train), (x_test, y_test) = load_data(train_dir+'train.npz',test_dir+'test.npz',
										num_words=max_features)

print(len(y_train), 'train sequences')
print(len(y_test), 'test sequences')

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
x_train = x_train[:num_train]
y_train = y_train[:num_train]
x_test = x_test[:num_val]
y_test = y_test[:num_val]
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

print('Build model...')

model = model(max_features, maxlen)

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

fname = 'tmp.h5'
if os.path.isfile(fname):
    model.load_weights(fname)
    print('weights loaded.')
else:
    print('No weights found. Start training.')

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

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          callbacks=callbacks_list)

# model.save_weights(fname)

exit()