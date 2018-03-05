from model import model
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

validation_data_dir = '../data/validation'
fname = 'avg.h5'
img_width, img_height = 150, 150
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=20,
    class_mode='binary')

model = model(input_shape)
model.load_weights(fname)
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
score, acc = model.evaluate_generator(validation_generator)
print('Test score:', score)
print('Test accuracy:', acc)