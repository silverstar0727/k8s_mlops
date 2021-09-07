# tensorflow와 tf.keras를 임포트합니다
import tensorflow as tf
from tensorflow import keras

# 헬퍼(helper) 라이브러리를 임포트합니다
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

import datetime
model.save('/model_storage/model-%s.h5' % datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

print('\n테스트 정확도:', test_acc)