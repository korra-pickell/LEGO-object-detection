from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import  Dense, Input, Dropout, GlobalAveragePooling2D
from keras import applications

import time

#data_dir = 'path/to/your/data'

val_split = 0.1
TARGET_SIZE = (75,75)
INPUT_SHAPE = (75,75,3)
BATCH_SIZE = 256
EPOCHS = 10

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
            seed = 160,
            subset='training'
)

val_gen = datagen.flow_from_directory(
            data_dir,
            target_size = TARGET_SIZE,
            batch_size = BATCH_SIZE,
            color_mode = 'rgb',
            class_mode = 'categorical',
            shuffle = True,
            seed = 160,
            subset='validation'
)

class_count = len(train_gen.class_indices)

def get_model():

    base_model = applications.InceptionResNetV2(weights='imagenet',
                include_top=False,
                input_shape=INPUT_SHAPE)
    base_model.trainable = True

    model = Sequential()
    model.add(base_model)
    model.add(GlobalAveragePooling2D())
    model.add(Dropout(0.6))
    model.add(Dense(class_count, 
                        activation='softmax'))

    return model

model = get_model()

model.compile(loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])

model.summary()
'''
log_dir = 'path/to/model/progress/data'+str(time.time())
save_dir = 'path/to/saved/models'

tensorboard_callback = TensorBoard(log_dir=log_dir,
                            histogram_freq=1)
save_callback = ModelCheckpoint(save_dir,
                            monitor='accuracy',
                            verbose=1,
                            save_best_only=True,
                            mode='auto',
                            period=1)
'''
history = model.fit_generator(generator=train_gen,
                            validation_data=val_gen,
                            epochs=EPOCHS,
                            shuffle=True,
                            verbose=True)
                            #callbacks=[tensorboard_callback,save_callback])

#log_dir = 'C:\\DATA-FAST\\brick-class\\Models\\Classifier\\logs\\'+str(time.time())
#tensorboard_callback = TensorBoard(log_dir=log_dir,histogram_freq=1)
#save_callback = ModelCheckpoint('C:\\DATA-FAST\\brick-class\\Models\\Classifier\\logs\\models\\brick-class-cnn.hdf5',monitor='accuracy',verbose=1,save_best_only=True,mode='auto',period=1)

