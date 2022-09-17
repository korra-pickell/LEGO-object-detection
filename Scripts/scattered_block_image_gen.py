from PIL import Image, ImageEnhance
import numpy as np
import os, random, math, cv2

class canvas_build:
    def crop_to_bbox(img):
        bbox = img.getbbox()
        cropped_img = img.crop(bbox)
        return cropped_img

    def overlap_check(img1,img2):

        img1_arr = np.array(img1)
        img2_arr = np.array(img2)

        img1_arr[img1_arr > 0] = 1
        img1_arr[img1_arr == 0] = 3

        img2_arr[img2_arr > 0] = 1
        img2_arr[img2_arr == 0] = 0

        intersect_bool = (img1_arr==img2_arr).any()

        return intersect_bool

    def load_image_paths(folder_path):
        files = [folder_path+'/'+file for file in os.listdir(folder_path)]
        return files

    def create_canvas_image(bgd_paths,imgs_paths,number_of_samples,number_of_attempts,canvas_width,canvas_height,brick_min_scale,brick_max_scale,shadows):

        imgs_paths = canvas_build.load_image_paths(imgs_paths)
        bgd_paths = canvas_build.load_image_paths(bgd_paths)

        canvas_objects = []

        bgd = random.choice(bgd_paths)

        bgd = Image.open(bgd)

        rand_rotate = random.choice((0,90,180,270,-90))

        bgd = bgd.resize((canvas_width,canvas_height))

        bgd = bgd.rotate(rand_rotate)

        canvas = Image.new('RGBA',(canvas_width,canvas_height),(0,0,0,0))

        for obj in range(number_of_samples):

            rand_img_path = random.choice(imgs_paths)
            img_id = rand_img_path.split('/')[-1].split('_')[0]

            rand_img_scale = random.choice([((brick_max_scale-brick_min_scale)/10)*s+brick_min_scale for s in range(1,10)])
            img = canvas_build.crop_to_bbox(Image.open(rand_img_path))
            img = img.resize((math.ceil(img.size[0]*rand_img_scale),math.ceil(img.size[1]*rand_img_scale)))

            brightness_factor = random.uniform(0.4,3.5)

            enhancer = ImageEnhance.Brightness(img)

            img = enhancer.enhance(brightness_factor)

            for attempt in range(number_of_attempts):

                rand_x,rand_y = random.randint(0,canvas_width-img.width-1),random.randint(0,canvas_height-img.height-1)

                canvas_selected_region = canvas.crop((rand_x,rand_y,rand_x+img.width,rand_y+img.height))

                overlap = canvas_build.overlap_check(img,canvas_selected_region)

                if (overlap == False):


                    canvas.paste(img,(rand_x,rand_y),img)
                    
                    canvas_objects.append([img_id,[rand_x,rand_y,rand_x+img.width,rand_y+img.height]])

                    break
        
        if (shadows==True):
            shadow_canvas = canvas
            shad_enhancer = ImageEnhance.Brightness(shadow_canvas)
            shadow_canvas = shad_enhancer.enhance(0)

            #shadow_canvas.show()

            shadow_shift_x = int((random.randint(0,10)/100)*CANVAS_WIDTH)
            shadow_shift_y = int((random.randint(0,10)/100)*CANVAS_HEIGHT)
            shadow_harshness = random.uniform(0,1)

            shadow_canvas.putalpha(shadow_harshness)
            #print(shadow_canvas)
            #print(shadow_shift_x,shadow_shift_y)
            bgd.paste(shadow_canvas,box=(shadow_shift_x,shadow_shift_y),mask=shadow_canvas)

        bgd.show()
        s = input('...')
        
        bgd.paste(canvas,canvas)
        bgd = bgd.convert('L')

        bgd.show()

        s = input('...')
        #stacked = np.stack((bgd,)*3,axis=-1)

        #return bgd,canvas_objects

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
SHADOWS = True

canvas_build.create_canvas_image(bgd_paths=bgd_img_folder,
                            imgs_paths=block_img_folder,
                            number_of_samples=NUMBER_OF_SAMPLES_PER_IMG,
                            number_of_attempts=NUMBER_OF_ATTEMPS_PER_SAMPLE,
                            canvas_width=CANVAS_WIDTH,
                            canvas_height=CANVAS_HEIGHT,
                            brick_min_scale=BRICK_MIN_SCALE,
                            brick_max_scale=BRICK_MAX_SCALE,
                            shadows=True)