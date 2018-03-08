import h5py
import os
import numpy as np
from operator import itemgetter

taskId = 1
nb_validation_samples = 2400
model_dir = '../tasks/'+str(taskId)+'/model/'
import sys
sys.path.append(model_dir)
from model import model
from keras.preprocessing.image import ImageDataGenerator

print('Loading model...')
model_base = model()
print('Model Loaded.')
print('Loading data...')
validation_data_dir = '../tasks/'+str(taskId)+'/data/validation'
test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow_from_directory(validation_data_dir,
				target_size=(150, 150),batch_size=20,class_mode='binary')
print('Data loaded.')

srcDir = 'weights/1/'
src_files = os.listdir(srcDir)

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

print(file_acc[0][0][3])

exit()