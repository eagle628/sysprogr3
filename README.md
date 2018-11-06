# main_class3.py
3クラス分類用
Requiremetns
| packkage | version     |
| :------------- | :------------- |
| chainer       | 5.0.0       |
| chainercv   | 0.11.0  |
| numpy   | 1.15.2  |

# mymodule
## create_dataset
chainer用のデータセットを作る関数
Requiremetns
| packkage | version     |
| :------------- | :------------- |
| chainer       | 5.0.0       |
| numpy   | 1.15.2  |

## generate_image
### video2frames(root='.', video_file='video.mov', image_dir='image_dir', image_file='img_frame', extension='.jpg', interval=0)
root
|-video_file
|-image_dir - img_frame
のような構造で動画が，フレームごとに分解される．
interbalは，intervalフレームごとに取るということにして要る．

Requiremetns
| packkage | version     |
| :------------- | :------------- |
| numpy   | 1.15.2  |
| opencv-python   | 3.4.3.18  |

## network_composition
ネットワーク構造の関数
Requiremetns
| packkage | version     |
| :------------- | :------------- |
| chainer       | 5.0.0       |
| numpy   | 1.15.2  |
