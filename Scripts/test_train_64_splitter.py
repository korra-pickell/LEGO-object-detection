import os

data_dir = r'E:\DATA\Blocks-2\classification\64'

target_dir = r'E:\DATA\Blocks-2\classification\64v1.0'

file_dirs = [os.path.join(data_dir,file) for file in os.listdir(data_dir)]

print(file_dirs)