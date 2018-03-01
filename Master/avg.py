import h5py
import os
import numpy as np
import gc

taskId = 3
model_dir = '../tasks/'+str(taskId)+'/model/'
import sys
sys.path.append(model_dir)
from model import model

print('Loading model...')
model_base = model()
print('Model Loaded.')
model = model_base
base_weights_dir='weights/tmp1.h5'
if os.path.isfile(base_weights_dir):
	print('Loading '+base_weights_dir)
	model.load_weights(base_weights_dir)
	print('Weight loaded.')
else:
	print('Base weight required.')

srcDir = 'weights/'

avg = model.get_weights()
num_layers = len(avg)

counter = 1.0
src_files = os.listdir(srcDir)
for f in src_files:
	if f.endswith(".h5") or f.endswith('.hdf5'):
		full_f = os.path.join(srcDir, f)
		tmp_model = model_base
		if full_f != base_weights_dir:	
			print('Loading '+full_f)
			tmp_model.load_weights(full_f)
			cur_weight = tmp_model.get_weights()
			for i in range(num_layers):
				avg[i] = (avg[i]*counter+cur_weight[i])/(counter+1)
		del tmp_model
		gc.collect()
		counter = counter+1
		# file = h5py.File(f,'r+')
		# dataset = file['/dset']
		# nums.append(dataset[0][0])
model.set_weights(avg)
model.save('avg.h5')