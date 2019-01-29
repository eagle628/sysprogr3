import numpy as np
import cv2
import os
import json
import uuid
import logging


class Heatmapimage :

    def __init__(self, map_path, quality=1):
        self.original_map = cv2.imread(map_path)
        self.resize_scale = quality
        self.image_size = list(self.original_map.shape[0:2])
        self.colormap_size = [int(x / quality) for x in self.image_size]
        self.color_weight = np.zeros(self.colormap_size+[1,], np.uint8)
        # read point
        map_path_root = os.path.dirname(map_path)
        with open(os.path.join(map_path_root,'point.json'),'r') as f:
            self.point = json.load(f)

    def __gaussian_2d(self,x,y):
        x_c = np.array([x, y]) - self.mu
        return np.exp(- x_c.dot(self.inv_sigma).dot(x_c[np.newaxis, :].T) / 2.0) / (2*np.pi*np.sqrt(self.det))

    def __gaussian_2d_matrix(self,pos,var):
        self.mu = np.array([pos[0],pos[1]])
        sigma = np.array([[var[0],0],
                          [0,var[1]]])
        self.det = np.linalg.det(sigma)
        self.inv_sigma = np.linalg.inv(sigma)

        x = np.arange(-1 * self.colormap_size[1] /2, self.colormap_size[1] / 2, 1)
        y = np.arange(-1 * self.colormap_size[0] / 2, self.colormap_size[0] / 2, 1)
        X, Y = np.meshgrid(x, y)
        return np.vectorize(self.__gaussian_2d)(X,Y)

    def add_gaussian(self,point,weight):
        pos = self.point[str(point)][0]
        pos[0] = (pos[0] - self.image_size[1]/2) / self.resize_scale
        pos[1] = (pos[1] - self.image_size[0]/2) / self.resize_scale
        logging.debug(pos)
        var = self.point[str(point)][1]
        var = [x / (self.resize_scale * self.resize_scale) for x in var]
        Z = self.__gaussian_2d_matrix(pos,var)
        Z = (Z * 255 * weight) / np.amax(Z)
        self.color_weight[:,:,0] = self.color_weight[:,:,0] + Z
        self.color_weight = (self.color_weight / np.amax(self.color_weight) ) * 255


    def export_heatmap(self, root, alpha=0.3, color_type=cv2.COLORMAP_RAINBOW):
        self.color_weight = self.color_weight.astype(np.uint8)
        self.image_size[0],self.image_size[1] = self.image_size[1],self.image_size[0]
        self.image_size = tuple(self.image_size)
        self.color_weight = cv2.resize(self.color_weight, self.image_size)
        color_map = cv2.applyColorMap(self.color_weight, color_type)
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        filename = os.path.join(root,str(uuid.uuid4()).replace('-', '')+'.jpg')
        cv2.imwrite(filename, blended)
        return filename
