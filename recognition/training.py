from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
import time
import layer
from PIL import Image
import os

def get_data():
  # MNIST ダウンロード
  X, y = datasets.fetch_openml('mnist_784', return_X_y=True)

  # one-hot vector
  lb = preprocessing.LabelBinarizer()
  y_v = lb.fit_transform(y)

  # 学習データとテストデータに分ける
  X_train, X_test, y_train, y_test = train_test_split(
    X / 255, # ピクセル値を0-1に変換
    y.astype('int64'), # 文字列のラベルデータを数値に変換
    stratify = y,
    random_state = 0
  )

  lb = preprocessing.LabelBinarizer()
  y_train = lb.fit_transform(y_train)
  y_test = lb.fit_transform(y_test)

  return [X_train, X_test, y_train, y_test]

n_in = 784 # 入力層のニューロン数
n_out = 10 # 出力層のニューロン数
n_middle = 1024

epoch = 70
interval = 5

eta = 0.1 # 学習係数

def training(X_train, X_test, y_train, y_test, extend=False):

  middle_layer = layer.MiddleLayer(n_in, n_middle)
  output_layer = layer.OutputLayer(n_middle, n_out)

  # 学習済みモデルをさらに学習させる場合
  if extend:
    npz_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_correct_extend.npz')
    npz = np.load(npz_name)

    middle_layer.w = npz['arr_0']
    middle_layer.b = npz['arr_1']
    output_layer.w = npz['arr_2']
    output_layer.b = npz['arr_3']

  for i in range(epoch):

    index_random = np.arange(len(X_train))
    np.random.shuffle(index_random)

    total_error = 0
    
    for idx in index_random:
      x = X_train[idx]
      t = y_train[idx]

      #順伝播
      middle_layer.forward(x.reshape(1, 784))
      output_layer.forward(middle_layer.y)

      #逆伝播
      output_layer.backward(t.reshape(1, 10))
      middle_layer.backward(output_layer.grad_x)

      middle_layer.update(eta)
      output_layer.update(eta)

      if i % interval == 0:
        y = output_layer.y.reshape(-1)

        total_error += -np.sum(t * np.log(y + 1e-7))

    print(str(i) + ' - ' + str(time.gmtime().tm_hour) + ':' + str(time.gmtime().tm_min))
    if i % interval == 0:
      print("Epoch:" + str(i) + "/" + str(epoch), "Error:" + str(total_error/len(y_train)))

      np.savez('model_correct_extend2.npz', 
      middle_layer.w, middle_layer.b, 
      output_layer.w, output_layer.b)

  test_error = 0
  for idx in range(len(X_test)):
    x = X_test[idx]
    t = y_test[idx]

    middle_layer.forward(x.reshape(1, 784))
    output_layer.forward(middle_layer.y)

    y = output_layer.y.reshape(-1)

    if np.argmax(y) != np.argmax(t):
      test_error += 1

  print("test error : " + str(test_error) + "count " + str(test_error / len(X_test)))

if __name__ == "__main__":
  X_train, X_test, y_train, y_test = get_data()
  training(X_train, X_test, y_train, y_test, False)
