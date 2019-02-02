import numpy as np
import cv2
import os
import json
import uuid
import logging


class Heatmapimage :

    def __init__(self, map_path, quality=1):
        self.original_map = cv2.imread(map_path+'.jpg')
        self.original_map_cut = cv2.imread(map_path+'.png',-1)
        self.resize_scale = quality
        self.image_size = list(self.original_map.shape[0:2])
        self.colormap_size = [int(x / quality) for x in self.image_size]
        self.color_weight = np.zeros(self.colormap_size+[1,], np.uint16)
        self.blank_image = np.zeros(self.image_size+[1,], np.uint8)
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

    def add_circle(self,point,darkness):
        logging.debug(darkness)
        pos = tuple(self.point[str(point % 13)][0])
        shape = tuple(self.point[str(point % 13)][1])
        self.blank_image = cv2.ellipse(self.blank_image,(pos,shape,360),(darkness,darkness,darkness), -1)

    def export_heatmap(self, root, alpha=0.3, color_type=cv2.COLORMAP_RAINBOW):
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        color_map = cv2.blur(color_map,(blur,blur))
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        filename = os.path.join(root,str(uuid.uuid4()).replace('-', '')+'.jpg')
        cv2.imwrite(filename, blended)
        return filename

    def __get_gradation_2d(self, start, stop, width, height, is_horizontal):
        if is_horizontal:
            return np.tile(np.linspace(start, stop, width), (height, 1))
        else:
            return np.tile(np.linspace(start, stop, height), (width, 1)).T

    def __get_gradation_3d(self, width, height, start_list, stop_list, is_horizontal_list):
        result = np.zeros((height, width, len(start_list)), dtype=np.uint8)
        for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
            result[:, :, i] = self.__get_gradation_2d(start, stop, width, height, is_horizontal)
        return result

    def export_heatmap_with_colorbar(self,root, alpha=0.65,color_type=cv2.COLORMAP_JET,blur=10):
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        color_map = cv2.blur(color_map,(blur,blur))
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        # array = self.__get_gradation_3d(512, 256, (0, 0, 0), (255, 255, 255), (True, True, True))
        gradation_array = self.__get_gradation_3d(50, self.image_size[0], (255, 255, 255), (0, 0, 0), (False, False, False))
        color_bar = cv2.applyColorMap(gradation_array, color_type)
        heatmap = cv2.hconcat([blended, color_bar])
        return heatmap

    def export_heatmap_with_colorbar_overlay(self,root,color_type=cv2.COLORMAP_JET,blur=15,mode=False):
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        #color_map = cv2.blur(color_map,(blur,blur))
        # blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        mask = self.original_map_cut[:,:,3]  # アルファチャンネルだけ抜き出す。
        mask = np.dstack([mask,mask,mask])
        self.original_map_cut = self.original_map_cut[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない

        color_map *= 255 - mask  # 透過率に応じて元の画像を暗くする
        color_map += self.original_map_cut  # 貼り付ける方の画像に透過率をかけて加算

        gradation_array = self.__get_gradation_3d(50, self.image_size[0], (255, 255, 255), (0, 0, 0), (False, False, False))
        color_bar = cv2.applyColorMap(gradation_array, color_type)
        heatmap = cv2.hconcat([color_map, color_bar])
        if mode:
            return heatmap
        else :
            filename = os.path.join(root,str(uuid.uuid4()).replace('-', '')+'.jpg')
            cv2.imwrite(filename, heatmap)
            return filename

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    obj = Heatmapimage(os.path.join(path,'Map_Honkan','1f_all'))
    for itr in range(0,13):
        obj.add_circle(itr, 200)

    img = obj.export_heatmap_with_colorbar_overlay('.',mode=True)
    cv2.imshow('map',img)
    cv2.waitKey(0)
