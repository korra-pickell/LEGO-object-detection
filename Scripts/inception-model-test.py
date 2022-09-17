import keras
import numpy as np
import pandas as pd
import os, time
from PIL import Image
from skimage.transform import resize
from random import shuffle

import matplotlib.pyplot as plt
from PIL import Image

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.inception_v3 import preprocess_input

from keras.models import Sequential
from keras.models import Model
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau, TensorBoard
from keras import optimizers, losses, activations, models
from keras.layers import Convolution2D, Dense, Input, Flatten, Dropout, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D, Concatenate
from keras import applications

val_split = 0.1
TARGET_SIZE = (75,75)
INPUT_SHAPE = (75,75,3)
BATCH_SIZE = 512
EPOCHS = 10000

data_dir = 'C:\\DATA-FAST\\brick-class\\64'


#list_paths = []
#for subdir, dirs, files in os.walk(data_dir):
#    for file in files[:1000]:
#        list_paths.append(subdir+os.sep+file)


datagen = ImageDataGenerator(rescale=1.0/255,
            validation_split=val_split)

train_gen = datagen.flow_from_directory(
            data_dir,
            target_size = TARGET_SIZE,
            batch_size = BATCH_SIZE,
            color_mode = 'rgb',
            class_mode = 'categorical',
            shuffle = True,
            seed = 155,
            subset='training'
)

val_gen = datagen.flow_from_directory(
            data_dir,
            target_size = TARGET_SIZE,
            batch_size = 500,
            color_mode = 'rgb',
            class_mode = 'categorical',
            shuffle = False,
            seed = 155,
            subset='validation'
)

model = keras.models.load_model('C:\\DATA-FAST\\brick-class\\Models\\brick-class-cnn-9296.hdf5')

print('Predicting')
pred = model.predict_generator(val_gen,40000)#[0]
incorrect_files = []
print('Selecting')
for index,p in enumerate(pred):
    #print(np.amax(p))

    if (val_gen.filenames[index].split('\\')[0] != list(train_gen.class_indices)[np.where(p==np.amax(p))[0][0]]):

        incorrect_files.append(data_dir+'\\'+val_gen.filenames[index])
    
        #print(val_gen.filenames[index],list(train_gen.class_indices)[np.where(p==np.amax(p))[0][0]],np.amax(p))
        #s=input('..')
print('Graphing')
rows = 10
shuffle(incorrect_files)
for index,file in enumerate(incorrect_files[:100]):
    img = Image.open(file)
    plt.subplot(rows,10,index+1)
    plt.axis('off')
    plt.imshow(img)
plt.show()