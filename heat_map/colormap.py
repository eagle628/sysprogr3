
import numpy as np
import cv2
from enum import Enum

class Region:
    Hbf00 = [296,364]
    Hbf01 = [158,368]
    Hbf02 = [448,368]
    Hbf03 = [94,302]
    Hbf04 = [94,156]
    Hbf05 = [206,302]
    Hbf06 = [206,156]
    Hbf07 = [385,302]
    Hbf08 = [385,156]
    Hbf09 = [496,302]
    Hbf10 = [496,156]
    Hbf11 = [160,106]
    Hbf12 = [434,106]

    H1f00 = [296,364]
    H1f01 = [158,368]
    H1f02 = [448,368]
    H1f03 = [94,302]
    H1f04 = [94,156]
    H1f05 = [206,302]
    H1f06 = [206,156]
    H1f07 = [385,302]
    H1f08 = [385,156]
    H1f09 = [496,302]
    H1f10 = [496,156]
    H1f11 = [160,106]
    H1f12 = [434,106]

    H2f00 = [296,364]
    H2f01 = [158,368]
    H2f02 = [448,368]
    H2f03 = [94,302]
    H2f04 = [94,156]
    H2f05 = [206,302]

class Heatmapimage : 

    def __init__(self,map_image1,map_image2, quality = 1):
        self.original_map = cv2.imread(map_image1)
        self.original_map_cut = cv2.imread(map_image2,-1)
        self.resize_scale = quality
        self.image_size = list(self.original_map.shape[0:2])
        self.colormap_size = [int(x / quality) for x in self.image_size]
        self.color_weight = np.zeros(self.colormap_size+[1,], np.uint16)
        self.blank_image = np.zeros(self.image_size+[1,], np.uint8)

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
    
    def add_gaussian(self,pos,var,weight):
        pos[0] = (pos[0] - self.image_size[1]/2) / self.resize_scale
        pos[1] = (pos[1] - self.image_size[0]/2) / self.resize_scale
        var = [x / (self.resize_scale * self.resize_scale) for x in var]
        # var = [x / self.resize_scale for x in var]
        Z = self.__gaussian_2d_matrix(pos,var)
        Z = (Z * 255 * weight) / np.amax(Z)   
        self.color_weight[:,:,0] = self.color_weight[:,:,0] + Z
    
    def add_circle(self,pos,shape,darkness):
        self.blank_image = cv2.ellipse(self.blank_image,((pos[0],pos[1]),(shape[0],shape[1]),360),(darkness,darkness,darkness), -1)       

    def export_heatmap(self, alpha,color_type,blur=10):
        # self.color_weight = (self.color_weight / np.amax(self.color_weight) ) * 255
        # self.color_weight = self.color_weight.astype(np.uint8)
        # self.image_size[0],self.image_size[1] = self.image_size[1],self.image_size[0]
        # self.image_size = tuple(self.image_size)
        # self.color_weight = cv2.resize(self.color_weight, self.image_size)
        # color_map = cv2.applyColorMap(self.color_weight, color_type)
        # blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        color_map = cv2.blur(color_map,(blur,blur))
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        return blended

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

    def export_heatmap_with_colorbar(self, alpha,color_type,blur=10):
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        color_map = cv2.blur(color_map,(blur,blur))
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        # array = self.__get_gradation_3d(512, 256, (0, 0, 0), (255, 255, 255), (True, True, True))
        gradation_array = self.__get_gradation_3d(50, self.image_size[0], (255, 255, 255), (0, 0, 0), (False, False, False))
        color_bar = cv2.applyColorMap(gradation_array, color_type)
        heatmap = cv2.hconcat([blended, color_bar])
        return heatmap
    
    def export_heatmap_with_colorbar_overlay(self,color_type,blur=10):
        color_map = cv2.applyColorMap(self.blank_image, color_type)
        color_map = cv2.blur(color_map,(blur,blur))
        # blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)

        mask = self.original_map_cut[:,:,3]  # アルファチャンネルだけ抜き出す。
        mask = np.dstack([mask,mask,mask])
        self.original_map_cut = self.original_map_cut[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない

        color_map *= 255 - mask  # 透過率に応じて元の画像を暗くする
        color_map += self.original_map_cut  # 貼り付ける方の画像に透過率をかけて加算

        gradation_array = self.__get_gradation_3d(50, self.image_size[0], (255, 255, 255), (0, 0, 0), (False, False, False))
        color_bar = cv2.applyColorMap(gradation_array, color_type)
        heatmap = cv2.hconcat([color_map, color_bar])

        return heatmap
 





