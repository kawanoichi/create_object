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


class Predict_Point:
    """画像から3Dオブジェクトを生成するクラス."""

    def __init__(self,
                 img_dir_path: str,
                 model_path: str,
                 point_save_dir_path: str,
                 num_points: int = 2048):
        self.img_dir_path = img_dir_path
        self.model_path = model_path
        self.point_save_dir_path = point_save_dir_path
        self.num_points = num_points

        self.check_exist(self.img_dir_path)
        self.check_exist(self.model_path)
        self.make_dir(self.point_save_dir_path)

    @staticmethod
    def check_exist(path) -> None:
        """ファイル, ディレクトリの存在確認を行う関数."""
        if not os.path.exists(path):
            raise Exception(f"Error :Not exist '{path}'")

    @staticmethod
    def make_dir(path) -> None:
        """中間ディレクトリを作成する関数."""
        os.makedirs(path, exist_ok=True)

    def predict(self, image_name):
        """学習済みモデルを使用して画像から点群を生成する."""
        """
        pathの設定
        """
        # 入力画像(pngファイル)
        read_img_path = os.path.join(self.img_dir_path, image_name)
        self.check_exist(read_img_path)

        # 点群データ保存先(npyファイル)
        save_file_name = os.path.splitext(image_name)[0] + ".npy"
        save_path = os.path.join(self.point_save_dir_path, save_file_name)

        """
        メイン処理
        """
        # 画像読み込み(128, 128, 3)
        image = cv2.imread(read_img_path)
        if image.shape[0] != 137 or image.shape[1] != 137:
            image = cv2.resize(image, (137, 137))
        image = image[4:-5, 4:-5, :3]  # これなんのため？

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
        print(f"save_path: {save_path}")
        np.save(save_path, predict_points)


if __name__ == "__main__":
    """
    実行コマンド
        $ poetry run python3 src/predict_point_cpu.py --catecory_number 0
        $ poetry run python3 src/predict_point_cpu.py --catecory_number 1
    # """
    SCRIPT_DIR_PATH = os.path.dirname(
        os.path.abspath(__file__))  # create_object_py/src
    PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)  # create_object_py
    WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")
    IMAGE_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data", "input_image")

    import argparse
    parser = argparse.ArgumentParser(description='コマンドライン引数の説明')
    parser.add_argument('--catecory_number', type=str,
                        default="0", help='オプション引数')
    args = parser.parse_args()

    import json
    category_file = os.path.join(SCRIPT_DIR_PATH, "category.json")
    with open(category_file) as fp:
        category_data = json.load(fp)

    # Option
    category_name = category_data[str(args.catecory_number)]
    epoch = 100
    # num_points = 1024
    num_points = 2048
    model_file_name = category_name+"_modelG_"+str(epoch)+".pth"

    # 画像のファイル名
    image_dir_path = os.path.join(
        WORK_DIR_PATH, "input_image", category_name)
    image_files = [file for file in os.listdir(
        image_dir_path) if file.endswith('.png')]

    # """
    # 点群予測クラスのインスタンス化
    pp = Predict_Point(img_dir_path=os.path.join(WORK_DIR_PATH, "input_image", category_name),
                       model_path=os.path.join(
                           WORK_DIR_PATH, "learned_model", str(num_points), model_file_name),
                       point_save_dir_path=os.path.join(
                           WORK_DIR_PATH, "predict_points", category_name),
                       num_points=num_points)
    for image_name in image_files:
        pp.predict(image_name)
    # """

    print("終了")
