import h5py
import os
import numpy as np
from numpy import linalg as LA
from operator import itemgetter

taskId = 3
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

srcDir = 'weights/2/'
src_files = os.listdir(srcDir)
num_nodes = len(src_files)
num_keep = num_nodes-int(np.floor(num_nodes*remove_percent))

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
valid_file = [item[0] for item in file_acc[:num_keep]]
num_valid = len(valid_file)

model = model_base
base_dir = os.path.join(srcDir, valid_file[0])
if os.path.isfile(base_dir):
	model.load_weights(base_dir)
else:
	print('No valid weights.')

avg = model.get_weights()
num_layers = len(avg)

counter = 1.0
src_files = os.listdir(srcDir)
for idx in range(1,num_valid):
	f = valid_file[idx]
	full_f = os.path.join(srcDir, f)
	tmp_model.load_weights(full_f)
	cur_weight = tmp_model.get_weights()
	for i in range(num_layers):
		avg[i] = (avg[i]*counter+cur_weight[i])/(counter+1)
	counter = counter+1

model.set_weights(avg)
save_dir = os.path.join(srcDir, 'avg.h5')
model.save(save_dir)

# Evaluate performance of avg.h5 
model.compile(loss='binary_crossentropy',
			optimizer='adam', metrics=['accuracy'])
_, acc = model.evaluate(x_test, y_test, batch_size=30)
print('Accuracy of averaged weights:', acc)

# check the nodeId of the closest weight
winId = 0
minDist = 1000000.0
# For tie breaking, select the first encountered minDist one 
# Which means the closest one with highest acc itself

for idx in range(num_valid):
	f = valid_file[idx]
	curId = f[3]
	full_f = os.path.join(srcDir, f)
	tmp_model.load_weights(full_f)
	cur_weight = tmp_model.get_weights()
	curDist = 0.0
	for i in range(num_layers):
		curDist = curDist+(LA.norm(cur_weight[i]-avg[i]))**2
	if curDist < minDist:
		minDist = curDist
		winId = curId
print('Winner nodeId:', winId)

exit()