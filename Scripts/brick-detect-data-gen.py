from PIL import Image, ImageEnhance
import numpy as np
import os, random, math, cv2
import xml.etree.ElementTree as ET
from xml.dom import minidom

from create_label import annotation

from scattered_block_image_gen import canvas_build

####### CONFIG ######### CONFIG ######### CONFIG ###############

#block_img_folder = 'E:/DATA/blocks/rendered_images'
#block_img_folder = 'E:/DATA/blocks/3002'
block_img_folder = 'E:/DATA/blocks/B100'
bgd_img_folder = 'E:/DATA/blocks/bgds'

img_out = 'E:/DATA/blocks/training_data/imgs'
ann_out = 'E:/DATA/blocks/training_data/annots'

NUMBER_OF_IMGS = 50000

NUMBER_OF_SAMPLES_PER_IMG = 50
NUMBER_OF_ATTEMPS_PER_SAMPLE = 10
CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 1024
CANVAS_DEPTH = 3
BRICK_MIN_SCALE = 0.3
BRICK_MAX_SCALE = 0.7
START_INDEX = 0

################################################################

def create_data(block_folder,bgd_folder,output_img,output_annot):
    for render_index in range(NUMBER_OF_IMGS):

        render_path = output_img+'/'+str(render_index+START_INDEX)+'.jpg'
        annot_path = output_annot+'/'+str(render_index+START_INDEX)+'.xml'

        render,objects = canvas_build.create_canvas_image(bgd_paths=bgd_folder,
                            imgs_paths=block_img_folder,
                            number_of_samples=NUMBER_OF_SAMPLES_PER_IMG,
                            number_of_attempts=NUMBER_OF_ATTEMPS_PER_SAMPLE,
                            canvas_width=CANVAS_WIDTH,
                            canvas_height=CANVAS_HEIGHT,
                            brick_min_scale=BRICK_MIN_SCALE,
                            brick_max_scale=BRICK_MAX_SCALE)

        ann = annotation()
        ann.meta_init(folder='None',filename=str(render_index+START_INDEX)+'.jpg',path=render_path,size=(CANVAS_WIDTH,CANVAS_HEIGHT,CANVAS_DEPTH))

        for object in objects:
            ann.add_object(name = object[0], bndbox = object[1])

        ann.objects_to_file(annot_path,file_index=render_index+START_INDEX)

        Image.fromarray(np.array(render)).save(render_path)

create_data(block_img_folder,bgd_img_folder,img_out,ann_out)