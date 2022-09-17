from os import listdir
import os
from xml.etree import ElementTree
from matplotlib.patches import Rectangle
from numpy import zeros
from numpy import asarray
import sys
import random
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import matplotlib
import math

ROOT_DIR = os.path.abspath("E:\\Documents\\PRGM\\NEURAL\\Blocks\\MRCNN\\Mask_RCNN-master")
sys.path.append(ROOT_DIR)

class_file = open('E:/Documents/PRGM/NEURAL/Blocks/classes.txt')
classes = [line.replace('\n','') for line in class_file.readlines()]


from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log
from mrcnn.model import mold_image

def last_model(log_dir):
	files = []
	for root, dirnames, filenames in os.walk(log_dir):
		for file in filenames:
			if ('h5' in file):
				files.append(os.path.join(root,file))
	files.sort(key=os.path.getmtime)
	return files[-1]

COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class brickConfig(Config):
	# define the name of the configuration

	NAME = "brick_cfg"
	BACKBONE = 'resnet50'
	
	NUM_CLASSES = 2  #+ len(classes)
	IMAGES_PER_GPU = 1

	#DETECTION_MIN_CONFIDENCE = 0.85
	LEARNING_RATE = 0.001

	#TRAIN_ROIS_PER_IMAGE = 10

	VALIDATION_STEPS = 10

	IMAGE_MAX_DIM = 1024

	STEPS_PER_EPOCH = 300

config = brickConfig()
config.display()

model = modellib.MaskRCNN(mode="training", config=config,
                          model_dir='E:\\Documents\\PRGM\\NEURAL\\Blocks\\MRCNN\\Builds\\logs')

init_with = "coco"

if init_with == "imagenet":
    model.load_weights(model.get_imagenet_weights(), by_name=True)
elif init_with == "coco":
    model.load_weights(COCO_MODEL_PATH, by_name=True,
                       exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", 
                                "mrcnn_bbox", "mrcnn_mask"])

elif init_with == "last":
    model.load_weights(model.find_last(), by_name=True)

class InferenceConfig(brickConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 2  #+ len(classes)
    #DETECTION_MAX_INSTANCES = 1
    DETECTION_MIN_CONFIDENCE = 0.7
    IMAGE_MAX_DIM = 1024
    

inference_config = InferenceConfig()

model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=COCO_MODEL_PATH)

logs = 'E:\\Documents\\PRGM\\NEURAL\\Blocks\\MRCNN\\Builds\\logs'

model_path = last_model(logs)

print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)

test_img_dir = 'E:\\DATA\\blocks\\training_data\\test_imgs'

test_imgs = [os.path.join(test_img_dir,filename) for filename in os.listdir(test_img_dir)]

plot_side_length = 2
fig,axs = plt.subplots(plot_side_length,plot_side_length)
#plt.axis('off')
for index,image_path in enumerate(test_imgs):
    image = Image.open(image_path)
    image_array = np.array(image)
    scaled_image = image_array.astype(np.float32) - inference_config.MEAN_PIXEL
    sample = np.expand_dims(scaled_image,0)
    print('PRED ',index+1)
    
    results = model.detect(sample)[0]

    #print(results)
    #s = input('...')

    pred = results['rois']
    class_ids = results['class_ids']
    scores = results['scores']

    axs[int(math.floor(index%plot_side_length)),int(math.floor(index/plot_side_length))].imshow(image_array)
    axs[int(math.floor(index%plot_side_length)),int(math.floor(index/plot_side_length))].axis('off')
    for b,box in enumerate(pred):
        y1, x1, y2, x2 = box
        width, height = x2 - x1, y2 - y1
        axs[int(math.floor(index%plot_side_length)),int(math.floor(index/plot_side_length))].add_patch(matplotlib.patches.Rectangle((x1,y1),width,height,fill=False,color='red'))
        axs[int(math.floor(index%plot_side_length)),int(math.floor(index/plot_side_length))].text(x1,y1+15,str(class_ids[b])+' : '+str(round(scores[b],2)),fontsize=6)
plt.show()

