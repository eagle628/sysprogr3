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
### create_data_set(dir_root, image_root_set, label_set, N)
imge_root_set及びlabel_setは，python list型です．
Nは指定したフォルダ内部の画像のうち，何枚使うかを指定します．フォルダ内の画像がNよりも少ない場合には，全部を使うことになっています．

<img src="./images/dir_composition_for_create_data_set.png" width="300">

Requiremetns
###　search_img_name(image_root)
image_root内部にjpg画像が何枚あるかを検索し，そのfile名をlistで返す関数

| packkage | version     |
| :------------- | :------------- |
| chainer       | 5.0.0       |
| numpy   | 1.15.2  |

## generate_image
### video2frames(root='.', video_file='video.mov', image_dir='image_dir', image_file='img_frame', extension='.jpg', interval=0)

<img src="./images/dir_composition_for_video2frames.png" width="300">

上記のようなディレクトリ構造で動画が，フレームごとに分解される．
intervalは，intervalフレームごとに取るということにして要る．
NOTE :　　
- video_fileは，MOVでなくても大丈夫です．例えば，DVI等でも大丈夫です．
- extensionもjpg以外も可能ですが，chainerがjpg, pngにしか対応していない.

Requiremetns

| packkage | version     |
| :------------- | :------------- |
| numpy   | 1.15.2  |
| opencv-python   | 3.4.3.18  |

## network_composition
ネットワーク構造の関数
- ネットワーク構造構造の定義は，このファイル内部に書き込んでいってください．
Requiremetns

| packkage | version     |
| :------------- | :------------- |
| chainer       | 5.0.0       |
| numpy   | 1.15.2  |
