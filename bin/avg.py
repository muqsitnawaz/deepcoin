import h5py
import os
import numpy as np
import gc
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--task_id", "-k", type=str, help="id of task", default=0)
args = parser.parse_args()

task_id = args.task_id

model_dir = './tasks/'+str(task_id)+'/model/'
sys.path.append(model_dir)

from model import model

print('Loading model...')
model_base = model()
print('Model Loaded.')

model = model_base
base_weights_dir='./data/1/tasks/'+task_id+'/model/tmp.h5'
if os.path.isfile(base_weights_dir):
	print('Loading '+base_weights_dir)
	model.load_weights(base_weights_dir)
	print('Weight loaded.')
else:
	print('Base weight required.')

srcDirs = []

nodes = os.listdir('./data')
for node in nodes:
	srcDirs.append('./data/'+node+'/tasks/'+task_id+'/model/')

avg = model.get_weights()
num_layers = len(avg)

counter = 1.0
for srcDir in srcDirs:
	full_f = os.path.join(srcDir, 'tmp.h5')
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

model.set_weights(avg)
model.save('./tasks/'+task_id+'/model/avg.h5')
print('Model average saved.')
exit()