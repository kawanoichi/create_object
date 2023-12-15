import cv2
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os
# import matplotlib


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditMeshAirplane:
    def __init__(self, vectors_26):
        self.vectors_26 = vectors_26

        # オブジェクトの正面方向
        self.front_vector = np.array([0, 0, -1])
        # オブジェクトの上方向
        self.upper_vector = np.array([0, 0, -1])
        # オブジェクトの下方向
        self.lower_vector = np.array([0, 0, -1])

    @staticmethod
    def draw_line(img, theta, rho):
        h, w = img.shape[:2]
        if np.isclose(np.sin(theta), 0):
            x1, y1 = rho, 0
            x2, y2 = rho, h
        else:
            def calc_y(x): return rho / np.sin(theta) - \
                x * np.cos(theta) / np.sin(theta)
            x1, y1 = 0, calc_y(0)
            x2, y2 = w, calc_y(w)

        # float -> int
        x1, y1, x2, y2 = list(map(int, [x1, y1, x2, y2]))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

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

    def edit_normals2(self, points: np.ndarray, normals: np.ndarray) -> None:
        # def edit_normals(self, points: np.ndarray, normals: np.ndarray) -> None:
        """法線ベクトルに関連する関数.

        Args:
            points(np.ndarray): 点群

        Variable:
            self.groupe:
                点群の座標のインデックスに関連して、
                26ベクトルの一番近いベクトルのインデックスを格納
        """
        theta_thre = 50
        groupe_upper = points[np.where(
            self.angle_between_vectors(normals, self.upper_vector) < theta_thre)]
        print(f"groupe_upper.shape: {groupe_upper.shape}")

        groupe_lower = points[np.where(
            self.angle_between_vectors(normals, self.lower_vector) < theta_thre)]
        print(f"groupe_lower.shape: {groupe_lower.shape}")

        grope_wings_points = points[np.where(
            (self.angle_between_vectors(normals, self.upper_vector) < theta_thre) |
            (self.angle_between_vectors(normals, self.lower_vector) < theta_thre)
        )]

        print(f"grope_wings_points.shape: {grope_wings_points.shape}")

        return normals, grope_wings_points, None

    def edit_normals3(self, points: np.ndarray, normals: np.ndarray) -> None:
        # def edit_normals2(self, points: np.ndarray, normals: np.ndarray) -> None:
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
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=140)

        if lines is not None:
            # pass
            for rho, theta in lines.squeeze(axis=1):
                self.draw_line(img, theta, rho)
        else:
            print("Error: 線が見つかりません")
            return normals, max_grope_points, None

        save_path = os.path.join(WORK_DIR_PATH, 'zikken2.png')
        cv2.imwrite(save_path, img)

        """
        重複している線を削除
        """
        # lineを並び替え
        # print("lines\n", lines[0, 0])

        print(f"lines.shape: {lines.shape}")
        lines_reshape = lines.reshape(lines.shape[0], lines.shape[2])
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
                self.draw_line(img, theta, rho)
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

    def edit_normals(self, points: np.ndarray, normals=None) -> None:
        """法線ベクトルに関連する関数.

        Args:
            points(np.ndarray): 点群

        Variable:
            self.groupe:
                点群の座標のインデックスに関連して、
                26ベクトルの一番近いベクトルのインデックスを格納
        """
        if normals is None:
            normals = np.asarray(points.normals)

        # グラフの追加
        # self.show_normals(points, normals, title="Normals")

        """
        点群を法線の向きでグループ分け
        """
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
        # self.show_point(max_grope_points, title="points of many vector groupe")
        # print(
        #     f"self.vectors_26[vector_index]: {self.vectors_26[vector_index]}")

        # self.show_point_2D(max_grope_points, title="2D")

        # ベクトルの符号を逆にしてみる
        # invert_some_normals = normals.copy()
        # invert_some_normals[np.where(self.groupe == vector_index)] *= -1
        # self.show_normals(points, invert_some_normals, title="invert vector")

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
        save_path = os.path.join(WORK_DIR_PATH, 'zikken.png')
        cv2.imwrite(save_path, point_img)

        # エッジ検出
        edges = cv2.Canny(img, 50, 150)

        # ハフ変換
        # NOTE: rho, theta = line
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)

        if lines is not None:
            for rho, theta in lines.squeeze(axis=1):
                self.draw_line(img, theta, rho)
        else:
            print("Error: 線が見つかりません")
            return normals, None, None

        save_path = os.path.join(WORK_DIR_PATH, 'zikken2.png')
        cv2.imwrite(save_path, img)

        """
        重複している線を削除
        """
        # lineを並び替え
        lines_reshape = lines.reshape(lines.shape[0], lines.shape[2])
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
                self.draw_line(img, theta, rho)
        else:
            print("Error: 線が見つかりません")
            return normals, None, None

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

        # self.show_point(classed_points, title="Part of wing")

        return normals, max_grope_points, classed_points