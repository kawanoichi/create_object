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
                   save_dir_path = WORK_DIR_PATH,
                   save_file_name = point_file_name)
    except Exception as e:
        print(f"{e} (1)\n")
        success = False

    try:
        npy_file_path = os.path.join(WORK_DIR_PATH, point_file_name)
        if npy_file_path:
            # chmodを実行
            os.chmod(npy_file_path, 0o777)
        else:
            return f"{npy_file_path} is not exist"
    except Exception as e:
        print(f"{e} (2)\n")
        success = False

    if os.path.exists(npy_file_path) is False:
        print(f"not exists {npy_file_path}")

    try:
        # 表面情報の作成
        ms = MakeSurface(point_file_dir=WORK_DIR_PATH,
                        point_file_name=point_file_name)
        ply_save_path = ms.main()
        
    except Exception as e:
        print(f"{e} (3)\n")
        success = False

    try:
        if ply_save_path:
            # chmodを実行
            os.chmod(ply_save_path, 0o777)
        else:
            return f"{ply_save_path} is not exist"
    except Exception as e:
        print(f"{e} (4)\n")
        success = False
        
    return success

print("### python ###")
image_name = sys.argv[1]
success = main(image_name)

if success:
    print(f"Python is success")
else:
    print(f"Python is failed")

print("###########")