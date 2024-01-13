import os
import cv2
import numpy as np
import json

from edit_normal_method import EditNormalMethod
from calculator import Calculator
from coordinate import Coordinate
from my_plt import MyPlt


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditNormal:
    def __init__(self, log=None,
                 vectors_26_path=os.path.join(SCRIPT_DIR_PATH, "vector26.npy")):
        # パラメータ読み込み
        self.read_param(os.path.join(SCRIPT_DIR_PATH, 'param.json'))
        self.vectors_26 = np.load(vectors_26_path)
        if self.show_vector26:
            MyPlt.show_vector(self.vectors_26)

        # ログ用
        self.log = log
        self.edit_normal = EditNormalMethod(vectors_26=self.vectors_26,
                                            log=self.log)

        self.call_count_pro2 = 0

    def read_param(self, json_path):
        """パラメータを読み込む関数."""
        with open(json_path, 'r') as json_file:
            Param = json.load(json_file)
        # 開発用
        self.develop = Param["develop"]
        # 26種のベクトルを表示
        self.show_vector26 = Param["show_vector26"] * self.develop
        # 開発過程の作成
        self.edit_process = Param["edit_process"] * self.develop
        # 開発過程の表示
        self.show_edit_process = Param["show_edit_process"] * self.develop

        if self.show_edit_process or not self.develop or not Param["save_edit_image"]:
            # self.show_edit_processがTrueなら保存できない
            self.save_edit_image = False
        else:
            # 開発過程を画像として保存(表示はできない)
            self.save_edit_image = Param["save_edit_image"]

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
        self.call_count_pro2 += 1
        # 側面の画像を描画する
        point_img = self.edit_normal.draw_point_cloud_axes(
            points, vector_index_list, coordi_index, all_point=True)

        # ライン(面)を検出
        line_img, selected_line_img, \
            vertical_line, horizontal_line = self.edit_normal.detect_line(
                point_img, line_thre)

        if self.save_edit_image:
            if point_img is not None:
                path = os.path.join(
                    WORK_DIR_PATH, f"point_img_{self.call_count_pro2}.png")
                cv2.imwrite(path, point_img)
            if line_img is not None:
                path = os.path.join(
                    WORK_DIR_PATH, f"detect_line_{self.call_count_pro2}.png")
                cv2.imwrite(path, line_img)
            if selected_line_img is not None:
                path = os.path.join(
                    WORK_DIR_PATH, f"selected_line_{self.call_count_pro2}.png")
                cv2.imwrite(path, selected_line_img)
        if vertical_line is not None:
            if len(vertical_line) > 0 and execute_vertical is True:
                self.edit_normal.inversion_normal(points, normals, vertical_line,
                                                  vector_index_list, Coordinate.Z.value)
        if horizontal_line is not None:
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
                                  X=True, Y=True, Z=True)
            self.correct_process2(work_points, normals, vector_index_list,
                                  coordi_index=Coordinate.Z.value,
                                  line_thre=140,
                                  execute_vertical=False, execute_horizonta=True)
            self.correct_process3(work_points, normals)

        # 椅子
        elif category == "1":
            # True False
            # self.correct_process1(points, normals, vector_index_list,
            #                       X=True, Y=True, Z=True)
            # self.correct_process2(work_points, normals, vector_index_list,
            #                       coordi_index=Coordinate.X.value,
            #                       line_thre=120,
            #                       execute_vertical=True, execute_horizonta=True)
            self.correct_process2(work_points, normals, vector_index_list,
                                  coordi_index=Coordinate.Z.value,
                                  line_thre=120,
                                  execute_vertical=True, execute_horizonta=True)
            # self.correct_process3(work_points, normals)
        else:
            raise Exception("Category Error")

        if self.show_edit_process:
            self.edit_normal.show_work_process()

        return normals
