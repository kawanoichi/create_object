import cv2
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

from image_processing import ImageProcessing as ImaP


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditMeshAirplane:
    def __init__(self, vectors_26):
        self.vectors_26 = vectors_26

    def angle_between_vectors(self, vector_a, vector_b):
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


    def edit_normals(self, points: np.ndarray, normals: np.ndarray) -> None:
        """法線ベクトルに関連する関数.

        Args:
            points(np.ndarray): 点群

        Variable:
            self.groupe:
                点群の座標のインデックスに関連して、
                26ベクトルの一番近いベクトルのインデックスを格納
        """
        # 点群を法線の向きでグループ分け
        # 似た方角を向いたベクトルをグループ分け
        self.groupe = np.zeros(normals.shape[0])
        for i, normal in enumerate(normals):
            min_theta = 180  # 比較するためのなす角
            for j, vector26 in enumerate(self.vectors_26):
                angle = int(self.angle_between_vectors(normal, vector26))
                if angle < min_theta:
                    self.groupe[i] = j
                    min_theta = angle

        # count_vector_classの作成
        # グループ分けされたベクトルの個数をカウントする
        self.count_vector_class = np.zeros(26)
        for i in range(self.vectors_26.shape[0]):
            self.count_vector_class[i] = \
                np.count_nonzero(self.groupe == i)
        print(f"self.count_vector_class:\n {self.count_vector_class}")

        # 最も多い要素を含むグループの点をグラフに追加
        vector_index = np.argmax(self.count_vector_class)
        max_grope_points = points[np.where(self.groupe == vector_index)]

        """
        ハフ変換
        """
        # 点群の座標は少数なので、座標も1000倍しないとだめ？
        img = np.zeros((1000, 1000), dtype=np.uint8)
        img += 255

        # 点群の画像を作成
        for point in max_grope_points:
            x = int(point[0] * 1000) + 500
            y = int(point[1] * 1000) + 500
            cv2.circle(img, (x, y), 2, 0, -1)

        point_img = img.copy()
        # save_path = os.path.join(DATA_DIR_PATH, 'zikken.png')
        # cv2.imwrite(save_path, point_img)

        # エッジ検出
        edges = cv2.Canny(img, 50, 150)

        # ハフ変換
        # NOTE: rho, theta = line
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=240)

        if lines is not None:
            for rho, theta in lines.squeeze(axis=1):
                ImaP.draw_line(img, theta, rho)
        else:
            print("Error: 線が見つかりません")
            return normals, max_grope_points, None

        save_path = os.path.join(WORK_DIR_PATH, 'zikken2.png')
        cv2.imwrite(save_path, img)

        """
        重複している線を削除
        """
        # lineを並び替え
        lines_reshape = lines.reshape(5, 2)
        new_line = lines_reshape[np.argsort(lines_reshape[:, 0])]

        pre_rho = 0
        thre = 10
        delete_index = []
        for i, line in enumerate(new_line):
            rho, theta = line
            if abs(pre_rho - rho) < thre:
                delete_index.append(i)
            pre_rho = rho

        new_line = np.delete(new_line, delete_index, 0)

        img = point_img.copy()

        if new_line is not None:
            new_line = new_line.reshape(new_line.shape[0], 1, 2)
            for rho, theta in new_line.squeeze(axis=1):
                ImaP.draw_line(img, theta, rho)
        else:
            print("Error: 線が見つかりません")
            return normals, max_grope_points, None

        save_path = os.path.join(WORK_DIR_PATH, 'zikken3.png')
        cv2.imwrite(save_path, img)

        """
        点群の割り当て
        - 一枚のラインずつみていく？
        """
        thre = 10
        classed_points = np.zeros((1, 3))

        for i, point in enumerate(points):
            point2 = point * 1000 + 500
            if abs(point2[0] - new_line[0, 0, 0]) < thre:
                # lineを構成する座標を抽出
                classed_points = np.vstack((classed_points, point))
                # 法線ベクトルの修正(逆にする)
                normals[i] *= -1
            if abs(point2[0] - new_line[2, 0, 0]) < thre:
                # 法線ベクトルの修正(逆にする)
                normals[i] *= -1
        classed_points = classed_points[1:]

        return normals, max_grope_points, classed_points
