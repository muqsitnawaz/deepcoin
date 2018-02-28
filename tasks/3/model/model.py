from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Conv1D, MaxPooling1D


def model(max_features = 20000, maxlen = 100):
	# Embedding
	embedding_size = 128
	# Convolution
	kernel_size = 5
	filters = 64
	pool_size = 4
	# LSTM
	lstm_output_size = 70

	model = Sequential()
	model.add(Embedding(max_features, embedding_size, input_length=maxlen))
	model.add(Dropout(0.25))
	model.add(Conv1D(filters,
	                 kernel_size,
	                 padding='valid',
	                 activation='relu',
	                 strides=1))
	model.add(MaxPooling1D(pool_size=pool_size))
	model.add(LSTM(lstm_output_size))
	model.add(Dense(1))
	model.add(Activation('sigmoid'))
	return model