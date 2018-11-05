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
from chainer.training import extensions
from chainer.cuda import to_cpu
from functools import partial
from chainercv import transforms
from chainer.datasets import TransformDataset

from mymodule import create_dataset

#############################################################
def reset_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    if chainer.cuda.available:
        chainer.cuda.cupy.random.seed(seed)

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

class MyNet(chainer.Chain):

    def __init__(self, n_out):
        super(MyNet, self).__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(None, 32, 3, 1, 1)
            self.conv2 = L.Convolution2D(32, 64, 3, 1, 1)
            self.conv3 = L.Convolution2D(64, 128, 3, 1, 1)
            self.fc4 = L.Linear(None, 1000)
            self.fc5 = L.Linear(1000, n_out)

    def __call__(self, x):
        h = F.relu(self.conv1(x))
        h = F.relu(self.conv2(h))
        h = F.relu(self.conv3(h))
        h = F.relu(self.fc4(h))
        h = self.fc5(h)
        return h

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

def train(network_object, dataset, batchsize=128, gpu_id=0, max_epoch=20, postfix='', base_lr=0.01, lr_decay=None):

    # prepare dataset
    train_size = int(len(dataset) * 0.9)
    train_val, test = chainer.datasets.split_dataset_random(Honkan_dataset, train_size, seed=0)
    train_size = int(len(train_val) * 0.9)
    train, valid = chainer.datasets.split_dataset_random(train_val, train_size, seed=0)

    # data augement
    train_dataset = TransformDataset(train, partial(transform, train=True))
    valid_dataset = TransformDataset(valid, partial(transform, train=False))
    test_dataset = TransformDataset(test, partial(transform, train=False))

    # 2. Iterator
    train_iter = iterators.SerialIterator(train, batchsize)
    #train_iter = iterators.MultiprocessIterator(train, batchsize)
    valid_iter = iterators.SerialIterator(valid, batchsize, False, False)
    #valid_iter = iterators.MultiprocessIterator(valid, batchsize, False, False)

    # 3. Model
    net = L.Classifier(network_object)

    # 4. Optimizer
    optimizer = optimizers.MomentumSGD(lr=base_lr).setup(net)
    #optimizer = optimizers.Adam().setup(net)
    optimizer.add_hook(chainer.optimizer.WeightDecay(0.0005))

    # 5. Updater
    updater = training.StandardUpdater(train_iter, optimizer, device=gpu_id)

    # 6. Trainer
    trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='{}_HonkanEntrance3_{}result'.format(network_object.__class__.__name__, postfix))

    # 7. Trainer extensions
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.observe_lr())
    trainer.extend(extensions.Evaluator(valid_iter, net, device=gpu_id), name='val')
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'val/main/loss', 'val/main/accuracy', 'elapsed_time', 'lr']))
    trainer.extend(extensions.PlotReport(['main/loss', 'val/main/loss'], x_key='epoch', file_name='loss.png'))
    trainer.extend(extensions.PlotReport(['main/accuracy', 'val/main/accuracy'], x_key='epoch', file_name='accuracy.png'))
    trainer.extend(extensions.ProgressBar())
    if lr_decay is not None:
        trainer.extend(extensions.ExponentialShift('lr', 0.1), trigger=lr_decay)
    trainer.run()
    del trainer

    # 8. Evaluation
    test_iter = iterators.SerialIterator(test, batchsize, False, False)
    #test_iter = iterators.MultiprocessIterator(test, batchsize, False, False)
    test_evaluator = extensions.Evaluator(test_iter, net, device=gpu_id)
    results = test_evaluator()
    print('Test accuracy:', results['main/accuracy'])

    return net

def transform(inputs, train=True):
    img, label = inputs
    img = img.copy()

    # Standardization
    img -= mean[:, None, None]
    img /= std[:, None, None]

    # Random flip & crop
    '''
    if train:
        img = transforms.random_crop(img, (512, 512))
    '''
    return img, label
#######################################################
# set random seed
reset_seed(0)

chainer.cuda.set_max_workspace_size(256 * 1024 * 1024)
chainer.config.autotune = True

# dataset path
img_root1 = 'C:\\Users\\NaoyaInoue\\Desktop\\syspro_gr3\\label1'
img_root2 = 'C:\\Users\\NaoyaInoue\\Desktop\\syspro_gr3\\label2'
img_root3 = 'C:\\Users\\NaoyaInoue\\Desktop\\syspro_gr3\\label3'
img_root = [img_root1, img_root2, img_root3]

Honkan_dataset = create_dataset.create_data_set(img_root, [0,1,2], 300)
#print(Honkan_dataset[0][0])
model = train(DeepCNN(3), Honkan_dataset, batchsize=1, max_epoch=100, base_lr=0.01, lr_decay=(30, 'epoch'))
#model = train(MyNet(3), Honkan_dataset, batchsize=1, max_epoch=100, base_lr=0.1, lr_decay=(30, 'epoch'))
