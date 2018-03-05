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

max_features = 20000
maxlen = 100
'''
Note:
batch_size is highly sensitive.
Only 2 epochs are needed as the dataset is very small.
'''

def load_data(path1='../data/train/train.npz',path2='../data/validation/test.npz',
			  num_words=None, skip_top=0,
              maxlen=None, seed=113,
              start_char=1, oov_char=2, index_from=3, **kwargs):
    """Loads the IMDB dataset.
    # Arguments
        path: where to cache the data (relative to `~/.keras/dataset`).
        num_words: max number of words to include. Words are ranked
            by how often they occur (in the training set) and only
            the most frequent words are kept
        skip_top: skip the top N most frequently occurring words
            (which may not be informative).
        maxlen: sequences longer than this will be filtered out.
        seed: random seed for sample shuffling.
        start_char: The start of a sequence will be marked with this character.
            Set to 1 because 0 is usually the padding character.
        oov_char: words that were cut out because of the `num_words`
            or `skip_top` limit will be replaced with this character.
        index_from: index actual words with this index and higher.
    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    # Raises
        ValueError: in case `maxlen` is so low
            that no input sequence could be kept.
    Note that the 'out of vocabulary' character is only used for
    words that were present in the training set but are not included
    because they're not making the `num_words` cut here.
    Words that were not seen in the training set but are in the test set
    have simply been skipped.
    """
    # Legacy support
    if 'nb_words' in kwargs:
        warnings.warn('The `nb_words` argument in `load_data` '
                      'has been renamed `num_words`.')
        num_words = kwargs.pop('nb_words')
    if kwargs:
        raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))

    # path1 = get_file(path1)
    # path2 = get_file(path2)
    with np.load(path1) as f:
        x_train, labels_train = f['x_train'], f['y_train']
    with np.load(path2) as f:
        x_test, labels_test = f['x_test'], f['y_test']

    np.random.seed(seed)
    indices = np.arange(len(x_train))
    np.random.shuffle(indices)
    x_train = x_train[indices]
    labels_train = labels_train[indices]

    indices = np.arange(len(x_test))
    np.random.shuffle(indices)
    x_test = x_test[indices]
    labels_test = labels_test[indices]

    xs = np.concatenate([x_train, x_test])
    labels = np.concatenate([labels_train, labels_test])

    if start_char is not None:
        xs = [[start_char] + [w + index_from for w in x] for x in xs]
    elif index_from:
        xs = [[w + index_from for w in x] for x in xs]

    if maxlen:
        xs, labels = sequence._remove_long_seq(maxlen, xs, labels)
        if not xs:
            raise ValueError('After filtering for sequences shorter than maxlen=' +
                             str(maxlen) + ', no sequence was kept. '
                             'Increase maxlen.')
    if not num_words:
        num_words = max([max(x) for x in xs])

    # by convention, use 2 as OOV word
    # reserve 'index_from' (=3 by default) characters:
    # 0 (padding), 1 (start), 2 (OOV)
    if oov_char is not None:
        xs = [[w if (skip_top <= w < num_words) else oov_char for w in x] for x in xs]
    else:
        xs = [[w for w in x if skip_top <= w < num_words] for x in xs]

    idx = len(x_train)
    x_train, y_train = np.array(xs[:idx]), np.array(labels[:idx])
    x_test, y_test = np.array(xs[idx:]), np.array(labels[idx:])

    return (x_train, y_train), (x_test, y_test)


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