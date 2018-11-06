#!python3.6.6
import random
import numpy as np
import chainer
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
from mymodule import network_composition

#############################################################
def reset_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    if chainer.cuda.available:
        chainer.cuda.cupy.random.seed(seed)

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
    trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='{}_HonkanEntrance3_data1500_{}result'.format(network_object.__class__.__name__, postfix))


    # 7. Trainer extensions
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
    trainer.extend(extensions.Evaluator(valid_iter, net, device=gpu_id), name='val')
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'val/main/loss', 'val/main/accuracy', 'l1/W/data/std', 'elapsed_time']))
    trainer.extend(extensions.PlotReport(['l1/W/data/std'], x_key='epoch', file_name='std.png'))
    trainer.extend(extensions.PlotReport(['main/loss', 'val/main/loss'], x_key='epoch', file_name='loss.png'))
    trainer.extend(extensions.PlotReport(['main/accuracy', 'val/main/accuracy'], x_key='epoch', file_name='accuracy.png'))
    trainer.extend(extensions.dump_graph('main/loss'))
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
# 結果保証
reset_seed(0)

chainer.cuda.set_max_workspace_size(256 * 1024 * 1024)
chainer.config.autotune = True

# dataset path
# imageの入っているpathを指定
dir_root = r'C:\Users\NaoyaInoue\Desktop\syspro_gr3\avi2jpg'
img_root1 = r'jpg_label0'
img_root2 = r'jpg_label1'
img_root3 = r'jpg_label2'
img_root = [img_root1, img_root2, img_root3]

N = 300; # １クラス当たりN個乱数で，抽出する．
Honkan_dataset = create_dataset.create_data_set(dir_root, img_root, [0,1,2], N)
print(len(Honkan_dataset))
print(Honkan_dataset[100][1])
#model = train(network_composition.DeepCNN(3), Honkan_dataset, batchsize=1, max_epoch=100, base_lr=0.01, lr_decay=(30, 'epoch'))
#model = train(MyNet(3), Honkan_dataset, batchsize=1, max_epoch=100, base_lr=0.1, lr_decay=(30, 'epoch'))
