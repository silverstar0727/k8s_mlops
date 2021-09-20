import sys
import tensorflow as tf
from tensorflow import keras

epochs = int(sys.argv[1]) # 인자로 epochs를 받아서 int로 변환
activate = sys.argv[2] # 인자로 activate를 받기 
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
    keras.layers.Dense(128, activation=activate), # 인자로 받은 activation function을 활용
    keras.layers.Dense(10, activation='softmax') 
])

#compile
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# training
model.fit(train_images, train_labels, epochs=epochs) # 인자로 받은 epochs를 활용
# evaluation
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\n테스트 정확도:', test_acc)