"""Open3Dで3D点群をメッシュ(ポリゴン)に変換するプログラム.
plyファイルからmeshを生成する.
参考URL
    Open3DとPythonによる実装
    https://tecsingularity.com/open3d/bpa/
    PLYファイルについて
    https://programming-surgeon.com/imageanalysis/ply-python/
実行コマンド
$ make surface_run
"""
import open3d as o3d
import numpy as np
import os

from src.edit_normal import EditNormal
from param_create_surface import Param
from log import Log
from my_plt import MyPlt


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class MakeSurface:
    """点群から表面を作りplyファイルに保存するクラス."""

    def __init__(self, point_dir, ply_save_dir,
                 vectors_26_path=os.path.join(SCRIPT_DIR_PATH, "vector26.npy")) -> None:
        """コンストラクタ.

        Args:
            point_file (str): 点群ファイル(.npy)
        """
        # ログ用
        self.log = Log()
        self.myplt = MyPlt(max_graph_num=6)

        # Path
        self.point_dir = point_dir
        self.ply_save_dir = ply_save_dir

        self.check_exist(self.point_dir)
        self.check_exist(self.ply_save_dir)

        self.groupe = None

        # 26方位ベクトルの作成([x, y, z])
        self.check_exist(vectors_26_path)
        self.vectors_26 = np.load(vectors_26_path)

    @staticmethod
    def check_exist(path):
        """ファイル, ディレクトリの存在確認を行う関数."""
        if not os.path.exists(path):
            raise Exception(f"Error :No such file or directory: '{path}'")

    def rotate_object(self, points, angle, axis="x"):
        """点群を回転させる関数.
        回転は右手座標系に依存.
        Args:
            points: 入力点群
            angle : 回転させる角度
            axis  : 回転の軸 ('x' or 'y' or 'z')
        Return:
            回転させた点群座標
        """
        theta = np.radians(angle)
        if axis == "x":
            rotation_matrix = np.array([[1, 0, 0],
                                        [0, np.cos(theta), -np.sin(theta)],
                                        [0, np.sin(theta), np.cos(theta)]])
        if axis == "y":
            rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                        [0, 1, 0],
                                        [-np.sin(theta), 0, np.cos(theta)]])
        if axis == "z":
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                        [np.sin(theta), np.cos(theta), 0],
                                        [0, 0, 1]])
        else:
            print("座標を指定してください")
            raise Exception
        # 座標データに回転行列を適用
        return np.dot(points, rotation_matrix.T)

    def main(self, point_file_name, category=0, develop=False, execute_web=False) -> None:
        """点群をメッシュ化し、表示する関数."""
        """
        パス設定
        """
        # 入力点群パス
        point_path = os.path.join(self.point_dir, point_file_name)
        self.check_exist(point_path)

        # 保存PLY(point)パス
        ply_file_name = os.path.splitext(point_file_name)[0] + "_point.ply"
        save_point_path = os.path.join(self.ply_save_dir, ply_file_name)

        # 保存PLY(mesh)パス
        ply_file_name = os.path.splitext(point_file_name)[0] + ".ply"
        save_mesh_path = os.path.join(self.ply_save_dir, ply_file_name)

        """
        メイン処理
        """
        # 点群データの読み込み
        points = np.load(point_path)
        if develop:
            self.log.add(title="points.shape", log=points.shape)
        self.myplt.show_point(points, title="Input Point")  # グラフの追加

        # オブジェクトの向きを調整
        points = self.rotate_object(points, angle=-90, axis="z")
        self.myplt.show_point(points, title="Rotated Input Point")  # グラフに追加

        # NumPyの配列からPointCloudを作成
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

        """法線ベクトルの作成"""
        # 法線情報を計算
        point_cloud.estimate_normals(
            # search_param=o3d.geometry.KDTreeSearchParamHybrid(
            #     radius=1, max_nn=10)
            # search_param=o3d.geometry.KDTreeSearchParamKNN(
            #     knn=20)
        )
        # self.myplt.show_normals(points, normals, title="Normals")  # グラフの追加

        """法線ベクトルの編集"""
        normals = np.asarray(point_cloud.normals)  # numpy配列に変換
        if (Param.edit_normal and develop) or execute_web:
            # メッシュ変数メソッドの実行
            edit = EditNormal(vectors_26=self.vectors_26,
                              develop=develop,
                              log=self.log)
            edited_normals, correct_even_index, correct_odd_index = edit.main(
                category, points, normals)

            # 法線ベクトルの更新
            if edited_normals is not None:
                self.log.add(title="Correct Normals", log="True")
                normals = edited_normals
            else:
                self.log.add(title="Correct Normals", log="False")

            if correct_even_index is not None and correct_odd_index is not None:
                self.log.add(title="correct_even_index len",
                             log=len(correct_even_index))
                self.log.add(title="correct_odd_index len",
                             log=len(correct_odd_index))
                self.myplt.show_correct_point_2D(
                    points, correct_even_index, correct_odd_index, title="Correct Point 2D")
                self.myplt.show_correct_point(
                    points, correct_even_index, correct_odd_index, title="Correct Point 3D")

        # 法線ベクトルの更新
        point_cloud.normals = o3d.utility.Vector3dVector(normals)

        """メッシュ作成"""
        # 三角形メッシュを計算する
        # point_cloud.orient_normals_consistent_tangent_plane(10)
        distances = point_cloud.compute_nearest_neighbor_distance()  # 近傍距離を計算
        avg_dist = np.mean(distances)  # 近傍距離の平均
        radius = 2*avg_dist  # 半径
        radii = [radius, radius * 1.5, radius * 2]  # [半径,直径]
        radii = o3d.utility.DoubleVector(radii)  # numpy配列 >> open3D形式
        recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            point_cloud, radii)

        # 生成したメッシュをPLYファイルに保存
        o3d.io.write_triangle_mesh(save_mesh_path, recMeshBPA)

        """開発用"""
        if develop:
            # 点群ファイルの保存
            if Param.point_only:
                o3d.io.write_point_cloud(save_point_path, point_cloud)

            # 点群や法線ベクトルの表示
            if Param.work_process:
                self.myplt.save_result(os.path.join(WORK_DIR_PATH, 'result.png')) \
                    if Param.output_image else self.myplt.show_result()

            # ディスプレイのサイズを取得
            screen_size = [2560//3, 1440//3]
            # 法線の表示
            if Param.show_normal:
                # ウィンドウの幅と高さをディスプレイのサイズに設定して描画
                o3d.visualization.draw_geometries(
                    [point_cloud], point_show_normal=True, width=screen_size[0], height=screen_size[1])
            # メッシュの表示
            if Param.show_mesh:
                o3d.visualization.draw_geometries(
                    [recMeshBPA], width=screen_size[0], height=screen_size[1])

        return save_mesh_path


if __name__ == "__main__":
    import time
    start = time.time()

    import argparse
    parser = argparse.ArgumentParser(description='コマンドライン引数の説明')
    parser.add_argument('--catecory_number', type=str,
                        default="0", help='オプション引数')
    parser.add_argument('--image_number', type=int,
                        default="0", help='オプション引数')
    args = parser.parse_args()

    import json
    category_file = os.path.join(SCRIPT_DIR_PATH, "category.json")
    with open(category_file) as fp:
        category_data = json.load(fp)

    category_name = category_data[str(args.catecory_number)]

    if args.catecory_number == "0":
        image_list = ["airplane.npy", "two_wings_1.npy", "two_wings_2.npy",
                      "fighter.npy", "jet.npy", "plane.npy"]
        image_name = image_list[args.image_number]
    if args.catecory_number == "1":
        image_list = ["chair_00.npy", "chair_01.npy", "chair_02.npy",
                      "chair_03.npy", "chair_04.npy", "chair_05.npy"]
        image_name = image_list[args.image_number]

    ms = MakeSurface(point_dir=os.path.join(WORK_DIR_PATH, "predict_points", category_name),
                     ply_save_dir=WORK_DIR_PATH)

    ms.log.add(title="Category", log=category_name)

    try:
        ms.main(point_file_name=image_name,
                category=args.catecory_number,
                develop=True)
        # 処理時間計測用
        execute_time = time.time() - start
        ms.log.add(title="Execution time", log=str(execute_time)[:5]+"s")
    finally:
        ms.log.show()

    print("終了")
