import os
import cv2
import numpy as np

# from param_create_surface import Param
from edit_normal_method import EditNormalMethod
from calculator import Calculator
from coordinate import Coordinate


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditNormal:
    def __init__(self, vectors_26, develop=False, log=None):
        self.vectors_26 = vectors_26
        self.develop = develop
        self.log = log  # ログ用

        self.edit_normal = EditNormalMethod(vectors_26=self.vectors_26,
                                            develop=self.develop,
                                            log=self.log)

    def correct_process1(self, points, normals, vector_index_list,
                         X=True, Y=True, Z=True):
        """法線ベクトル修正処理１.
        法線ベクトルを外側に向ける
        """
        if X:
            self.edit_normal.correct_direct_outside(
                points, normals, vector_index_list,
                coordi_index=Coordinate.X.value, symmetry="line")
        if Y:
            self.edit_normal.correct_direct_outside(
                points, normals, vector_index_list,
                coordi_index=Coordinate.Y.value, symmetry="line")
        if Z:
            self.edit_normal.correct_direct_outside(
                points, normals, vector_index_list,
                coordi_index=Coordinate.Z.value, symmetry="line")

    def correct_process2(self, points, normals, vector_index_list,
                         coordi_index=Coordinate.X.value, line_thre=100,
                         execute_vertical=True, execute_horizonta=True):
        """法線ベクトル修正処理２.
        法線ベクトルを外側に向ける
        """
        # 側面の画像を描画する
        img = self.edit_normal.draw_point_cloud_axes(
            points, vector_index_list, coordi_index, all_point=True)

        # ライン(面)を検出
        _, vertical_line, horizontal_line = self.edit_normal.detect_line(
            img, line_thre)

        if len(vertical_line) > 0 and execute_vertical is True:
            self.edit_normal.inversion_normal(points, normals, vertical_line,
                                              vector_index_list, Coordinate.Z.value)
        if len(horizontal_line) > 0 and execute_horizonta is True:
            self.edit_normal.inversion_normal(points, normals, horizontal_line,
                                              vector_index_list, Coordinate.Y.value)

    def correct_process3(self, points, normals):
        """法線ベクトル修正処理３.
        端の座標の点の法線ベクトルを外側に向ける
        """
        self.edit_normal.correct_edge_point(
            points, normals, Coordinate.X.value)
        self.edit_normal.correct_edge_point(
            points, normals, Coordinate.Y.value)
        self.edit_normal.correct_edge_point(
            points, normals, Coordinate.Z.value)

    def main(self, category: str, points: np.ndarray, normals=None) -> None:
        """法線ベクトルを修正する関数.
        Args:
            category: オブジェクトカテゴリ
            points: 点群座標
            normals: 法線ベクトル
        """

        # 値が少数なので処理しやすいように正規化
        work_points = points * 1000
        work_points = np.floor(work_points).astype(int)

        """点群を法線の向きでグループ分け"""
        # vector_index_list: 26方位に法線ベクトルをグループ分け
        #                    グループ分けした26方位のインデックスを格納
        vector_index_list = np.zeros(
            normals.shape[0], dtype=int)  # (2048,)
        count_list = np.zeros(self.vectors_26.shape[0], dtype=int)  # 確認用
        for i, normal in enumerate(normals):
            min_theta = 180  # 比較するためのなす角
            min_index = 0  # 確認用
            for j, vector26 in enumerate(self.vectors_26):
                angle = int(
                    Calculator.angle_between_vectors(normal, vector26))
                if angle < min_theta:
                    vector_index_list[i] = j
                    min_theta = angle
                    min_index = j  # 確認用
            count_list[min_index] += 1  # 確認用

        # 飛行機
        if category == "0":
            # True False
            self.correct_process1(points, normals, vector_index_list,
                                  X=True, Y=False, Z=False)
            # self.correct_process2(work_points, normals, vector_index_list,
            #                       coordi_index=Coordinate.Z.value,
            #                       line_thre=140,
            #                       execute_vertical=False, execute_horizonta=True)
            # self.correct_process3(work_points, normals)

        # 椅子
        elif category == "1":
            # True False
            self.correct_process1(points, normals, vector_index_list,
                                  X=True, Y=True, Z=True)
            self.correct_process2(work_points, normals, vector_index_list,
                                  coordi_index=Coordinate.X.value,
                                  line_thre=110,
                                  execute_vertical=True, execute_horizonta=True)
            self.correct_process3(work_points, normals)
        else:
            raise Exception("Category Error")

        return normals
