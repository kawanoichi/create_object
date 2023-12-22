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
from edit_mesh_chair import EditMeshChair
from edit_mesh_airplane import EditMeshAirplane
from param_create_surface import Param
from log import Log

import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os

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

        # Path
        self.point_dir = point_dir
        self.ply_save_dir = ply_save_dir

        self.check_exist(self.point_dir)
        self.check_exist(self.ply_save_dir)

        self.groupe = None

        # 表示する点群(散布図)に関する変数
        self.fig = plt.figure()  # 表示するグラフ
        self.fig_vertical = 2  # 縦
        self.fig_horizontal = 3  # 横
        self.graph_num = 1  # 横

        # 26方位ベクトルの作成([x, y, z])
        self.check_exist(vectors_26_path)
        self.vectors_26 = np.load(vectors_26_path)

        # 26方位に当てはまった各ベクトルの個数
        self.count_vector_class = None

        # y=1方向のベクトルのインデックスを取得
        y1_vector = np.array([0, 1, 0])
        self.y1_vector_index = np.where(
            np.all(self.vectors_26 == y1_vector, axis=1))

        # x=1方向のベクトルのインデックスを取得
        x1_vector = np.array([1, 0, 0])
        self.x1_vector_index = np.where(
            np.all(self.vectors_26 == x1_vector, axis=1))

    @staticmethod
    def check_exist(path):
        """ファイル, ディレクトリの存在確認を行う関数."""
        if not os.path.exists(path):
            raise Exception(f"Error :No such file or directory: '{path}'")

    def show_point(self, points, title="None") -> None:
        """点群を表示する関数.
        NOTE: 表示する軸方向をopen3dと統一
            x: 右方向
            y: 上
            z: 手前
        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num,
                                  projection='3d')
        plt.xlim(-0.3, 0.3)
        plt.ylim(-0.3, 0.3)
        ax.set_zlim(-0.3, 0.3)
        self.graph_num += 1
        plt.title(title)
        ax.set(xlabel='x', ylabel='y', zlabel='z')
        colors1 = np.where(points[:, 0] > 0, 'red', 'blue')
        colors2 = np.where(points[:, 0] > 0, 'purple', 'green')
        colors = np.where(points[:, 1] > 0, colors1, colors2)
        ax.scatter(points[:, 0],
                   points[:, 1],
                   points[:, 2],
                   c=colors)

    def show_point_2D(self, points, title="None") -> None:
        """点群を表示する関数.

        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num)
        self.graph_num += 1

        plt.title(title)
        ax.set(xlabel='x', ylabel='y')

        ax.scatter(points[:, 0],
                   points[:, 1],
                   c='b',
                   s=5)

    def show_normals(self, points, normals, title="None") -> None:
        """点群と法線ベクトルを表示する関数.

        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num,
                                  projection='3d')
        self.graph_num += 1

        plt.title(title)
        ax.set(xlabel='x', ylabel='y', zlabel='z')

        # 点をプロット
        ax.scatter(points[:, 0], points[:, 1],
                   points[:, 2], c='b', marker='o', label='Points')

        # 法線ベクトルをプロット
        scale = 0.1  # 矢印のスケール
        for i in range(len(points)):
            if points[i, 0] < -0.05:  # 一部を表示
                ax.quiver(points[i, 0], points[i, 1], points[i, 2],
                          normals[i, 0]*scale, normals[i, 1]*scale, normals[i, 2]*scale, color='r', length=1.0, normalize=True)

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

        # 保存PLYパス
        ply_file_name = os.path.splitext(point_file_name)[0] + "_point.ply"
        save_point_path = os.path.join(self.ply_save_dir, ply_file_name)

        ply_file_name = os.path.splitext(point_file_name)[0] + ".ply"
        save_mesh_path = os.path.join(self.ply_save_dir, ply_file_name)

        """
        メイン処理
        """
        # 点群データの読み込み
        points = np.load(point_path)
        self.log.add(title="points.shape", log=points.shape)
        self.show_point(points, title="Input Point")  # グラフの追加

        # オブジェクトの向きを調整
        points = self.rotate_object(points, angle=-90, axis="z")
        self.show_point(points, title="Rotated Input Point")  # グラフに追加

        # NumPyの配列からPointCloudを作成
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        if Param.point_only and develop:
            o3d.io.write_point_cloud(save_point_path, point_cloud)

        """法線ベクトルの作成"""
        # 法線情報を計算
        point_cloud.estimate_normals(
            # search_param=o3d.geometry.KDTreeSearchParamHybrid(
            #     radius=1, max_nn=30)
        )
        # 法線ベクトルの編集(numpy配列に変換)
        normals = np.asarray(point_cloud.normals)
        # self.show_normals(points, normals, title="Normals")  # グラフの追加

        """法線ベクトルの編集"""
        if (Param.edit_normal and develop) or execute_web:
            if category == "0":
                self.log.add(title="Edit Mode", log="Airplane")
                edit = EditMeshAirplane(vectors_26=self.vectors_26,
                                        develop=develop,
                                        log=self.log)
            elif category == "1":
                self.log.add(title="Edit Mode", log="Chair")
                edit = EditMeshChair(vectors_26=self.vectors_26,
                                     develop=develop,
                                     log=self.log)
            else:
                raise Exception("Category Error")

            edited_normals, wing_points, correct_point = \
                edit.edit_normal(points, normals)

            if edited_normals is not None:
                self.log.add(title="Correct Normals", log="True")
                normals = edited_normals
            else:
                self.log.add(title="Correct Normals", log="False")

            if Param.work_process:
                if wing_points is not None:
                    self.show_point_2D(wing_points, title="2D")
                if correct_point is not None:
                    self.show_point(correct_point, title="Correct Point")

        # 編集後の法線ベクトルを表示
        # self.show_normals(points, normals, title="After Normals")

        # 点群や法線ベクトルの表示
        if Param.work_process and develop:
            if Param.output_image:
                save_path = os.path.join(WORK_DIR_PATH, 'result.png')
                plt.savefig(save_path)
            else:
                plt.show()

        """メッシュ作成"""
        point_cloud.normals = o3d.utility.Vector3dVector(normals)  # TODO

        # 法線の表示
        if Param.show_normal and develop:
            o3d.visualization.draw_geometries(
                [point_cloud], point_show_normal=True)

        # 三角形メッシュを計算する
        distances = point_cloud.compute_nearest_neighbor_distance()  # 近傍距離を計算
        avg_dist = np.mean(distances)  # 近傍距離の平均
        radius = 2*avg_dist  # 半径
        radii = [radius, radius * 2]  # [半径,直径]
        radii = o3d.utility.DoubleVector(radii)  # numpy配列 >> open3D形式
        recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            point_cloud, radii)

        # geometry.Geometry オブジェクトのリストを描画する関数(meshの表示)
        if Param.show_mesh and develop:
            # x: 右方向
            # y: 上
            # z: 手前
            o3d.visualization.draw_geometries([recMeshBPA])

        # 生成したメッシュをPLYファイルに保存
        o3d.io.write_triangle_mesh(save_mesh_path, recMeshBPA)

        return save_mesh_path


if __name__ == "__main__":
    import matplotlib

    if Param.output_image:
        matplotlib.use('Agg')
    else:
        # 最初は以下を実行する
        # $ sudo apt-get install python3-tk
        matplotlib.use('TKAgg')

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
        execute_time = time.time() - start
        ms.log.add(title="Execution time", log=str(execute_time)[:5]+"s")
    finally:
        ms.log.show()

    # 処理時間計測用

    print("終了")
