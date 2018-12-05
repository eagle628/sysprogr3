# -*- coding: utf-8 -*-
#!python2.7
import os
import datetime

import preprocess


data_dir = 'original_data/'

now_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
os.makedirs(now_str)


# convert videodata to image sequence

label_list = os.listdir(data_dir)
for label in label_list:
    label_dir = os.path.join(data_dir,label)
    video_list = os.listdir(label_dir)
    for video in video_list:
        video_path = os.path.join(data_dir,label,video)
        save_path = os.path.join(now_str,'labeled_images',label)
        preprocess.video2frames(video_file=video_path,image_dir=save_path)


preprocess.show_blur_hist('2018_12_04_16_15_02')
preprocess.blur_filtering('2018_12_04_18_47_56',threshold = 20)
preprocess.img_selection('2018_12_04_18_47_56', decimate_rate = 0, crop_number = 3, crop_size = 1000, resize_scale = 1)
