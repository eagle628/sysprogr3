import cv2
import os
from imutils import paths
import random
import logging

import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import serializers
from chainer.cuda import to_cpu

import logging

# preprocess  fucntion
def preprocess(root_path, image_name, decimate_rate = 0, crop_number = 3, crop_size = 1000, resize_scale = 1, extension='.jpg'):
    preprocessed_image_name = []
    if random.random() >= decimate_rate :
        image = cv2.imread(os.path.join(root_path,image_name))
        logging.debug(image_name)
        logging.debug(image.shape)
        if image.shape[0] < image.shape[1]:
            image = image.transpose(1,0,2)
        logging.debug(image.shape)
        for i in range(crop_number) :
            x = random.randint(0, 1920 - crop_size)
            y = random.randint(0, 1080 - crop_size)
            cropped_image = image[x:x+crop_size,y:y+crop_size]
            logging.debug(cropped_image.shape)
            resized_image = cv2.resize(cropped_image,(int(round(cropped_image.shape[1]/resize_scale)),int(round(cropped_image.shape[0]/resize_scale))))

            preprocessed_image_name.append(os.path.join(root_path, os.path.splitext(image_name)[0]) + '_' +str(i) + extension)
            cv2.imwrite(preprocessed_image_name[-1], resized_image)
            logging.debug('---------------**WRITE IMAGE**---------------')

    return preprocessed_image_name

def est_locale(image_path, gpu_id=-1):
    net = DeepCNN(3)
    net = L.Classifier(net)
    #net = MLP()
    chainer.serializers.load_npz(
        os.path.join(os.path.dirname(__file__),'ML_model/snapshot_epoch-20'),
        net, path='updater/model:main/')
    if gpu_id >= 0:
        net.to_gpu(gpu_id)
    logging.debug('Start ML Processing')
    dataset = chainer.datasets.ImageDataset([image_path])
    dataset = dataset[0]
    net.to_cpu()
    with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
        result = net.predictor(dataset[None, ...]).data
    #result = to_cpu(result.array)
    result = chainer.functions.softmax(result)
    result = result.data
    result = result[0].tobytes()
    logging.debug('End ML Processing')
    return result

# network definition
class MLP(chainer.Chain):

    def __init__(self, n_mid_units=100, n_out=10):
        super(MLP, self).__init__()

        with self.init_scope():
            self.l1 = L.Linear(None, n_mid_units)
            self.l2 = L.Linear(n_mid_units, n_mid_units)
            self.l3 = L.Linear(n_mid_units, n_out)

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)

class DeepCNN(chainer.ChainList):

    def __init__(self, n_output):
        super(DeepCNN, self).__init__(
            ConvBlock(128),
            ConvBlock(128, True),
            ConvBlock(256),
            ConvBlock(256, True),
            LinearBlock(),
            LinearBlock(),
            L.Linear(None, n_output)
        )

    def __call__(self, x):
        for f in self:
            x = f(x)
        return x

class ConvBlock(chainer.Chain):

    def __init__(self, n_ch, pool_drop=False):
        w = chainer.initializers.HeNormal()
        super(ConvBlock, self).__init__()
        with self.init_scope():
            self.conv = L.Convolution2D(None, n_ch, 3, 3, 1, nobias=True, initialW=w)
            self.bn = L.BatchNormalization(n_ch)
        self.pool_drop = pool_drop

    def __call__(self, x):
        h = F.relu(self.bn(self.conv(x)))
        if self.pool_drop:
            h = F.max_pooling_2d(h, 2, 2)
            h = F.dropout(h, ratio=0.25)
        return h

class LinearBlock(chainer.Chain):

    def __init__(self, drop=False):
        w = chainer.initializers.HeNormal()
        super(LinearBlock, self).__init__()
        with self.init_scope():
            self.fc = L.Linear(None, 1024, initialW=w)
        self.drop = drop

    def __call__(self, x):
        h = F.relu(self.fc(x))
        if self.drop:
            h = F.dropout(h)
        return h
