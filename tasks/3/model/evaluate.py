from model import model
from load_data import load_data
from keras.preprocessing import sequence

fname = 'avg.h5'
model = model()
model.load_weights(fname)
print('Weight loaded.')
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Loading data..')
(x_train, y_train), (x_test, y_test) = load_data()
x_test = sequence.pad_sequences(x_test, maxlen=100)

score, acc = model.evaluate(x_test, y_test, batch_size=30)
print('Test score:', score)
print('Test accuracy:', acc)