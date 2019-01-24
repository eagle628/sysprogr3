# coding: UTF-8
import cv2
from colormap import Heatmapimage


heatmap1 = Heatmapimage('1f.jpg') #オリジナル画像を指定してインスタンス生成

heatmap1.add_gaussian([551,336],[800,6000],1) #描画中心座標，xy分散,重みを指定して，ガウシアン（山）を書き込み
heatmap1.add_gaussian([311,336],[800,6000],0.5)
heatmap1.add_gaussian([726,428],[1000,1000],0.8)


color_map1 = heatmap1.export_heatmap(0.3,cv2.COLORMAP_RAINBOW)
#ヒートマップ画像を生成
#カラーマップはCOLORMAP_OCEAN,COLORMAP_HSV,COLORMAP_RAINBOW,COLORMAP_HOTなどがある

# 表示
cv2.imshow('color_map',color_map1)
cv2.waitKey(0)