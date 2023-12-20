import os
import numpy as np
# import cv2

# from param_create_surface import Param

SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditMeshChair:
    def __init__(self, vectors_26, develop=False, log=None):
        self.vectors_26 = vectors_26
        self.develop = develop
        self.log = log  # ログ用

        # オブジェクトの正面方向
        self.front_vector = np.array([0, 0, 1])
        self.upper_vector_index = np.where(
            (self.vectors_26 == self.front_vector).all(axis=1))[0]
        # オブジェクトの上方向
        self.upper_vector = np.array([0, 1, 0])
        self.upper_vector_index = np.where(
            (self.vectors_26 == self.upper_vector).all(axis=1))[0]
        # オブジェクトの右方向
        self.right_vector = np.array([1, 0, 0])
        self.right_vector_index = np.where(
            (self.vectors_26 == self.right_vector).all(axis=1))[0]
        self.left_vector_index = np.where(
            (self.vectors_26 == (self.right_vector * -1)).all(axis=1))[0]

    @staticmethod
    def angle_between_vectors(vector_a, vector_b):
        """ベクトル間のなす角を求める関数.

        ベクトルAとベクトルBのなす角を求める.

        Args:
            vector_a: ベクトルA
            vector_b: ベクトルB
        Return:
            theta_deg: なす角
        """
        dot_product = np.dot(vector_a, vector_b)
        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        cos_theta = dot_product / (magnitude_a * magnitude_b)

        # acosはarccosine関数で、cosの逆関数です。
        theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        # 弧度法から度数法に変換
        return np.degrees(theta_rad)

    def correct_direct_outside(self, points, normals, vector_index_list, coordinate: str = "x"):
        """法線ベクトルを外側に向ける関数.
        Args:
            points: 点群座標
            normals: 法線ベクトル
            vector_index_list: 26方位のベクトルを比較
            coordinate: 外側に向ける座標軸
        """
        # 左右
        if coordinate == "x":
            condition1 = self.right_vector_index
            condition2 = self.left_vector_index
            coordinate_index = 0
        # 上下
        elif coordinate == "y":
            self.upper_vector = np.array([0, 1, 0])
            condition1 = self.right_vector_index
            condition2 = self.left_vector_index
            coordinate_index = 1
        # 前後
        elif coordinate == "z":
            self.front_vector = np.array([0, 0, 1])
            condition1 = self.right_vector_index
            condition2 = self.left_vector_index
            coordinate_index = 2
        else:
            raise ()

        target_index = np.where(
            (vector_index_list == condition1) | \
                (vector_index_list == condition2))[0]
        
        if len(target_index) == 0:
            return None
        
        # ベクトルの向きと座標の符号を比較し、修正
        count = 0
        for index in target_index:
            if points[index, coordinate_index] > 0 and \
                normals[index, coordinate_index] < 0:
                normals[index, coordinate_index] *= -1
                count += 1
            if points[index, coordinate_index] < 0 and \
                normals[index, coordinate_index] > 0:
                normals[index, coordinate_index] *= -1
                count += 1
        self.log.add(title=f"direct {coordinate} outside count", log=count)
        return normals
        
    def detect_face(self, points, normals):
        """面を検出する関数."""
        
        """作業中"""
        
        return normals
        

    def edit_normal(self, points: np.ndarray, normals=None) -> None:
        """法線ベクトルを修正する関数.
        Args:
            points: 点群座標
            normals: 法線ベクトル
        """
        """点群を法線の向きでグループ分け"""
        # vector_index_list: 法線が'self.vectors_26'の中で一番近いベクトルのインデックスを格納
        vector_index_list = np.zeros(normals.shape[0])  # (2048,)
        for i, normal in enumerate(normals):
            min_theta = 180  # 比較するためのなす角
            for j, vector26 in enumerate(self.vectors_26):
                angle = int(self.angle_between_vectors(normal, vector26))
                if angle < min_theta:
                    vector_index_list[i] = j
                    min_theta = angle
        
        """椅子の側面を修正"""
        # 左右方向の法線ベクトルを修正
        correct_normals = self.correct_direct_outside(
            points, normals, vector_index_list, coordinate="x")
        if correct_normals is not None:
            normals = correct_normals

        """椅子の面を見つけて編集する"""
        correct_normals = self.detect_face(points, normals)
        if correct_normals is not None:
            normals = correct_normals

        return normals, None
