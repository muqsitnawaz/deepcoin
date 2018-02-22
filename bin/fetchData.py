import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("taskId", type=int, help="task ID")
parser.add_argument("nodeId", type=int, help="node ID")
parser.add_argument("num_nodes", type=int, help="total number of nodes")
args = parser.parse_args()

#inputs
nodeId = args.nodeId
num_nodes = args.num_nodes
taskId = args.taskId

threshold = 0.0
localDir = './data/'+str(nodeId)+'/tasks/'+str(taskId)+'/'
localDataDir = localDir+'data/'
localModelDir = localDir+'model/'
if not os.path.exists(localDir):
	os.makedirs(localDir)
if not os.path.exists(localDataDir):
	os.makedirs(localDataDir)
if not os.path.exists(localModelDir):
	os.makedirs(localModelDir)

# Copy model and optional weights if not there
srcDir = './tasks/'+str(taskId)+'/model/'
src_files = os.listdir(srcDir)
for file_name in src_files:
    full_file_name = os.path.join(srcDir, file_name)
    if (os.path.isfile(full_file_name)):
      if not(os.path.isfile(localModelDir+file_name)):
        shutil.copy(full_file_name, localModelDir)

# Parse meta.txt
for line in open('./tasks/'+str(taskId)+'/meta.txt'):
  fields = line.split(':')
  # print(fields[0][:5])
  if fields[0] == 'threshold':
    threshold = fields[1]
    print(threshold)
  else:
    if not os.path.exists(localDataDir+fields[0]+'/'):
      os.makedirs(localDataDir+fields[0]+'/')

    num_data = int(fields[1])
    lIdx = num_data/num_nodes*(nodeId-1)
    rIdx = lIdx+num_data/num_nodes

    srcDir = './tasks/'+str(taskId)+'/data/'
    src_files = os.listdir(srcDir+fields[0]+'/')
    if len(src_files)==int(fields[1]):  
      for file_name in src_files[int(lIdx):int(rIdx)]:
          full_file_name = os.path.join(srcDir+fields[0]+'/', file_name)
          if (os.path.isfile(full_file_name)):
            if not(os.path.isfile(localDataDir+fields[0]+'/'+file_name)):
              shutil.copy(full_file_name, localDataDir+fields[0]+'/')
    else:
      for file_name in src_files:
          full_file_name = os.path.join(srcDir+fields[0]+'/', file_name)
          if (os.path.isfile(full_file_name)):
            if not(os.path.isfile(localDataDir+fields[0]+'/'+file_name)):
              shutil.copy(full_file_name, localDataDir+fields[0]+'/')

exit()