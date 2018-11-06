#!python3.6.6
from mymodule import generate_image

root = r'C:\Users\NaoyaInoue\Desktop\label2'
video_file = '002.MOV'

generate_image.video2frames(root=root, video_file=video_file)
