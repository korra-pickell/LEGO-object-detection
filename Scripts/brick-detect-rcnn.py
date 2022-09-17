# fit a mask rcnn on the brick dataset
from os import listdir
import os
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
import sys
import random
import tensorflow as tf


def gpu_mem_allocate():
    print('MEM CONFIG ++++++++++++++++++++++++++++++++++')
    config = tf.compat.v1.ConfigProto()
    from tensorflow.python.keras.backend import set_session
    #config.gpu_options.per_process_gpu_memory_fraction = 0.9
    config.gpu_options.allow_growth = True
    set_session(tf.compat.v1.Session(config=config))

gpu_mem_allocate()

'''
import tensorflow as tf
print (tf.test.gpu_device_name())

def gpu_mem_allocate():
    print('MEM CONFIG ++++++++++++++++++++++++++++++++++')
    config = tf.compat.v1.ConfigProto()
    from tensorflow.python.keras.backend import set_session
    #config.gpu_options.per_process_gpu_memory_fraction = 0.9
    config.gpu_options.allow_growth = True
    set_session(tf.compat.v1.Session(config=config))

gpu_mem_allocate()'''

ROOT_DIR = os.path.abspath("E:\\Documents\\PRGM\\NEURAL\\Blocks\\MRCNN\\Mask_RCNN-master")
sys.path.append(ROOT_DIR)

class_file = open('E:/Documents/PRGM/NEURAL/Blocks/classes.txt')
classes = [line.replace('\n','') for line in class_file.readlines()]


from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log
 
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


# class that defines and loads the brick dataset
class brickDataset(utils.Dataset):
	# load the dataset definitions
	def load_dataset(self, dataset_dir, is_train=True):
		# define classes
		
		self.add_class('dataset',1,'brick')

		#for index,c in enumerate(classes):
		#	self.add_class('dataset', index+1, c)
		
		#self.add_class("dataset", 1, "3002")

		items = [int(name[:-4]) for name in os.listdir('E:\\DATA\\blocks\\training_data\\annots')][:10000]
		items.sort()
		#print(items)

		#stop = input('....')
		val_count = 50
        
		if (is_train == True):
			for index in items[:-val_count]:
				self.add_image('dataset', image_id=1, path='E:\\DATA\\blocks\\training_data\\imgs\\'+str(index)+'.jpg',
				annotation='E:\\DATA\\blocks\\training_data\\annots\\'+str(index)+'.xml')
		else:
			for index in items[-val_count:]:
				self.add_image('dataset', image_id=1, path='E:\\DATA\\blocks\\training_data\\imgs\\'+str(index)+'.jpg',
				annotation='E:\\DATA\\blocks\\training_data\\annots\\'+str(index)+'.xml')
 
	# extract bounding boxes from an annotation file
	def extract_boxes(self, filename):
		# load and parse the file
		tree = ElementTree.parse(filename)
		# get the root of the document
		root = tree.getroot()
		# extract each bounding box
		objects = list()
		for object in root.findall('.//object'):
			name = object.find('name').text
			box = object.find('bndbox')
			xmin = int(box.find('xmin').text)
			ymin = int(box.find('ymin').text)
			xmax = int(box.find('xmax').text)
			ymax = int(box.find('ymax').text)
			
			coors = [xmin, ymin, xmax, ymax, name]
			#coors = [xmin, ymin, xmax, ymax]
			#print(coors)
			#s = input('....')
			objects.append(coors)
		# extract image dimensions
		width = int(root.find('.//size/width').text)
		height = int(root.find('.//size/height').text)
		return objects, width, height
 
	# load the masks for an image
	def load_mask(self, image_id):
		# get details of image
		info = self.image_info[image_id]
		# define box file location
		path = info['annotation']
		# load XML
		boxes, w, h = self.extract_boxes(path)
		# create one array for all masks, each on a different channel
		masks = zeros([h, w, len(boxes)], dtype='uint8')
		# create masks
		class_ids = list()
		for i in range(len(boxes)):
			box = boxes[i]
			row_s, row_e = box[1], box[3]
			col_s, col_e = box[0], box[2]
			masks[row_s:row_e, col_s:col_e, i] = 1
			#class_ids.append(self.class_names.index(box[4]))
			class_ids.append(self.class_names.index('brick'))
		return masks, asarray(class_ids, dtype='int32')
 
	# load an image reference
	def image_reference(self, image_id):
		info = self.image_info[image_id]
		return info['path']
 
# define a configuration for the model
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

# prepare train set
train_set = brickDataset()
train_set.load_dataset('brick', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = brickDataset()
test_set.load_dataset('brick', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))
# prepare config
config = brickConfig()
config.display()

# define the model
model = modellib.MaskRCNN(mode="training", config=config,
                          model_dir='E:\\Documents\\PRGM\\NEURAL\\Blocks\\MRCNN\\Builds\\logs')

# Which weights to start with?
init_with = "coco"  # imagenet, coco, or last

if init_with == "imagenet":
    model.load_weights(model.get_imagenet_weights(), by_name=True)
elif init_with == "coco":
    # Load weights trained on MS COCO, but skip layers that
    # are different due to the different number of classes
    # See README for instructions to download the COCO weights
    model.load_weights(COCO_MODEL_PATH, by_name=True,
                       exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", 
                                "mrcnn_bbox", "mrcnn_mask"])
elif init_with == "last":
    # Load the last model you trained and continue training
    model.load_weights(model.find_last(), by_name=True)

model.train(train_set, test_set, 
            learning_rate=config.LEARNING_RATE, 
            epochs=10, 
            layers='heads')

model.train(train_set, test_set, 
            learning_rate=config.LEARNING_RATE / 10, 
            epochs=20, 
            layers='heads')

model.train(train_set, test_set, 
            learning_rate=config.LEARNING_RATE / 10,
            epochs=30, 
            layers="all")

