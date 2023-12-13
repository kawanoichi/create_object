import os
import sys

from predict_point_cpu import Predict_Point
from create_surface import MakeSurface

SCRIPT_DIR_PATH = os.path.dirname(
    os.path.abspath(__file__))  # create_object_py/src
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)  # create_object_py
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")
DATA_DIR_PATH = "/var/www/html/storage/app/public/data"


def main(image_name):
    success = True

    # pathの設定
    input_img_dir_path = DATA_DIR_PATH
    npy_dir_path = DATA_DIR_PATH
    ply_dir_path = DATA_DIR_PATH

    # 画像から点群データ(npy)を作成
    try:
        pp = Predict_Point(img_dir_path=input_img_dir_path,
                           model_path=os.path.join(
                               WORK_DIR_PATH, "modelG_50.pth"),
                           point_save_dir_path=npy_dir_path)
        pp.predict(image_name)
    except Exception as e:
        print(f"{e} (1)\n")
        success = False

    # npyファイルに権限付与
    try:
        npy_file_name = os.path.splitext(image_name)[0] + ".npy"
        npy_file_path = os.path.join(npy_dir_path, npy_file_name)
        if npy_file_path:
            # chmodを実行
            os.chmod(npy_file_path, 0o777)
        else:
            return f"{npy_file_path} is not exist"
    except Exception as e:
        print(f"{e} (2)\n")
        success = False

    # 点群データからplyファイルの作成
    try:
        ms = MakeSurface(point_dir=npy_dir_path,
                         ply_save_dir=ply_dir_path)
        ms.main(image_name)
    except Exception as e:
        print(f"{e} (3)\n")
        success = False

    # plyファイルに権限付与
    try:
        ply_file_name = os.path.splitext(image_name)[0] + ".ply"
        ply_file_path = os.path.join(ply_dir_path, ply_file_name)
        if ply_file_path:
            # chmodを実行
            os.chmod(ply_file_path, 0o777)
        else:
            return f"{ply_file_path} is not exist"
    except Exception as e:
        print(f"{e} (4)\n")
        success = False

    return success


if __name__ == "__main__":
    print("### python ###")
    image_name = sys.argv[1]
    object_category = sys.argv[2]
    success = main(image_name)

    if success:
        print(f"Python is success")
    else:
        print(f"Python is failed")

    print(f"object_category is {object_category}")
    print("###########")
