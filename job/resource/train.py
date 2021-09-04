import sys
import tensorflow as tf
from tensorflow import keras

epochs = int(sys.argv[1])
activate = sys.argv[2]
print(sys.argv)

import numpy as np

print(tf.__version__)

# load data
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# data preprocessing
train_images = train_images / 255.0
test_images = test_images / 255.0

# model build
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation=activate)
])

#compile
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# training
model.fit(train_images, train_labels, epochs=epochs)
# evaluation
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\n테스트 정확도:', test_acc)