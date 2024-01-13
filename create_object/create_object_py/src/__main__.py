import os
import json

from predict_point_cpu import Predict_Point
from create_surface import MakeSurface

SCRIPT_DIR_PATH = os.path.dirname(
    os.path.abspath(__file__))  # create_object_py/src
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)  # create_object_py
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")
DATA_DIR_PATH = "/var/www/html/storage/app/public/data"


class CreateObject:
    def __init__(self,
                 category_file=os.path.join(SCRIPT_DIR_PATH, "category.json")):
        self.write_param(os.path.join(SCRIPT_DIR_PATH, 'param.json'))
        with open(category_file) as fp:
            self.category_data = json.load(fp)
        self.point_num = 2048

    def write_param(self, param_path):
        # JSONファイルからデータを読み込む
        with open(param_path, 'r') as json_file:
            Param = json.load(json_file)

        # データの変更
        Param['develop'] = False

        # 変更したデータをJSONファイルに書き込む
        with open(param_path, 'w') as json_file:
            json.dump(Param, json_file, indent=2)



    def main(self, image_name, category_num, develop):
        print("main実行OK")
        global DATA_DIR_PATH
        success = True
        if develop:
            DATA_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")  # 作業用
        """Option"""
        # object category
        category_name = self.category_data[str(category_num)]  # 例: "airplane"

        # model path
        model_path = os.path.join(
            WORK_DIR_PATH, "learned_model", str(self.point_num), category_name+"_modelG_50.pth")

        # file name
        npy_file_name = os.path.splitext(image_name)[0] + ".npy"
        ply_file_name = os.path.splitext(image_name)[0] + ".ply"

        # save path
        input_img_dir_path = DATA_DIR_PATH
        npy_dir_path = DATA_DIR_PATH
        npy_file_path = os.path.join(npy_dir_path, npy_file_name)
        ply_dir_path = DATA_DIR_PATH
        ply_file_path = os.path.join(ply_dir_path, ply_file_name)

        # develop path
        if develop:
            input_img_dir_path = os.path.join(
                DATA_DIR_PATH, "input_image", category_name)
            npy_dir_path = os.path.join(DATA_DIR_PATH, "predict_points")
        print("Option設定OK")

        """3Dオブジェクト生成"""
        # 画像から点群データ(npy)を作成
        try:
            pp = Predict_Point(img_dir_path=input_img_dir_path,
                               model_path=model_path,
                               point_save_dir_path=npy_dir_path,
                               num_points=2048)
            pp.predict(image_name)
        except Exception as e:
            print(f"python script error:\n{e} (1)\n")
            success = False

        # npyファイルに権限付与
        if develop is False:
            try:
                if npy_file_path:
                    # chmodを実行
                    os.chmod(npy_file_path, 0o777)
                else:
                    return f"{npy_file_path} is not exist"
            except Exception as e:
                print(f"python script error:\n{e} (2)\n")
                success = False

        # 点群データからplyファイルの作成
        try:
            ms = MakeSurface(point_dir=npy_dir_path,
                             ply_save_dir=ply_dir_path)
            ms.main(npy_file_name, category=category_num)
        except Exception as e:
            print(f"python script error:\n{e} (3)\n")
            success = False

        if develop is False:
            # plyファイルに権限付与
            try:
                if ply_file_path:
                    # chmodを実行
                    os.chmod(ply_file_path, 0o777)
                else:
                    return f"{ply_file_path} is not exist"
            except Exception as e:
                print(f"python script error:\n{e} (4)\n")
                success = False

        return success


if __name__ == "__main__":
    """
    実行コマンド:
        $ poetry run python3 -m src -img airplane.png -category 0 --develop
        $ poetry run python3 -m src -img chair_00.png -category 1 --develop
    # """

    print("### python ###")
    import argparse
    # ArgumentParserオブジェクトの作成
    parser = argparse.ArgumentParser(description='コマンドライン引数の説明')

    # 引数の定義
    parser.add_argument('--img_name', "-img", type=str, help='画像のファイル名')
    parser.add_argument('--catecory_number', "-category", type=str,
                        default=0, help='生成するオブジェクトのカテゴリ')
    parser.add_argument('--develop', action='store_true', help='開発用フラグ')

    # コマンドライン引数の解析
    args = parser.parse_args()

    create = CreateObject()
    success = create.main(image_name=args.img_name,
                          category_num=args.catecory_number,
                          develop=args.develop)
    print(f"Python is success") if success else print(f"Python is failed")
    print("###########")
