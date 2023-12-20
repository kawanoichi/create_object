import os
import cv2
import numpy as np

from param_create_surface import Param


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditMeshAirplane:
    def __init__(self, vectors_26, develop=False, log=None):
        self.vectors_26 = vectors_26
        self.develop = develop
        self.log = log  # ログ用

        # オブジェクトの正面方向
        self.front_vector = np.array([0, 0, -1])
        # オブジェクトの上方向
        self.upper_vector = np.array([0, 1, 0])
        self.upper_vector_index = np.where(
            (self.vectors_26 == self.upper_vector).all(axis=1))[0]

        # オブジェクトの下方向
        self.lower_vector = np.array([0, -1, 0])
        self.lower_vector_index = np.where(
            (self.vectors_26 == self.lower_vector).all(axis=1))[0]

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

    @staticmethod
    def rho_theta_to_line(rho, theta):
        """rho, thetaから傾きと切片を求める関数"""
        a = -np.cos(theta) / np.sin(theta)
        b = rho / np.sin(theta)
        return a, b

    def detect_wing(self, max_grope_points, normals):
        """Hough変換による羽を検知."""
        """
        ハフ変換
        """
        # 点群の座標は少数なので、座標も1000倍しないとだめ？
        img = np.zeros((1000, 1000), dtype=np.uint8)
        img += 255

        # 点群の画像を作成(正面)
        front_point_img = img.copy()
        for point in max_grope_points:
            x = int(point[0] * 1000) + 500
            y = int(point[1] * 1000) + 500
            cv2.circle(front_point_img, (x, y), 2, 0, -1)

        # 点群の画像を作成(上面)
        upper_point_img = img.copy()
        for point in max_grope_points:
            x = int(point[0] * 1000) + 500
            z = int(point[2] * 1000) + 500
            cv2.circle(upper_point_img, (x, z), 2, 0, -1)

        # 点群の画像を作成(横面)
        beside_point_img = img.copy()
        for point in max_grope_points:
            y = int(point[1] * 1000) + 500
            z = int(point[2] * 1000) + 500
            cv2.circle(beside_point_img, (y, z), 2, 0, -1)

        # 作業用
        if Param.work_process and Param.output_image and self.develop:
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'point_front.png'), front_point_img)
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'point_upper.png'), upper_point_img)
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'point_beside.png'), beside_point_img)

        # エッジ検出
        edges = cv2.Canny(front_point_img, 50, 150)

        # ハフ変換
        # NOTE: rho, theta = line
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=210)

        # 線が見つからない場合
        if lines is None:
            return None

        # 作業用: 検出したすべての線の表示
        if Param.work_process and Param.output_image and self.develop:
            detect_wing_img = front_point_img.copy()
            for rho, theta in lines.squeeze(axis=1):
                self.draw_line(detect_wing_img, theta, rho)
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'detect_line.png'), detect_wing_img)
            del detect_wing_img

        """
        重複している線を削除

        NOTE:
        rho : 直線の原点からの距離
        thre: 直線の法線との角度
        - 描画して確かめた感じ、threの数値が高いほうが水平な気がする
        """
        # lineを並び替え(rhoの小さい順に並び替え)
        lines_reshape = lines.reshape(lines.shape[0], lines.shape[2])
        new_line = lines_reshape[np.argsort(lines_reshape[:, 0])]

        """重なった線の削除"""
        thre_a = 10  # 傾きの閾値
        thre_b = 10  # 他の線の切片との差の閾値
        pre_b = 0  # 比較用切片(分かりやすいようにここで初期化)
        delete_index = []  # 削除するlineのindexを格納する
        detect_first_line = False  # 最初の飛行機の羽を表す線を見つけたかどうかのフラグ
        for i, line in enumerate(new_line):
            rho, theta = line
            a, b = self.rho_theta_to_line(rho, theta)  # 傾きと切片を求める
            a = round(a * (10 ** 8), 4)  # 値が小さいのでわかりやすいように補正
            if detect_first_line is False:
                if abs(a) < thre_a:
                    pre_b = b
                    detect_first_line = True
                else:
                    delete_index.append(i)
                    continue
            else:
                # 傾きが水平でない or 前の線と近い場合
                if abs(a) > thre_a or abs(pre_b - b) < thre_b:
                    delete_index.append(i)
                else:
                    pre_b = b

        # ラインの削除
        wing_line = np.delete(new_line, delete_index, 0)

        # 作業用: 検出した線の表示
        if Param.work_process and Param.output_image and self.develop:
            selected_line_img = front_point_img.copy()
            wing_line = wing_line.reshape(wing_line.shape[0], 1, 2)
            for rho, theta in wing_line.squeeze(axis=1):
                self.draw_line(selected_line_img, theta, rho)
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'detect_line_selected.png'), selected_line_img)
            wing_line = wing_line[:, 0, :]
            del selected_line_img
        return wing_line

    def edit_normal_pattern1(self, points, normals, wing_line):
        """法線ベクトルを編集する関数.
        lineが偶数本見つかった場合に、法線ベクトルを面ごとに交互(表裏)にする関数
        Args:
            points: オブジェクト(飛行機)の点群
            normals: 法線ベクトル
            wing_line: 飛行機の羽の位置を表す線
        Return:
            normals: 編集を行った法線ベクトル
        """
        thre = 10
        # x, y座標で考える
        count_line = np.array([0, 0, 0, 0])
        for i, point in enumerate(points):
            min_dis = 100
            min_line_index = 0
            for j, line in enumerate(wing_line):
                _, b = self.rho_theta_to_line(rho=line[0], theta=line[1])
                y = int(point[1] * 1000) + 500
                # bを1000から引いているのは座標と画像上の座標を合わせるため
                dis = abs(y - (1000 - b))  # 線と点の距離(y軸方向)
                if dis < min_dis:
                    min_dis = dis
                    min_line_index = j

            # ラインの切片と点のy座標を比較
            if min_dis < thre:
                count_line[min_line_index] += 1
                # 羽の上を補正
                if min_line_index % 2 == 0 and normals[i, 1] < 0:
                    normals[i, 1] *= -1
                # 羽の下
                elif min_line_index % 2 == 1 and normals[i, 1] > 0:
                    normals[i, 1] *= -1
        return normals

    def edit_normal_pattern2(self, points, normals):
        """法線ベクトルを編集する関数.
        lineが偶数本見つかった場合に、法線ベクトルを面ごとに交互(表裏)にする関数
        Args:
            points: オブジェクト(飛行機)の点群
            normals: 法線ベクトル
        Return:
            normals: 編集を行った法線ベクトル
        """
        for i, point in enumerate(points):
            # 縦向き(x軸方向)のベクトルに着目する
            if point[0] > 0 and normals[i, 0] < 0:
                normals[i, 0] *= -1
            elif point[0] < 0 and normals[i, 0] > 0:
                normals[i, 0] *= -1
            # 縦向き(y軸方向)のベクトルに着目する
            if point[1] > 0 and normals[i, 1] < 0:
                normals[i, 1] *= -1
            elif point[1] < 0 and normals[i, 1] > 0:
                normals[i, 1] *= -1
            # 縦向き(z軸方向)のベクトルに着目する
            if point[2] > 0 and normals[i, 2] < 0:
                normals[i, 2] *= -1
            elif point[2] < 0 and normals[i, 2] > 0:
                normals[i, 2] *= -1
        return normals

    def edit_normal(self, points: np.ndarray, normals=None) -> None:
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

        """点群を法線の向きでグループ分け"""
        # self.groupe: 法線が'self.vectors_26'の中で一番近いベクトルのインデックスを格納
        self.groupe = np.zeros(normals.shape[0])  # (2048,)
        for i, normal in enumerate(normals):
            min_theta = 180  # 比較するためのなす角
            for j, vector26 in enumerate(self.vectors_26):
                angle = int(self.angle_between_vectors(normal, vector26))
                if angle < min_theta:
                    self.groupe[i] = j
                    min_theta = angle

        """法線ベクトルの編集"""

        # 羽の部分の点群を取得
        wing_points_index = np.where(
            (self.groupe == self.upper_vector_index) |
            (self.groupe == self.lower_vector_index)
        )
        wing_points = points[wing_points_index]

        # 羽を検知 wing_line.shape: (線の本数, 2) ※2は[rho, theta]
        wing_line = self.detect_wing(wing_points, normals)

        # ラインが見つからない場合は、パターン２
        if wing_line is None:
            self.log.add(title="Correction", log="pattern2")
            normals = self.edit_normal_pattern2(points, normals)

        # ラインが見つかった場合は、パターン１
        elif wing_line.shape[0] % 2 == 0:
            self.log.add(title="Correction", log="pattern1")
            self.log.add(title="Detect Line", log=wing_line.shape[0])
            # (ラインの本数, 1, 2) >> (ラインの本数, 2)
            # wing_line = wing_line[:, 0, :]
            # 羽を表す点群の面が偶数枚ある場合、法線ベクトルの向きを交互にする
            normals = self.edit_normal_pattern2(points, normals)
            normals = self.edit_normal_pattern1(points, normals, wing_line)

        return normals, wing_points
