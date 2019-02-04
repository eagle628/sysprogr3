import numpy as np
import cv2
import os
import json
import uuid
import logging


class Treemapimage :

    def __init__(self, map_path, quality=1):
        self.original_map = cv2.imread(map_path+'.jpg')
        self.resize_scale = quality
        self.image_size = list(self.original_map.shape[0:2])
        # read point
        map_path_root = os.path.dirname(map_path)
        with open(os.path.join(map_path_root,'point.json'),'r') as f:
            self.point = json.load(f)

    def __add_arrowedLine(self, point, color=(0, 255, 0), thickness=5, shift=0, tipLength=0.1):
        cv2.arrowedLine(
                        self.original_map,
                        self.__trans_pos(point[0]),  self.__trans_pos(point[1]),
                        color,
                        thickness=thickness, shift=shift, tipLength=tipLength,
                        )

    def __add_marker(self, point, color=(0, 0, 255), thickness=5, markerType=cv2.MARKER_SQUARE):
        cv2.drawMarker(
                    self.original_map,
                    self.__trans_pos(point),
                    color,
                    thickness=thickness, markerType=markerType,
                    )

    def __trans_pos(self, point):
        pos = self.point[str(point % 13)][0]
        pos = tuple(pos)
        return pos

    def export_treemap(self, root, node_list):
        for node in node_list:
            self.__add_marker(node)
        for itr in range(0,len(node_list)-1):
            self.__add_arrowedLine(node_list[itr:itr+2])
        # write image
        filename = os.path.join(root,str(uuid.uuid4()).replace('-', '')+'.jpg')
        cv2.imwrite(filename, self.original_map)
        return filename

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    AAA = Treemapimage(os.path.join(path,'Map_Honkan','1f_all.jpg'))
    node_list = [7,8,12,10,9,2,0,5,6,11,4,3]
    #AAA.export_treemap('.',node_list) # cut write image line
    #cv2.imshow('Tree', AAA.original_map)
    #cv2.waitKey(0)
