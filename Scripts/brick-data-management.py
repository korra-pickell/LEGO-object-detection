import os
from collections import Counter

blocks_file = open('E:/Documents/PRGM/NEURAL/Blocks/parts-popular.txt','r')
#render_directory = 'E:/DATA/blocks/rendered_images'
render_directory = 'E:/DATA/blocks/B100'

def gen_used_classes_file():

    renders = [render_directory+'/'+item for item in os.listdir(render_directory)]
    class_names = list(set([path.split('/')[-1].split('_')[0] for path in renders]))

    output_dir = 'E:/Documents/PRGM/NEURAL/Blocks'

    file = open(output_dir+'/classes.txt','w')
    for c in class_names:
        file.write(c+'\n')
    file.close()

gen_used_classes_file()

def repair_blocks():
    
    blocks = [b.replace('\n','') for b in blocks_file.readlines()]

    expected_intances = 25

    renders = [render_directory+'/'+item for item in os.listdir(render_directory)]

    need_repair = []
    render_block_names = [path.split('/')[-1].split('_')[0] for path in renders]

    count = Counter(render_block_names)

    for block in blocks:

        if (count[str(block)] != expected_intances and count[str(block)] > 0):
            need_repair.append([block,count[str(block)]])

    print('NEED REPAIR:')

    for block in need_repair:
        print(block[1],block[0])