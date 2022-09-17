from create_label import annotation
import os, ast

text_dir = 'E:\\DATA\\Blocks-2\\DataGen\\annotations'
output_dir = 'E:\\DATA\\Blocks-2\\DataGen\\ann\\annotations'

text_files = [text_dir+'\\'+filename for filename in os.listdir(text_dir)]

for index,file in enumerate(text_files):

    file = open(file,'r')
    text = file.readlines()

    ann = annotation()
    ann.meta_init(folder='None',filename=str(index),path='None',size=(2048,2048,3),lighting=text[0])

    for obj in text[1:]:
        data = ast.literal_eval(obj)
        ann.add_object(name = data[0], bndbox = (data[1][0],data[1][1],data[1][0]+data[1][2],data[1][1]+data[1][3]),pose=data[2])

    ann.objects_to_file(output_dir+'\\'+str(index)+'.xml',file_index=index)


