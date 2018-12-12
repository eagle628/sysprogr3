# -*- coding: utf-8 -*-

import cv2
import os
from imutils import paths
import uuid
import random

import re
import shutil

import numpy as np
import matplotlib.pyplot as plt


def video2frames(root='.', video_file='video.mov', image_dir='image_dir', image_file='img_frame', extension='.jpg', interval=0):
  # Make the directory if it doesn't exist.

  if not os.path.exists(os.path.join(root,image_dir)):
          os.makedirs(os.path.join(root,image_dir))

  # Video to frames
  i = 0
  cap = cv2.VideoCapture(os.path.join(root, video_file))
  while(cap.isOpened()):
      flag, frame = cap.read()  # Capture frame-by-frame
      if flag == False:  # Is a frame left?
          break
      if (i % (interval+1)) is 0 :
          image_file_frame = image_file + str(i) + extension
          save_path = os.path.join(root,image_dir,image_file_frame)
          cv2.imwrite(save_path, frame)  # Save a frame
          print('Save', save_path)
      i += 1

  cap.release()  # When everything done, release the capture



# loot_path = "./original_images" #生画像データが入っているディレクトリ
# threshold = 200 #微分フィルタ評価値のスレッショルド
# decimate_rate = 0 #間引き率　0~1 (間引きされる割合　1ならすべて間引き　0で全通過)
# crop_number = 3 #一枚の画像から切り抜き画像を吐き出す数
# crop_size = 1000 #クロップ（正方形）するときの辺のピクセル数
# resize_scale = 1 #クロップしたあとのリサイズスケール

def blur_filtering(loot_path,threshold = 20):

    if not os.path.exists(os.path.join(loot_path,'filterd_images')):
        os.makedirs(os.path.join(loot_path,'filterd_images'))

    filelist = os.listdir(os.path.join(loot_path,'labeled_images'))
    labeled_directories = [f for f in filelist if os.path.isfile(os.path.join(loot_path,'labeled_images', f)) is False]
    print"Label List\n",labeled_directories

    for directory_name in labeled_directories:
        directory_path = os.path.join(loot_path,'labeled_images',directory_name)
        for image_path in paths.list_images(directory_path):
            print image_path
            image = cv2.imread(image_path)
            print 'imaze size : ', image.shape
            if image.shape[0] >= 1920 or image.shape[1] >= 1920 :
                grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(grey, cv2.CV_64F)
                print 'laplacian value :' ,laplacian.var()
                if laplacian.var() >= threshold :
                    resize_image = cv2.resize(image,(1080,1920))
                    cv2.imwrite(loot_path + '/filterd_images/' + directory_name + '_' + str(uuid.uuid4()) + '.png', resize_image)
                    print '---------------\n**WRITE IMAGE**\n---------------'
            print '\n'

def show_blur_hist(loot_path):

    filelist = os.listdir(os.path.join(loot_path,'labeled_images'))
    labeled_directories = [f for f in filelist if os.path.isfile(os.path.join(loot_path,'labeled_images', f)) is False]
    print"Label List\n",labeled_directories

    x = np.array([])

    for directory_name in labeled_directories:
        directory_path = os.path.join(loot_path,'labeled_images',directory_name)
        for image_path in paths.list_images(directory_path):
            print image_path
            image = cv2.imread(image_path)
            print 'imaze size : ', image.shape
            if image.shape[0] >= 1920 or image.shape[1] >= 1920 :
                grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(grey, cv2.CV_64F)
                print 'laplacian value :' ,laplacian.var()
                x = np.append(x, laplacian.var())

            print '\n'
    print x
    plt.hist(x,bins=100)
    plt.show()


def img_selection(loot_path, decimate_rate = 0, crop_number = 3, crop_size = 1000, resize_scale = 1):

    if not os.path.exists(os.path.join(loot_path,'selected_images')):
        os.makedirs(os.path.join(loot_path,'selected_images'))

    if not os.path.exists(os.path.join(loot_path,'selected_images_grey')):
        os.makedirs(os.path.join(loot_path,'selected_images_grey'))

    for image_path in paths.list_images(os.path.join(loot_path,'filterd_images')):

        if random.random() >= decimate_rate :
            print image_path
            image = cv2.imread(image_path)

            for i in range(crop_number) :
                x = random.randint(0, 1920 - crop_size)
                y = random.randint(0, 1020 - crop_size)
                cropped_image = image[x:x+crop_size,y:y+crop_size]

                resized_image = cv2.resize(cropped_image,(int(round(cropped_image.shape[1]/resize_scale)),int(round(cropped_image.shape[0]/resize_scale))))

                cv2.imwrite(loot_path + '/selected_images/' + os.path.splitext(os.path.basename(image_path))[0] + '_' +str(i) + '.png', resized_image)

                grey = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(loot_path + '/selected_images_grey/' + os.path.splitext(os.path.basename(image_path))[0] + '_' +str(i) + '.png', grey)

                print '---------------\n**WRITE IMAGE**\n---------------'

        print '\n'
