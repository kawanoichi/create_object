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
    # 点群予測関数の実行
    # point_file_name = os.path.splitext(image_name)[0] + ".npy"
    # pp = Predict_Point()
    # pp.predict(image_name, point_file_name)

    try:
        point_file_name = os.path.splitext(image_name)[0] + ".npy"
        pp = Predict_Point()
        pp.predict(image_name,
                   save_dir_path = DATA_DIR_PATH,
                   save_file_name = point_file_name)
    except Exception as e:
        print(e)
        success = False

    try:
        npy_file_path = os.path.exists(DATA_DIR_PATH, point_file_name)
        if npy_file_path:
            # chmodを実行
            os.chmod(npy_file_path, 0o777)
        else:
            return f"{npy_file_path} is not exist"
    except Exception as e:
        print(e)
        success = False


    try:
        # 表面情報の作成
        ms = MakeSurface(point_file_dir=WORK_DIR_PATH,
                        point_file_name=point_file_name)
        ms.main()
    except Exception as e:
        print(e)
        success = False

    return success


image_name = sys.argv[1]
success = main(image_name)

if success:
    print(f"Python is success")
else:
    print(f"Python is failed")
