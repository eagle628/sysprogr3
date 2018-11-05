#!python3.6.6
import numpy as np
import chainer
import os
import re
import random

def search_img_name(image_root):
    data_number = 0
    image_name = []
    files = os.listdir(image_root)
    for file in files:
        index = re.search('.jpg', file)# 拡張子が，jpgのものを検出
        if index:
            data_number += 1
            image_name.append(file)
    return data_number, image_name

def create_data_set(image_roots,labels,N):
    img_data = []
    label_data = []
    for (image_root,label) in zip(image_roots,labels):
        (data_number, img_data) = search_img_name(image_root)
        if N < data_number:
            img_data.extend(random.sample(img_data, k=N))
            data_number = N
        label_data.extend([label for i in range(data_number)])
    dataset = chainer.datasets.LabeledImageDataset(list(zip(img_data,label_data)),root=image_root)
    return dataset
