import h5py
import os
import numpy as np
from operator import itemgetter

taskId = 1
nb_validation_samples = 2400
model_dir = 'tasks/'+str(taskId)+'/model/'
import sys
sys.path.append(model_dir)
from model import model
from keras.preprocessing.image import ImageDataGenerator

print('Loading model...')
model_base = model()
print('Done.')

# Node 1 is master
print('Loading validation data...')
validation_data_dir = 'tasks/'+str(taskId)+'/data/validation'
test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow_from_directory(validation_data_dir, target_size=(150, 150),batch_size=20,class_mode='binary')
print('Done.')

srcDir = '~/efs/data/'
src_folders = os.listdir(srcDir)
src_folders = [x for x in src_folders if os.path.isdir(x)] 
print(src_folders)

print('Calculating accuracy...')
file_acc = {}
tmp_model = model_base
tmp_model.compile(loss='binary_crossentropy',
			optimizer='rmsprop',metrics=['accuracy'])
for i in range(len(src_folders)):
	nodeId = src_folders[i]
	full_f = srcDir+nodeId+'/tasks/'+str(taskId)+'/tmp.h5'
	if os.path.isfile(full_f):
		tmp_model.load_weights(full_f)
		_, acc = tmp_model.evaluate_generator(validation_generator,
						steps=nb_validation_samples // 20)
		print('Accuracy of', nodeId, acc)
		file_acc[nodeId]=acc

file_acc = sorted(file_acc.items(), key=itemgetter(1), reverse=True)
print(file_acc[0][0])
print('Done')

# save opt.h5 to all nodes
print('Saving optimal weights...')
winDir = srcDir+file_acc[0][0]+'/tasks/'+str(taskId)+'/tmp.h5'
tmp_model.load_weights(winDir)
for i in range(len(src_folders)):
	save_dir = srcDir+src_folders[i]+'/tasks/'+str(taskId)+'/opt.h5'
	tmp_model.save(save_dir)
print('Done')
exit()