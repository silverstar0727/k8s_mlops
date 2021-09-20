import tensorflow as tf
from tensorflow import keras

from minio import Minio

import numpy as np
import datetime
import sys

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
    keras.layers.Dense(10, activation='softmax')
])

#compile
model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
# training
model.fit(train_images, train_labels, epochs=5)
# evaluation
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\n테스트 정확도:', test_acc)

model_name = 'model-%s.h5' % datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
model_path = "/model_storage/" + model_name
model.save(model_path)
