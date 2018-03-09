import h5py
import os
import numpy as np
from numpy import linalg as LA
from operator import itemgetter

taskId = 2
model_dir = '~/efs/tasks/'+str(taskId)+'/model/'
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
(x_train, y_train), (x_test, y_test) = load_data(path1='~/efs/tasks/'+str(taskId)+'/data/train/train.npz',
											path2='~/efs/tasks/'+str(taskId)+'/data/validation/test.npz',)
x_test = sequence.pad_sequences(x_test, maxlen=100)
print('Data loaded.')

srcDir = '~/efs/data/'
src_folders = os.listdir(srcDir)
src_folders = [x for x in src_folders if os.path.isdir(x)]

file_acc = {}
tmp_model = model_base
tmp_model.compile(loss='binary_crossentropy',
				optimizer='adam', metrics=['accuracy'])
for i in range(len(src_folders)):
	nodeId = src_folders[i]
	full_f = srcDir+nodeId+'/tasks/'+str(taskId)+'/tmp.h5'
	if os.path.isfile(full_f):
		tmp_model.load_weights(full_f)
		_, acc = tmp_model.evaluate(x_test, y_test, batch_size=30)
		print('Accuracy of', nodeId, acc)
		file_acc[nodeId]=acc

file_acc = sorted(file_acc.items(), key=itemgetter(1), reverse=True)

print(file_acc[0][0])

# save opt.h5 to all nodes
winDir = srcDir+file_acc[0][0]+'/tasks/'+str(taskId)+'/tmp.h5'
tmp_model.load_weights(winDir)
for i in range(len(src_folders)):
	save_dir = srcDir+src_folders[i]+'/tasks/'+str(taskId)+'/opt.h5'
	tmp_model.save(save_dir)

exit()