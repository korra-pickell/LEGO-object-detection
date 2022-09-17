import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Conv2D, Input, Dropout, BatchNormalization
import os, random, time
import numpy as np
from sklearn.utils import shuffle
from tensorflow.python.keras import activations
from tensorflow.python.keras.layers.core import Activation
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

from PIL import Image
import matplotlib.pyplot as plt 

IMG_DIM = 32
IMG_DEPTH = 3
BATCH_SIZE = 128
NUM_CLASSES = 200
EPOCHS = 10000
DATA_CUTOFF = 800000


data_file = 'C:\\DATA-FAST\\NPY\\brick\\class\\64\\brick-32-rgb.npz'

def get_dataset(data_file,train_split=0.90,val_split=0.05):
    
    data = np.load(data_file,allow_pickle=True)
    data_x = data['x']
    data_y = data['y']

    

    #data_x = data_x.reshape(len(data_x),IMG_DIM,IMG_DIM,1)

    #im = Image.fromarray(data_x[0]*255)
    #im.show()

    data_x_shuf, data_y_shuf = shuffle(data_x,data_y,random_state=0)
    data_x_shuf, data_y_shuf = data_x_shuf[:DATA_CUTOFF], data_y_shuf[:DATA_CUTOFF]

    split_point = int(len(data_x_shuf)*train_split)
    val_point = int(len(data_x_shuf)*(train_split+val_split))

    train_x,train_y = data_x_shuf[:split_point],data_y_shuf[:split_point]
    test_x,test_y = data_x_shuf[split_point:val_point],data_y_shuf[split_point:val_point]
    val_x,val_y = data_x_shuf[val_point:],data_y_shuf[val_point:]

    return train_x,train_y,test_x,test_y,val_x,val_y

def get_class_model():
    model = Sequential()

    #model.add(Input(shape=(IMG_DIM,IMG_DIM,1),batch_size=BATCH_SIZE))

    model.add(Conv2D(32,(3,3),padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(BatchNormalization())
    #model.add(Dropout(0.2))

    model.add(Conv2D(64,(3,3),padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(BatchNormalization())
    #model.add(Dropout(0.2))
    
    model.add(Conv2D(64,(3,3),padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(BatchNormalization())
    #model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(NUM_CLASSES*2))
    model.add(Activation('relu'))
    #model.add(Dropout(0.2))

    model.add(Dense(NUM_CLASSES*2))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    

    model.add(Dense(NUM_CLASSES))
    model.add(Activation('softmax'))

    return model
    
train_x,train_y,test_x,test_y,val_x,val_y = get_dataset(data_file)

model = get_class_model()

log_dir = 'C:\\DATA-FAST\\brick-class\\Models\\Classifier\\logs\\'+str(time.time())
tensorboard_callback = TensorBoard(log_dir=log_dir,histogram_freq=1)
save_callback = ModelCheckpoint(log_dir+'\\models\\brick-class-cnn.hdf5',monitor='loss',verbose=1,save_best_only=True,mode='auto',period=1)

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
#model.summary()

model.fit(x=train_x,y=train_y,validation_data=(val_x,val_y), batch_size=BATCH_SIZE,epochs=EPOCHS,verbose=1,callbacks=[tensorboard_callback,save_callback])