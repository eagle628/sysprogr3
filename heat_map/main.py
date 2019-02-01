# coding: UTF-8
import cv2
from colormap import Heatmapimage
from colormap import Region
import time

t1 = time.time() 
 
#オリジナル画像と重み描画分解能を指定してインスタンス生成
heatmap1 = Heatmapimage('1f_all.jpg','1f_all.png',5) 

#描画中心座標，xy分散,重みを指定して，ガウシアン（山）を書き込み
# heatmap1.add_gaussian(Region.Hbf01,[1000,1000],0.1)
# heatmap1.add_gaussian(Region.Hbf02,[1000,1000],0.2)
# heatmap1.add_gaussian(Region.Hbf03,[1000,1000],0.3)
# heatmap1.add_gaussian(Region.Hbf04,[1000,1000],0.4)
# heatmap1.add_gaussian(Region.Hbf05,[1000,1000],0.5)
# heatmap1.add_gaussian(Region.Hbf06,[1000,1000],0.6)
# heatmap1.add_gaussian(Region.Hbf07,[1000,1000],0.7)
# heatmap1.add_gaussian(Region.Hbf08,[1000,1000],0.8)
# heatmap1.add_gaussian(Region.Hbf09,[1000,1000],0.9)
# heatmap1.add_gaussian(Region.Hbf10,[1000,1000],1.0)
# heatmap1.add_gaussian(Region.Hbf11,[1000,1000],1.0)
# heatmap1.add_gaussian(Region.Hbf12,[1000,1000],1.0)

heatmap1.add_circle(Region.Hbf00,[120,20],50)
heatmap1.add_circle(Region.Hbf01,[120,20],100)
heatmap1.add_circle(Region.Hbf02,[120,20],100)
heatmap1.add_circle(Region.Hbf03,[20,120],10)
heatmap1.add_circle(Region.Hbf04,[20,120],10)
heatmap1.add_circle(Region.Hbf05,[20,120],10)
heatmap1.add_circle(Region.Hbf06,[20,120],10)
heatmap1.add_circle(Region.Hbf07,[20,120],10)
heatmap1.add_circle(Region.Hbf08,[20,120],10)
heatmap1.add_circle(Region.Hbf09,[20,120],10)
heatmap1.add_circle(Region.Hbf10,[20,120],10)
heatmap1.add_circle(Region.Hbf11,[120,20],200)
heatmap1.add_circle(Region.Hbf12,[120,20],200)

#ヒートマップ画像を生成
#カラーマップはCOLORMAP_OCEAN,COLORMAP_HSV,COLORMAP_RAINBOW,COLORMAP_HOTなどがある
color_map1 = heatmap1.export_heatmap(0.65,cv2.COLORMAP_JET,15)
color_map1 = heatmap1.export_heatmap_with_colorbar(0.65,cv2.COLORMAP_JET,15)
color_map1 = heatmap1.export_heatmap_with_colorbar_overlay(cv2.COLORMAP_JET,15)
t2 = time.time()
print(t2-t1)

# 表示
cv2.imwrite('heatmap.jpg',color_map1)
cv2.imshow('color_map',color_map1)
cv2.waitKey(0)