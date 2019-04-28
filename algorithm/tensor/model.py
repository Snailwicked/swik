import matplotlib.pyplot as plt
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
import numpy as np
from keras.models import load_model
'''
keras实现神经网络回归模型
'''


'''读取数据并转化为目标矩阵'''
data2dtrain = './data/data2dtrain.txt'
data3dtrain = './data/data3d2train.txt'
data2dtest = './data/data2dtest.txt'
X_dataset = []
Y_dataset = []
X_test = []
with open(data2dtrain ,"r") as fr:
    for item in fr.readlines():
        result = item.replace("\n","").strip().split(" ")
        data = [int(value) for value in result]
        X_dataset.append(data)

with open(data3dtrain ,"r") as fr:
    for item in fr.readlines():
        result = item.replace("\n","").strip().split(" ")
        data = [float(value) for value in result]
        Y_dataset.append(data)

with open(data2dtest ,"r") as fr:
    for item in fr.readlines():
        result = item.replace("\n","").strip().split(" ")
        data = [float(value) for value in result]
        X_test.append(data)
''''''
X_dataset = np.mat(X_dataset)
Y_dataset = np.mat(Y_dataset)
X_test = np.mat(X_test)

'''搭建神经网络模型，训练数据，显示训练结果，并保存模型'''
from sklearn.model_selection import train_test_split
train_X, test_X, train_y, test_y = train_test_split(X_dataset, Y_dataset, test_size=0.25)
model = Sequential()
model.add(Dense(128, input_shape=(12,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(6))
model.compile(loss='mean_squared_error', optimizer=Adam())
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=50, verbose=2)
history = model.fit(train_X, train_y, epochs=300, batch_size=20, validation_data=(test_X, test_y), verbose=2, shuffle=False, callbacks=[early_stopping])
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
model.save("./model.h5")



'''加载模型、测试数据，对二维数据进行预测画出三维图形'''
from mpl_toolkits.mplot3d import Axes3D
model = load_model('model.h5')
# # 预测
yhat = model.predict(X_test)
MatToArray = np.array(yhat)
for item in MatToArray:
    datas = list(item)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = np.linspace(datas[0], datas[3], 100)
    y = np.linspace(datas[1], datas[4], 100)
    z = np.linspace(datas[2], datas[5], 100)


    ax.plot(x, y, z, label='parametric curve')  # 这里传入x, y, z的值
    ax.legend()
    plt.show()
