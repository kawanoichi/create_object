import os
import sys

from predict_point_cpu import Predict_Point
from create_surface import MakeSurface

SCRIPT_DIR_PATH = os.path.dirname(
    os.path.abspath(__file__))  # create_object_py/src
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)  # create_object_py
DATA_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


def main(image_name):
    # 点群予測関数の実行
    point_file_name = os.path.splitext(image_name)[0] + ".npy"
    pp = Predict_Point()
    pp.predict(image_name, point_file_name)

    # 表面情報の作成
    ms = MakeSurface(point_file_dir=DATA_DIR_PATH,
                     point_file_name=point_file_name)
    ms.main()


image_name = sys.argv[1]
main(image_name)
