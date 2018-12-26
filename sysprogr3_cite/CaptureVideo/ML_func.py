import cv2
import os
from imutils import paths
import random
import logging

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
            #resized_image = cv2.resize(cropped_image,(int(round(cropped_image.shape[1]/resize_scale)),int(round(cropped_image.shape[0]/resize_scale))))

            preprocessed_image_name.append(os.path.join(root_path, os.path.splitext(image_name)[0]) + '_' +str(i) + extension)
            cv2.imwrite(preprocessed_image_name[-1], cropped_image)
            logging.debug('---------------**WRITE IMAGE**---------------')

    return preprocessed_image_name
