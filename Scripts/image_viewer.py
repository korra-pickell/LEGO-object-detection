from PIL import Image, ImageFilter
import os
import numpy as np
import matplotlib.pyplot as plt

data_dir = 'C:\\DATA-FAST\\brick-class\\64\\'


classes = os.listdir(data_dir)


f,axs = plt.subplots(10,20)

plt.tick_params(left=False,
                bottom=False,
                labelleft=False,
                labelbottom=False)

for ax,c in zip(axs.reshape(-1),classes):
    c_image = Image.open(data_dir+'\\'+str(c)+'\\0.jpg').convert('L').resize((32,32))
    #c_image = c_image.filter(ImageFilter.FIND_EDGES)
    c_arr = np.array(c_image)
    ax.imshow(c_arr,cmap='gray',vmin=0, vmax=255)
    ax.set_xticks([])
    ax.set_yticks([])

plt.show()
