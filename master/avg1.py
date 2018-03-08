import h5py
import os
import numpy as np
from numpy import linalg as LA
from operator import itemgetter

taskId = 1
nb_validation_samples = 2400
model_dir = '../tasks/'+str(taskId)+'/model/'
import sys
sys.path.append(model_dir)
from model import model
from keras.preprocessing.image import ImageDataGenerator

remove_percent = 0.25

print('Loading model...')
model_base = model()
print('Model Loaded.')
print('Loading data...')
validation_data_dir = '../tasks/'+str(taskId)+'/data/validation'
img_width, img_height = 150, 150
test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow_from_directory(validation_data_dir,
				target_size=(img_width, img_height),batch_size=20,class_mode='binary')
print('Data loaded.')

srcDir = 'weights/1/'
src_files = os.listdir(srcDir)
num_nodes = 0
for f in src_files:
	if f.endswith(".h5") or f.endswith('.hdf5'):
		num_nodes = num_nodes+1

num_keep = num_nodes-int(np.floor(num_nodes*remove_percent))
print('Keep: ', num_keep)

file_acc = {}
tmp_model = model_base
tmp_model.compile(loss='binary_crossentropy',
			optimizer='rmsprop',metrics=['accuracy'])
for f in src_files:
	if f.endswith(".h5") or f.endswith('.hdf5'):
		full_f = os.path.join(srcDir, f)
		tmp_model.load_weights(full_f)
		_, acc = tmp_model.evaluate_generator(validation_generator,
						steps=nb_validation_samples // 20)
		print('Accuracy of', f, acc)
		file_acc[f]=acc

file_acc = sorted(file_acc.items(), key=itemgetter(1), reverse=True)
file_acc = file_acc[:num_keep]

num_valid = len(file_acc)
print(file_acc)
acc_sum = sum([item[1] for item in file_acc])

model = model_base
base_dir = os.path.join(srcDir, file_acc[0][0])
if os.path.isfile(base_dir):
	print('load '+base_dir)
	model.load_weights(base_dir)
else:
	print('No valid weights.')

avg = model.get_weights()
num_layers = len(avg)
for i in range(num_layers):
	avg[i] = avg[i]*file_acc[0][1]/acc_sum

# counter = 1.0
src_files = os.listdir(srcDir)
for idx in range(1,num_valid):
	f = file_acc[idx][0]
	full_f = os.path.join(srcDir, f)
	print('load '+full_f)
	tmp_model.load_weights(full_f)
	cur_weight = tmp_model.get_weights()
	for i in range(num_layers):
		avg[i] = avg[i]+cur_weight[i]*file_acc[idx][1]/acc_sum
		# avg[i] = (avg[i]*counter+cur_weight[i])/(counter+1)
	# counter = counter+1

model.set_weights(avg)
save_dir = os.path.join(srcDir, 'avg.h5')
model.save(save_dir)

# Evaluate performance of avg.h5 
model.compile(loss='binary_crossentropy',
			optimizer='rmsprop',metrics=['accuracy'])
_, acc_avg = model.evaluate_generator(validation_generator,
				steps=nb_validation_samples // 20)
print('Accuracy of averaged weights:', acc_avg)

# check the nodeId of the closest weight
winId = 0
minDist = 1000000.0
# For tie breaking, select the first encountered minDist one 
# Which means the closest one with highest acc itself

for idx in range(num_valid):
	f = file_acc[idx][0]
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