# coding: UTF-8
import cv2
from colormap import Heatmapimage
from colormap import Region


heatmap1 = Heatmapimage('1f_all.jpg',10) #オリジナル画像と重み描画分解能を指定してインスタンス生成

heatmap1.add_gaussian(Region.bf01,[10000,200],0.1) #描画中心座標，xy分散,重みを指定して，ガウシアン（山）を書き込み
# heatmap1.add_gaussian(Region.bf02,[10,10],1)
# heatmap1.add_gaussian(Region.bf03,[10,10],1)


color_map1 = heatmap1.export_heatmap(0.65,cv2.COLORMAP_HOT)
#ヒートマップ画像を生成
#カラーマップはCOLORMAP_OCEAN,COLORMAP_HSV,COLORMAP_RAINBOW,COLORMAP_HOTなどがある

# 表示
cv2.imshow('color_map',color_map1)
cv2.waitKey(0)