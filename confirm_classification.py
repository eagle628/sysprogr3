#!python3.6.6
import random
import numpy as np
import chainer
import matplotlib.pyplot as plt
from chainer import iterators
import chainer.links as L
import chainer.functions as F
from chainer import optimizers
from chainer import training
from chainer import serializers
from chainercv import transforms
from chainer.training import extensions
from chainer.cuda import to_cpu
from functools import partial
from chainer.datasets import TransformDataset

from mymodule import create_dataset
from mymodule import network_composition


def transform(inputs, train=True):
    img, label = inputs
    img = img.copy()

    # Standardization
    img -= mean[:, None, None]
    img /= std[:, None, None]

    # Random flip & crop

    if train:
        img = img.transpose(0, 2, 1)
        img = img.resize((1280, 720), Image.ANTIALIAS)

    return img, label


infer_net = network_composition.DeepCNN(3)
serializers.load_npz(
    'DeepCNN_HonkanEntrance3_result/snapshot_epoch-100',
    infer_net, path='updater/model:main/predictor/')

gpu_id = 0
if gpu_id >= 0:
    infer_net.to_gpu(gpu_id)

dir_root = r'C:\Users\NaoyaInoue\Desktop\syspro_gr3\test_honkan'
img_root1 = r'0'
img_root2 = r'1'
img_root3 = r'2'
img_root = [img_root1, img_root2, img_root3]
data = create_dataset.create_data_set(dir_root, img_root, [0,1,2], 1)
#data = TransformDataset(data, partial(transform, train=True))
print(data[0][0].shape)
print(len(data))
