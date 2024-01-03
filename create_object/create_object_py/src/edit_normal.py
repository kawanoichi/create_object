import os
import cv2
import numpy as np
from enum import Enum

# from param_create_surface import Param
from edit_normal_method import EditNormalMethod
from calculator import Calculator


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class Coordinate(Enum):
    """座標クラス."""
    X = 0
    Y = 1
    Z = 2


class EditNormal:
    def __init__(self, vectors_26, develop=False, log=None):
        self.vectors_26 = vectors_26
        self.develop = develop
        self.log = log  # ログ用

        self.edit_normal = EditNormalMethod(vectors_26=self.vectors_26,
                                            develop=self.develop,
                                            log=self.log)

    def airplane(self, points, normals, vector_index_list):
        """飛行機の法線ベクトルを修正"""
        # 側面の画像を描画する
        img = self.edit_normal.draw_point_cloud_axes(
            points, vector_index_list, coordi_index=Coordinate.X.value)

        # 側面から線(面)を出力する
        _, vertical_line, horizontal_line = self.edit_normal.detect_line(
            img, coordi_index=Coordinate.X.value)

        # 側面方向に見ていく(椅子の背もたれの面のベクトル方向はZ)
        correct_normals, correct_normal_index = self.edit_normal.inversion_normal(
            points, normals, vertical_line, vector_index_list, face_axis=Coordinate.Z.value)
        if correct_normals is None:
            return normals, None
        else:
            normals = correct_normals

        # 椅子の座る部分の面を見つけて法線ベクトルの補正を加える
        correct_normals, correct_normal_index = self.edit_normal.inversion_normal(
            points, normals, horizontal_line, vector_index_list, face_axis=Coordinate.Y.value)

        if correct_normal_index is not None:
            correct_point = points[correct_normal_index]

        return normals, correct_point

    def chair(self, points, normals, vector_index_list):
        """椅子の法線ベクトルを修正"""
        # 側面の画像を描画する
        img = self.edit_normal.draw_point_cloud_axes(
            points, vector_index_list, coordi_index=Coordinate.X.value)

        # 側面から線(面)を出力する
        _, vertical_line, horizontal_line = self.edit_normal.detect_line(
            img, coordi_index=Coordinate.X.value)

        # 側面方向に見ていく(椅子の背もたれの面のベクトル方向はZ)
        correct_normals, correct_normal_index = self.edit_normal.inversion_normal(
            points, normals, vertical_line, vector_index_list, face_axis=Coordinate.Z.value)
        if correct_normals is None:
            return normals, None
        else:
            normals = correct_normals

        # 椅子の座る部分の面を見つけて法線ベクトルの補正を加える
        correct_normals, correct_normal_index = self.edit_normal.inversion_normal(
            points, normals, horizontal_line, vector_index_list, face_axis=Coordinate.Y.value)

        if correct_normal_index is not None:
            correct_point = points[correct_normal_index]

        return normals, correct_point

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
        vector_index_list = np.zeros(normals.shape[0], dtype=int)  # (2048,)
        count_list = np.zeros(self.vectors_26.shape[0], dtype=int)  # 確認用
        for i, normal in enumerate(normals):
            min_theta = 180  # 比較するためのなす角
            min_index = 0  # 確認用
            for j, vector26 in enumerate(self.vectors_26):
                angle = int(Calculator.angle_between_vectors(normal, vector26))
                if angle < min_theta:
                    vector_index_list[i] = j
                    min_theta = angle
                    min_index = j  # 確認用
            count_list[min_index] += 1  # 確認用

        """椅子の側面を修正"""

        # 横方向(x軸方向)を向いた法線ベクトルを外側に向ける
        correct_normals = self.edit_normal.correct_direct_outside(
            points, normals, vector_index_list, coordi_index=Coordinate.X.value)
        correct_normals = self.edit_normal.correct_direct_outside(
            points, correct_normals, vector_index_list, coordi_index=Coordinate.Y.value)
        if correct_normals is not None:
            normals = correct_normals

        if category == "0":
            normals, correct_point = self.airplane(
                work_points, normals, vector_index_list)
        elif category == "1":
            normals, correct_point = self.chair(work_points, normals, vector_index_list)
        else:
            raise Exception("Category ID Error")

        return normals, None, correct_point