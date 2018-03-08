import h5py
import os
import numpy as np
from numpy import linalg as LA
from operator import itemgetter

taskId = 2
model_dir = '../tasks/'+str(taskId)+'/model/'
import sys
sys.path.append(model_dir)
from model import model
from load_data import load_data
from keras.preprocessing import sequence

remove_percent = 0.25

print('Loading model...')
model_base = model()
print('Model Loaded.')
print('Loading data...')
(x_train, y_train), (x_test, y_test) = load_data(path1='../tasks/'+str(taskId)+'/data/train/train.npz',
											path2='../tasks/'+str(taskId)+'/data/validation/test.npz',)
x_test = sequence.pad_sequences(x_test, maxlen=100)
print('Data loaded.')

srcDir = 'weights/'+str(taskId)+'/'
src_files = os.listdir(srcDir)

file_acc = {}
tmp_model = model_base
tmp_model.compile(loss='binary_crossentropy',
				optimizer='adam', metrics=['accuracy'])
for f in src_files:
	if f.endswith(".h5") or f.endswith('.hdf5'):
		full_f = os.path.join(srcDir, f)
		tmp_model.load_weights(full_f)
		_, acc = tmp_model.evaluate(x_test, y_test, batch_size=30)
		print('Accuracy of', f, acc)
		file_acc[f]=acc

file_acc = sorted(file_acc.items(), key=itemgetter(1), reverse=True)

print(file_acc[0][0][3])

exit()