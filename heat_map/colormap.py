
import numpy as np
import cv2



class Heatmapimage : 

    def __init__(self,map_image, quality = 1):
        self.original_map = cv2.imread(map_image)
        self.resize_scale = quality
        self.image_size = list(self.original_map.shape[0:2])
        self.colormap_size = [int(x / quality) for x in self.image_size]
        self.color_weight = np.zeros(self.colormap_size+[1,], np.uint8)

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
        Z = self.__gaussian_2d_matrix(pos,var)
        Z = (Z * 255 * weight) / np.amax(Z)   
        self.color_weight[:,:,0] = self.color_weight[:,:,0] + Z
        self.color_weight = (self.color_weight / np.amax(self.color_weight) ) * 255


    def export_heatmap(self, alpha,color_type):
        self.color_weight = self.color_weight.astype(np.uint8)
        self.image_size[0],self.image_size[1] = self.image_size[1],self.image_size[0]
        self.image_size = tuple(self.image_size)
        self.color_weight = cv2.resize(self.color_weight, self.image_size)
        color_map = cv2.applyColorMap(self.color_weight, color_type)
        blended = cv2.addWeighted(self.original_map, 1 - alpha, color_map, alpha, 0)
        return blended





