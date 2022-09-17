import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ast
from PIL import Image

file = open('E:\\DATA\\Blocks-2\\DataGen\\annotations\\14.txt')

bboxes = [ast.literal_eval(line.replace('\n',''))[1] for line in file.readlines()[1:]]

im = Image.open('C:\\Users\\16363\\Desktop\\demo_OD.png')

fig, ax = plt.subplots()

ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])

ax.imshow(im)

save_img = 'C:\\Users\\16363\\Desktop\\demo_OD_1.png'

for bbox in bboxes:
    rect = patches.Rectangle((bbox[0],bbox[1]),bbox[2],bbox[3],linewidth=0.5,edgecolor='black',facecolor='none')
    ax.add_patch(rect)

plt.savefig(save_img, dpi=600)