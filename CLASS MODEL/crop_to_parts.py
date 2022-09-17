from genericpath import isfile
from PIL import Image
import os, random, ast
from progress.bar import Bar

full_img_height, full_img_width = 2048, 2048
output_img_size = 64

num_of_files = 2000

metadata_dir = 'E:\\DATA\\Blocks-2\\DataGen\\Metadata\\'
render_dir = 'E:\\DATA\\Blocks-2\\DataGen\\Renders\\'
bgd_dir = 'C:\\Users\\16363\\Desktop\\bgds\\'

output_dir = 'E:\\DATA\\Blocks-2\\classification\\'

bgds = [bgd_dir + filename for filename in os.listdir(bgd_dir)]

bgd_cnt = 0

def get_current_save_num(size,name):
    dir = output_dir+str(output_img_size)+'\\'+name
    if (os.path.isdir(dir)):
        return str(len(os.listdir(dir))+1)
    else:
        return str(0)

bar = Bar('Processing ', max = num_of_files, suffix = '%(percent).1f%% - %(eta)ds')

for index in range(0,num_of_files):

    metadata_file = open(metadata_dir+str(index)+'.txt','r')
    objects = metadata_file.readlines()[1:]

    render_img = Image.open(render_dir+str(index)+'.png')

    bgd_img = Image.open(bgds[int(bgd_cnt%len(bgds))]).resize((2048,2048)) #.crop((0,0,full_img_width,full_img_height))
    bgd_cnt += 1

    bgd_img.paste(render_img,box=None,mask=render_img)

    for obj in objects:
        obj = ast.literal_eval(obj)
        cropped_img = bgd_img.crop((obj[1][0],obj[1][1],obj[1][0]+obj[1][2],obj[1][1]+obj[1][3]))
        save_path = output_dir+str(output_img_size)+'\\'+obj[0]+'\\'+get_current_save_num(output_img_size,obj[0])+'.jpg'

        if (os.path.isdir(output_dir+str(output_img_size)+'\\'+obj[0])):
            cropped_img.resize((output_img_size,output_img_size)).save(save_path)
        else:
            os.makedirs(output_dir+str(output_img_size)+'\\'+obj[0])
            cropped_img.resize((output_img_size,output_img_size)).save(save_path)
    bar.next()
bar.finish()

print('>> PROCESSING COMPLETE ')
