import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.models import Sequential
from keras.layers import LSTM,Dense
from sklearn.preprocessing import MinMaxScaler
import os.path
import argparse
from model import model

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--batch_size", "-b", type=int, help="batch size", default=10)
parser.add_argument("--epochs", "-e", type=int, help="number of epochs", default=50)
parser.add_argument("--num_train", "-t", type=int, help="number of training data", default=25000)
parser.add_argument("--num_val", "-v", type=int, help="number of validation data", default=25000)
args = parser.parse_args()

batch_size = args.batch_size
epochs = args.epochs

# Any results you write to the current directory are saved as output.

# data = pd.read_csv('../all_stocks_5yr.csv')
# cl = data[data['Name']=='MMM'].close

# scl = MinMaxScaler()
# #Scale the data
# cl = cl.reshape(cl.shape[0],1)
# cl = scl.fit_transform(cl)


# #Create a function to process the data into 7 day look back slices
# def processData(data,lb):
#     X,Y = [],[]
#     for i in range(len(data)-lb-1):
#         X.append(data[i:(i+lb),0])
#         Y.append(data[(i+lb),0])
#     return np.array(X),np.array(Y)
# X,y = processData(cl,7)
# X_train,X_test = X[:int(X.shape[0]*0.80)],X[int(X.shape[0]*0.80):]
# y_train,y_test = y[:int(y.shape[0]*0.80)],y[int(y.shape[0]*0.80):]
# print(X_train.shape[0])
# print(X_test.shape[0])
# print(y_train.shape[0])
# print(y_test.shape[0])

# np.savez('../data/train/train', X_train = X_train, y_train = y_train)
# np.savez('../data/validation/test', X_test = X_test, y_test = y_test)

with np.load('../data/train/train.npz') as f:
        X_train, y_train = f['X_train'], f['y_train']
with np.load('../data/validation/test.npz') as f:
        X_test, y_test = f['X_test'], f['y_test']

print(X_train.shape[0])
print(X_test.shape[0])
print(y_train.shape[0])
print(y_test.shape[0])

#Reshape data for (Sample,Timestep,Features) 
X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))

#import model
model = model()
model.compile(optimizer='adam',loss='mse')

#Fit model with history to check for overfitting
fname = 'tmp.h5'
if os.path.isfile(fname):
    model.load_weights(fname)
    print('weights loaded.')
else:
    print('No weights found. Start training.')

print('Train...')

model.fit(X_train,y_train,
	batch_size=batch_size,
	epochs=epochs,
	validation_data=(X_test,y_test),
	shuffle=False)

#print(model.evaluate(X_test, y_test, batch_size = batch_size))


model.save_weights(fname)

exit()









