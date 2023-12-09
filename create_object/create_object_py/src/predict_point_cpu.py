"""学習済みモデルを使用して画像から3Dオブジェクトを生成する.
https://github.com/yonghanzhang94/A-Single-View-3D-Object-Point-Cloud-Reconstruction/blob/master/show_shapenet.py
をもとに作成

実行コマンド
$ python3 predict_point_shapenet.py
"""
import os
import cv2
import numpy as np
import torch
from torch.autograd import Variable

from model import generator

SCRIPT_DIR_PATH = os.path.dirname(
    os.path.abspath(__file__))  # create_object_py/src
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)  # create_object_py
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")
DATA_DIR_PATH = "/var/www/html/storage/app/public/data"


class Predict_Point:
    """画像から3Dオブジェクトを生成するクラス."""

    def __init__(self,
                 model_path=os.path.join(WORK_DIR_PATH, "modelG_50.pth"),
                 num_points=2048):
        self.model_path = model_path
        self.num_points = num_points

    def predict(self, image_name, save_file_name=None):
        """学習済みモデルを使用して画像から点群を生成する."""
        read_img_path = os.path.join(
            DATA_DIR_PATH, image_name)
        if not os.path.exists(read_img_path):
            print("Error: image is not exist")
            print("Search path is ", read_img_path)
            exit()

        # 画像読み込み(128, 128, 3)
        image = cv2.imread(read_img_path)
        image = cv2.resize(image, (128, 128))
        image = image[4:-5, 4:-5, :3]

        # BGRからRGBへの変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 配列の形状を変更
        image = np.transpose(image, (2, 0, 1))

        # Tensorクラスのインスタンス化
        image = torch.Tensor(image)

        # 指定した位置にサイズ1の次元を挿入する
        # torch.Size([3, 128, 128]) >>> torch.Size([1, 3, 128, 128])
        image = image.unsqueeze(0)

        # generatorクラスのインスタンス化
        gen = generator(self.num_points, use_gpu=False)

        gen.eval()

        # 学習済みモデルの読み込み
        with open(self.model_path, "rb") as f:
            gen.load_state_dict(torch.load(
                f, map_location=torch.device('cpu')))

        # torch.Tensorに計算グラフの情報を保持させる
        image = Variable(image.float())

        # 点群生成
        points, _, _, _ = gen(image)

        points = points.detach().numpy()

        # (1, 3, 1024) >>> (3, 1024)
        points = np.squeeze(points)

        # (3, 1024) >>> (3, 1024)
        predict_points = np.transpose(points, (1, 0))

        # 予測座標の保存
        if save_file_name is None:
            save_file_name = os.path.splitext(image_name)[0] + ".npy"
        pre_save_path = os.path.join(WORK_DIR_PATH, save_file_name)

        np.save(pre_save_path, predict_points)


if __name__ == "__main__":
    print(f"SCRIPT_DIR_PATH : {SCRIPT_DIR_PATH}")
    print(f"PROJECT_DIR_PATH: {PROJECT_DIR_PATH}")
    print(f"WORK_DIR_PATH   : {WORK_DIR_PATH}")
    print(f"DATA_DIR_PATH   : {DATA_DIR_PATH}")

    # 画像のファイル名
    image_name = "airplane.png"

    # 点群予測クラスのインスタンス化
    pp = Predict_Point()
    # 点群予測関数の実行
    pp.predict(image_name)

    print("終了")
