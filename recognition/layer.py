import numpy as np

wb_width = 0.01 # 重みとバイアスの広がり具合(正規分布の広がり具合)

class MiddleLayer:
  def __init__(self, n_upper, n):
    self.w = wb_width * np.random.randn(n_upper, n) #randn : 正規分布
    self.b = wb_width * np.random.randn(n)

  def forward(self, x):
    self.x = x
    u = np.dot(x, self.w) + self.b
    self.y = 1 / (1 + np.exp(-u)) # シグモイド関数関数

  def backward(self, grad_y):
    delta = grad_y * (1 - self.y) * self.y

    self.grad_w = np.dot(self.x.T, delta)
    self.grad_b = np.sum(delta, axis=0)

    self.grad_x = np.dot(delta, self.w.T)

  def update(self, eta):
    self.w -= eta * self.grad_w
    self.b -= eta * self.grad_b


class OutputLayer:
  def __init__(self, n_upper, n):
    self.w = wb_width * np.random.randn(n_upper, n)
    self.b = wb_width * np.random.randn(n)

  def forward(self, x):
    self.x = x
    u = np.dot(x, self.w) + self.b
    self.y = np.exp(u) / np.sum(np.exp(u), axis=1, keepdims=True) # ソフトマックス関数
  
  def backward(self, t):
    delta = self.y - t

    self.grad_w = np.dot(self.x.T, delta)
    self.grad_b = np.sum(delta, axis=0)

    self.grad_x = np.dot(delta, self.w.T)

  def update(self, eta):
    self.w -= eta * self.grad_w
    self.b -= eta * self.grad_b