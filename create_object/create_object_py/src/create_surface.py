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
from edit_mesh_table import EditMeshTable
from edit_mesh_airplane import EditMeshAirplane
# import rotate_coordinate as rotate
from param_create_surface import Param

import cv2
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
# 最初は以下を実行する
# $ sudo apt-get install python3-tk
matplotlib.use('TKAgg')
# matplotlib.use('Agg')
# from sklearn.linear_model import RANSACRegressor


class MakeSurface:
    """点群から表面を作りplyファイルに保存するクラス."""

    def __init__(self,
                 point_dir,
                 ply_save_dir) -> None:
        """コンストラクタ.

        Args:
            point_file (str): 点群ファイル(.npy)
        """
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
        self.vectors_26 = self.vector_26()

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
            raise Exception(f"Error :Not exist '{path}'")

    def vector_26(self):
        """26方位ベクトル作成関数."""
        kinds_of_coodinate = [-1, 0, 1]

        # 26方位のベクトル(終点座標)を作成
        vectors_26 = np.array([])
        for x in kinds_of_coodinate:
            for y in kinds_of_coodinate:
                for z in kinds_of_coodinate:
                    if not x == y == z == 0:
                        append_coordinate = np.array([x, y, z])
                        vectors_26 = np.append(
                            vectors_26, append_coordinate, axis=0)
        vectors_26 = vectors_26.reshape(
            (len(kinds_of_coodinate) ^ 3)-1, 3)
        return vectors_26

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

        ax.set(xlabel='x', ylabel='z', zlabel='y')
        ax.scatter(points[:, 0],
                   points[:, 2],
                   points[:, 1],
                   c='b')

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

    def main(self, point_file_name, category=0) -> None:
        """点群をメッシュ化し、表示する関数."""

        """
        パス設定
        """
        # 入力点群パス
        point_path = os.path.join(self.point_dir, point_file_name)
        self.check_exist(point_path)

        # 保存PLYパス
        ply_file_name = os.path.splitext(point_file_name)[0] + ".ply"
        save_ply_path = os.path.join(self.ply_save_dir, ply_file_name)

        """
        メイン処理
        """
        # 点群データの読み込み
        points = np.load(point_path)

        print(f"points.shape: {points.shape}")

        # グラフの追加
        self.show_point(points, title="Input Point")

        # オブジェクトの向きを調整
        points = self.rotate_object(points, angle=-90, axis="z")

        # グラフに追加
        self.show_point(points, title="Rotated Input Point")

        # NumPyの配列からPointCloudを作成
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

        # 法線情報を計算
        point_cloud.estimate_normals()

        # 法線ベクトルの編集(numpy配列に変換)
        normals = np.asarray(point_cloud.normals)

        # グラフの追加
        self.show_normals(points, normals, title="Normals")

        """法線ベクトルの作成・編集 (Airplane)"""
        if category == 0 and Param.edit_normal:
            airplane = EditMeshAirplane(vectors_26=self.vectors_26)
            normals, max_grope_points, classed_points = \
                airplane.edit_normals(points, normals)
            if classed_points is not None:
                self.show_point_2D(max_grope_points, title="2D")
            
            if classed_points is not None:
                self.show_point(classed_points, title="Part of wing")


        """法線ベクトルの作成・編集 (Table)"""
        if category == 1 and Param.edit_normal:
            table = EditMeshTable(vectors_26=self.vectors_26)
            normals = table.edit_normals(points, normals)

        # 編集後の法線ベクトルを表示
        self.show_normals(points, normals, title="After Normals")

        # 点群や法線ベクトルの表示
        if Param.work_process:
            plt.show()
            save_path = os.path.join(WORK_DIR_PATH, 'result.png')
            plt.savefig(save_path)

        """mesh作成"""
        # 新しい法線ベクトルの代入
        point_cloud.normals = o3d.utility.Vector3dVector(normals)

        # 近傍距離を計算
        distances = point_cloud.compute_nearest_neighbor_distance()

        # 法線の表示
        if Param.show_normal:
            o3d.visualization.draw_geometries(
                [point_cloud], point_show_normal=True)

        # 近傍距離の平均
        avg_dist = np.mean(distances)

        # 半径
        radius = 2*avg_dist

        # [半径,直径]
        radii = [radius, radius * 2]

        # o3d.utility.DoubleVector:numpy配列をopen3D形式に変換
        radii = o3d.utility.DoubleVector(radii)

        # 三角形メッシュを計算する
        recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            point_cloud, radii)

        # geometry.Geometry オブジェクトのリストを描画する関数(meshの表示)
        if Param.show_mesh:
            # x: 右方向
            # y: 上
            # z: 手前
            o3d.visualization.draw_geometries([recMeshBPA])

        # 生成したメッシュをPLYファイルに保存
        o3d.io.write_triangle_mesh(save_ply_path, recMeshBPA)

        return save_ply_path


if __name__ == "__main__":
    import time
    start = time.time()

    SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
    WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")

    massages = []
    massages.append(f"SCRIPT_DIR_PATH  : {SCRIPT_DIR_PATH}")
    massages.append(f"PROJECT_DIR_PATH : {PROJECT_DIR_PATH}")
    massages.append(f"WORK_DIR_PATH    : {WORK_DIR_PATH}")

    max_length = max(len(massage) for massage in massages)
    line = "_" * max_length

    # 設定の出力
    print(line)
    for massage in massages:
        print(massage)
    print(line)

    # file_name = "airplane.npy"
    file_name = "two_wings_1.npy"

    ms = MakeSurface(point_dir=WORK_DIR_PATH,
                     ply_save_dir=WORK_DIR_PATH)

    ms.main(file_name)

    # 処理時間計測用
    execute_time = time.time() - start
    print(f"実行時間: {str(execute_time)[:5]}s")

    print("終了")
