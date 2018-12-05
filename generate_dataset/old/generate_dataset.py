# -*- coding: utf-8 -*-

import cv2
import os
from imutils import paths
import uuid
import random

loot_path = "./original_images" #生画像データが入っているディレクトリ
threshold = 200 #微分フィルタ評価値のスレッショルド
decimate_rate = 0 #間引き率　0~1 (間引きされる割合　1ならすべて間引き　0で全通過)
crop_number = 3 #一枚の画像から切り抜き画像を吐き出す数
crop_size = 1000 #クロップ（正方形）するときの辺のピクセル数
resize_scale = 1 #クロップしたあとのリサイズスケール

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)


if __name__ == '__main__':

    filelist = os.listdir(loot_path)
    labeled_directories = [f for f in filelist if os.path.isfile(os.path.join(loot_path, f)) is False]
    print"Label List\n",labeled_directories

    for directory_name in labeled_directories:
        directory_path = loot_path + '/' + directory_name
        for image_path in paths.list_images(directory_path):
            print image_path
            image = cv2.imread(image_path)
            print 'imaze size : ', image.shape
            if image.shape[0] >= 1920 or image.shape[1] >= 1920 :
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                laplacian = variance_of_laplacian(gray)
                print 'laplacian value :' ,laplacian.var()
                if laplacian.var() >= threshold :
                    resize_image = cv2.resize(image,(1080,1920))
                    cv2.imwrite('./filterd_images/' + directory_name + '_' + str(uuid.uuid4()) + '.png', resize_image)
                    print '---------------\n**WRITE IMAGE**\n---------------'
            print '\n'


    for image_path in paths.list_images('filterd_images'):

        if random.random() >= decimate_rate :
            print image_path
            image = cv2.imread(image_path)

            for i in range(crop_number) :
                x = random.randint(0, 1920 - crop_size)
                y = random.randint(0, 1020 - crop_size)
                cropped_image = image[x:x+crop_size,y:y+crop_size]

                resized_image = cv2.resize(cropped_image,(int(round(cropped_image.shape[1]/resize_scale)),int(round(cropped_image.shape[0]/resize_scale))))
                cv2.imwrite('./generated_dataset/' + image_path[15:-4] + '_' +str(i) + '.png', resized_image)
                print '---------------\n**WRITE IMAGE**\n---------------'

        print '\n'
