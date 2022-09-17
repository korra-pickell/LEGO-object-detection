import numpy as np
import os, time
from PIL import Image
from progress.bar import Bar

data_dir = 'C:\\DATA-FAST\\brick-class\\64\\'

output_dir = 'C:\\DATA-FAST\\NPY\\brick\\class\\64'

classes = os.listdir(data_dir)

cutoff = 4000

IMG_SIZE = 32
IMG_DEPTH = 3

def prepare():
    x_data,y_data = [],[]
    
    for index,class_name in enumerate(classes):
        bar = Bar('Processing ',max=cutoff,suffix = '%(percent).1f%% - %(eta)ds')
        print(index,class_name)
        files = [data_dir+'\\'+class_name+'\\'+file for file in os.listdir(data_dir+'\\'+class_name+'\\')]
        for file in files[:cutoff]:
            if (IMG_DEPTH == 3):
                im = Image.open(file).resize((IMG_SIZE,IMG_SIZE))
            else:
                im = Image.open(file).convert('L').resize((IMG_SIZE,IMG_SIZE))
            im_arr = np.array(im) / 255.0
            im_class_encoded = [0 for i in range(len(classes))]
            im_class_encoded[classes.index(class_name)] = 1
            x_data.append(np.array(im_arr).reshape(IMG_SIZE,IMG_SIZE,IMG_DEPTH))
            y_data.append(np.array(im_class_encoded))
            bar.next()
        bar.finish()
    np.savez(output_dir+'\\brick-32-rgb.npz',x=x_data,y=y_data)
    

prepare()