# coding: UTF-8
import cv2
from colormap import Heatmapimage
from colormap import Region
import time

t1 = time.time() 
 
#オリジナル画像と重み描画分解能を指定してインスタンス生成
heatmap1 = Heatmapimage('1f_all.jpg',5) 

#描画中心座標，xy分散,重みを指定して，ガウシアン（山）を書き込み
heatmap1.add_gaussian(Region.Hbf01,[100,100],0.1)
heatmap1.add_gaussian(Region.Hbf02,[100,100],0.2)
heatmap1.add_gaussian(Region.Hbf03,[100,100],0.3)
heatmap1.add_gaussian(Region.Hbf04,[100,100],0.4)
heatmap1.add_gaussian(Region.Hbf05,[100,100],0.5)
heatmap1.add_gaussian(Region.Hbf06,[100,100],0.6)
heatmap1.add_gaussian(Region.Hbf07,[100,100],0.7)
heatmap1.add_gaussian(Region.Hbf08,[100,100],0.8)
heatmap1.add_gaussian(Region.Hbf09,[100,100],0.9)
heatmap1.add_gaussian(Region.Hbf10,[100,100],1.0)
heatmap1.add_gaussian(Region.Hbf11,[100,100],1.0)
heatmap1.add_gaussian(Region.Hbf12,[100,100],1.0)

#ヒートマップ画像を生成
#カラーマップはCOLORMAP_OCEAN,COLORMAP_HSV,COLORMAP_RAINBOW,COLORMAP_HOTなどがある
color_map1 = heatmap1.export_heatmap(0.65,cv2.COLORMAP_HOT)

t2 = time.time()
print(t2-t1)

# 表示
cv2.imshow('color_map',color_map1)
cv2.waitKey(0)