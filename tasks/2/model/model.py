from keras.models import Sequential
from keras.layers import LSTM,Dense

def model():
	model = Sequential()
	model.add(LSTM(256,input_shape=(7,1)))
	model.add(Dense(1))
	return model