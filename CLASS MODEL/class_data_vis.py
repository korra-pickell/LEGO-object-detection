import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

brick_num = 3660

imgs = ['E:\\DATA\\Blocks-2\\classification\\64\\'+str(brick_num)+'\\'+filename for filename in os.listdir('E:\\DATA\\Blocks-2\\classification\\64\\'+str(brick_num))][:100]
img_index = 0

f, axarr = plt.subplots(10,10)

f.suptitle('BRICK ID: ' + str(brick_num),fontsize=20)
plt.subplots_adjust(hspace=0.05,wspace=0.05)

for x in range(10):
    for y in range(10):
        axarr[x,y].imshow(Image.open(imgs[img_index]))
        axarr[x,y].axis('off')
        img_index += 1
plt.savefig('E:\\DATA\\Blocks-2\\classification\\Demos\\'+str(brick_num)+'.jpg', dpi=150)