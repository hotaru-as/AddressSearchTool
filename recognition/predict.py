import numpy as np
from . import layer
import cv2
import os

class Predict():
  def predict(self, img):
    n_in = 784 # 入力層のニューロン数
    n_out = 10 # 出力層のニューロン数
    n_middle = 1024

    middle_layer = layer.MiddleLayer(n_in, n_middle)
    output_layer = layer.OutputLayer(n_middle, n_out)

    npz_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.npz')
    npz = np.load(npz_name)

    middle_layer.w = npz['arr_0']
    middle_layer.b = npz['arr_1']
    output_layer.w = npz['arr_2']
    output_layer.b = npz['arr_3']

    img = cv2.resize(img, (28, 28))
    img = cv2.bitwise_not(img) # 学習データに合わせて白黒反転
    img = img / 255

    middle_layer.forward(img.reshape(1, 784))
    output_layer.forward(middle_layer.y)
    y = output_layer.y.reshape(-1)

    return np.argmax(y).item()


