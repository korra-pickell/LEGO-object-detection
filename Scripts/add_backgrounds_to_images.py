from PIL import Image
import numpy as np
import os, random

img_dir = 'E:\\DATA\\Blocks-2\\DataGen\\images'

bgd_img_dir = 'E:\\DATA\\Blocks-2\\DataGen\\background_imgs\\background_imgs'

out_dir = 'E:\\DATA\\Blocks-2\\DataGen\\images_with_backgrounds'

img_paths = [[os.path.join(img_dir,path),path] for path in os.listdir(img_dir)]
bgd_img_paths = [os.path.join(bgd_img_dir,path) for path in os.listdir(bgd_img_dir)]

IMG_DIM = 2048

for index,img_path in enumerate(img_paths):
    img = Image.open(img_path[0])
    bgd_img = Image.open(random.choice(bgd_img_paths)).resize((IMG_DIM,IMG_DIM)).rotate(random.choice([0,90,180,270]))

    bgd_img.paste(img,(0,0),img)
    
    bgd_img.save(os.path.join(out_dir,img_path[1]))

    print(index / len(img_paths))