import os
import numpy as np
from enum import Enum
import cv2
from itertools import cycle

from param_create_surface import Param
from calculator import Calculator

SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class Coordinate(Enum):
    """座標クラス."""
    X = 0
    Y = 1
    Z = 2


class EditMeshChair:
    def __init__(self, vectors_26, develop=False, log=None):
        self.vectors_26 = vectors_26
        self.develop = develop
        self.log = log  # ログ用

        # オブジェクトの正面方向
        self.front_vector = np.array([0, 0, 1])
        self.front_vector_index = np.where(
            (self.vectors_26 == self.front_vector).all(axis=1))[0]
        self.back_vector_index = np.where(
            (self.vectors_26 == (self.front_vector * -1)).all(axis=1))[0]

        # オブジェクトの上方向
        self.upper_vector = np.array([0, 1, 0])
        self.upper_vector_index = np.where(
            (self.vectors_26 == self.upper_vector).all(axis=1))[0]
        self.lower_vector_index = np.where(
            (self.vectors_26 == (self.upper_vector * -1)).all(axis=1))[0]

        # オブジェクトの右方向
        self.right_vector = np.array([1, 0, 0])
        self.right_vector_index = np.where(
            (self.vectors_26 == self.right_vector).all(axis=1))[0][0]
        self.left_vector_index = np.where(
            (self.vectors_26 == (self.right_vector * -1)).all(axis=1))[0][0]

    def correct_direct_outside(self, points, normals, vector_index_list, coordi_index: int):
        """法線ベクトルを外側に向ける関数.
        Args:
            points: 点群座標
            normals: 法線ベクトル
            vector_index_list: 26方位のベクトルを比較
            coordi_index: 外側に向ける座標軸
        """
        # 左右
        if coordi_index == Coordinate.X.value:
            condition1 = self.right_vector_index
            condition2 = self.left_vector_index
        # 上下
        elif coordi_index == Coordinate.Y.value:
            condition1 = self.upper_vector_index
            condition2 = self.lower_vector_index
        # 前後
        elif coordi_index == Coordinate.Z.value:
            condition1 = self.front_vector_index
            condition2 = self.back_vector_index
        else:
            raise ()

        target_index = np.where(
            (vector_index_list == condition1) |
            (vector_index_list == condition2))[0]

        if len(target_index) == 0:
            return None

        # ベクトルの向きと座標の符号を比較し、修正
        count = 0
        for index in target_index:
            if points[index, coordi_index] > 0 and \
                    normals[index, coordi_index] < 0:
                # normals[index, coordi_index] *= -1
                normals[index] *= -1
                count += 1
            if points[index, coordi_index] < 0 and \
                    normals[index, coordi_index] > 0:
                # normals[index, coordi_index] *= -1
                normals[index] *= -1
                count += 1
        self.log.add(title=f"direct {coordi_index} outside count", log=count)
        return normals

    def draw_point_cloud_axes(self, points, vector_index_list, coordi_index: int):
        """各座標軸に対して描画する関数."""

        # それぞれの軸の最大値を求めていく
        if coordi_index == Coordinate.X.value:
            max_y = abs(np.max(points[:, 1]))
            min_y = abs(np.min(points[:, 1]))
            max_z = abs(np.max(points[:, 2]))
            min_z = abs(np.min(points[:, 2]))
            max_value = np.max(np.array([max_y, min_y, max_z, min_z]))
        elif coordi_index == Coordinate.Y.value:
            max_x = abs(np.max(points[:, 0]))
            min_x = abs(np.min(points[:, 0]))
            max_z = abs(np.max(points[:, 2]))
            min_z = abs(np.min(points[:, 2]))
            max_value = np.max(np.array([max_x, min_x, max_z, min_z]))
        elif coordi_index == Coordinate.Z.value:
            max_x = abs(np.max(points[:, 0]))
            min_x = abs(np.min(points[:, 0]))
            max_y = abs(np.max(points[:, 1]))
            min_y = abs(np.min(points[:, 1]))
            max_value = np.max(np.array([max_x, min_x, max_y, min_y]))
        else:
            raise Exception("Error")

        # 最大の位を繰り上げ(例: 1234 -> 2000, 12345 -> 20000)
        new_max_place = str(int(str(max_value)[0]) + 1)
        new_max_value = int(new_max_place + "0"*len(str(max_value)[1:]))

        # 白画像を作成
        img_size = new_max_value*2
        img = np.zeros((img_size, img_size, 3), dtype=np.uint8) + 255

        # 点群の原点を画像の中心に合わせる
        points += int(img_size/2)

        # NOTE: img[y,x]に注意
        # 側面画像
        correct_value = 2
        if coordi_index == Coordinate.X.value:
            for point, vec_index in zip(points, vector_index_list):
                if vec_index == self.right_vector_index or \
                        vec_index == self.left_vector_index:
                    continue
                _, y, z = point
                # 点を描画
                img[y-correct_value:y+correct_value,
                    z-correct_value:z+correct_value] = [0, 0, 0]
            img_name = "beside_yz.png"
        # 上面画像
        elif coordi_index == Coordinate.Y.value:
            for point, vec_index in zip(points, vector_index_list):
                if vec_index == self.upper_vector_index or \
                        vec_index == self.lower_vector_index:
                    continue
                x, _, z = point
                # 点を描画
                img[z-correct_value:z+correct_value,
                    x-correct_value:x+correct_value] = [0, 0, 0]
            img_name = "upper_zx.png"
        # 正面画像
        elif coordi_index == Coordinate.Z.value:
            for point, vec_index in zip(points, vector_index_list):
                if vec_index == self.front_vector_index or \
                        vec_index == self.back_vector_index:
                    continue
                x, y, _ = point
                # 点を描画
                img[y-correct_value:y+correct_value,
                    x-correct_value:x+correct_value] = [0, 0, 0]
            img_name = "front_yx.png"
        else:
            raise ()

        self.log.add(title="Line Image Name", log=img_name)
        if Param.work_process and Param.output_image and self.develop:
            cv2.imwrite(os.path.join(WORK_DIR_PATH, img_name), img)

        return img

    def detect_line(self, img, coordi_index):
        """線を検出する関数.
        Args:
            img: 点群を描画した画像
        """

        """ライン検出"""
        print(f"img.shape: {img.shape}")

        # エッジ検出
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        reversed_gray = cv2.bitwise_not(gray)
        cv2.imwrite(os.path.join(WORK_DIR_PATH, 'bitwise.png'), reversed_gray)

        # 線分検出
        if coordi_index == Coordinate.X.value:
            # 参考: https://way2se.ringtrees.com/py_cv2-004/#toc7
            lines = cv2.HoughLinesP(reversed_gray, rho=1,
                                    theta=np.pi/360, threshold=160,
                                    minLineLength=int(img.shape[0]*0.25), maxLineGap=200)
            lines = lines[:, 0, :]
        else:
            raise

        # 線が見つからない場合
        if lines is None:
            if Param.work_process and Param.output_image and self.develop:
                detect_line_img = img.copy()
                cv2.imwrite(os.path.join(WORK_DIR_PATH,
                            'detect_line.png'), detect_line_img)
            self.log.add(title="Detect lines", log="None")  # ログ
            return None
        self.log.add(title="Detect lines", log=lines.shape)  # ログ

        # 作業用: 検出したすべての線の表示
        if Param.work_process and Param.output_image and self.develop:
            detect_line_img = img.copy()
            # 描画
            for line in lines:
                x1, y1, x2, y2 = line
                cv2.line(detect_line_img, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'detect_line.png'), detect_line_img)
            del detect_line_img

        """
        重複している線を削除

        NOTE:
        x1, y1, x2, y2 = line
        - 描画して確かめた感じ、threの数値が高いほうが水平な気がする
        """
        # x1に関して小さい順にソート
        lines = lines[np.argsort(lines[:, 0])]

        delete_index = []
        vertical_line_index = []
        horizontal_line_index = []

        diff_a_thre = 20  # 傾き(度数法)の閾値
        diff_coordi_thre = int(img.shape[0] / 50)  # x1座標の閾値
        dis_thre = 20  # 直線と点の距離の閾値
        for i, line in enumerate(lines):
            if i == 0:
                pre_line = line
            else:
                # 傾きの角度を比較
                condition1 = int(
                    abs(Calculator.calculate_slope(line)-Calculator.calculate_slope(pre_line))) < diff_a_thre
                # ライン同士の距離で比較
                condition2 = Calculator.distance_point_to_line(pre_line, line[:2]) < dis_thre\
                    and Calculator.distance_point_to_line(pre_line, line[2:]) < dis_thre
                if condition1 and condition2:
                    delete_index.append(i)
                    continue
                else:
                    pre_line = line
            # ラインが水平か垂直かで分類
            if Calculator.calculate_slope(line) > 45:  # 縦
                vertical_line_index.append(i)
            else:  # 横
                horizontal_line_index.append(i)

        # ラインの削除
        vertical_line = lines[vertical_line_index]
        horizontal_line = lines[horizontal_line_index]
        lines = np.delete(lines, delete_index, 0)
        self.log.add(title="Vertical lines", log=vertical_line.shape)  # ログ
        self.log.add(title="Horizontal lines", log=horizontal_line.shape)  # ログ
        self.log.add(title="Mearged Detect lines", log=lines.shape)  # ログ

        if Param.work_process and Param.output_image and self.develop:
            # 結果を表示
            detect_line_img = img.copy()
            colors = cycle([(0, 0, 255), (0, 255, 0),
                           (255, 0, 0)])  # (B, G, R)
            for line in lines:
                x1, y1, x2, y2 = line
                color = next(colors)
                cv2.line(detect_line_img, (x1, y1), (x2, y2), color, 5)
            # x1の閾値の幅の確認
            detect_line_img[:, 50:52] = [0, 0, 255]
            detect_line_img[:, 50+diff_coordi_thre:52 +
                            diff_coordi_thre] = [0, 0, 255]
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'detect_line2.png'), detect_line_img)

        return lines, vertical_line, horizontal_line

    def reverse_vector(self, normal, vector_26_index):
        try:
            vector = self.vectors_26[vector_26_index]
            # vector = self.vectors_26[int(vector_26_index)]
            reversed_vector = normal.copy()
            for i, element in enumerate(vector):
                if element != 0:
                    reversed_vector[i] *= -1
        except Exception as e:
            print(e)
            print(f"normal: {normal}")
            print(f"vector_26_index: {vector_26_index}")
            exit()

        return reversed_vector

    def inversion_normal(self, points, normals, lines, vector_index_list, face_axis):
        """面(線)の本数によって法線ベクトルを修正.
        Args:
            lines: 面を表す線
            vector_index_list: 26方位に分類したときのindexを格納した配列
            face_axis: 面面を表す法線ベクトルの座標系 ※0(x) or 1(y) or 2(z)
        """
        if lines.shape[0] % 2 != 0:
            self.log.add(title="Invert Normal Executed", log="False")
            return None, None

        lines = lines[np.argsort(lines[:, 0])]
        if face_axis == Coordinate.X.value:
            raise ()

        if face_axis == Coordinate.Y.value:
            line_axis = 1  # 画像上x座標が小さい方向ベクトル x or y (0 or 1)
            target_posi_vec_index = np.where(
                self.vectors_26[:, face_axis] == 1)[0]
            target_nega_vec_index = np.where(
                self.vectors_26[:, face_axis] == -1)[0]

        # 物体に対して前方後方向きのベクトルについて考える
        if face_axis == Coordinate.Z.value:
            line_axis = 0  # 画像上x座標が小さい方向ベクトル x or y (0 or 1)
            target_posi_vec_index = np.where(
                self.vectors_26[:, face_axis] == 1)[0]
            target_nega_vec_index = np.where(
                self.vectors_26[:, face_axis] == -1)[0]

        lines = lines[np.argsort(lines[:, line_axis])]

        correct_normal_index = []
        # 閾値は実際にやってうまく言った数値
        diff_coordi_thre = 20
        for i, (point, vec_index) in enumerate(zip(points, vector_index_list)):
            # 対象としている法線ベクトルの場合
            if np.any(target_posi_vec_index == vec_index) or np.any(target_nega_vec_index == vec_index):
                # 各ラインについて見ていく
                for j, line in enumerate(lines):
                    # ラインに点が近いか、判別
                    if abs(point[face_axis] - line[line_axis]) < diff_coordi_thre:
                        # 偶数本の場合
                        if j % 2 == 0:
                            if np.any(target_posi_vec_index == vec_index):
                                normals[i] = \
                                    self.reverse_vector(normals[i], vec_index)
                        # 奇数本の場合
                        elif any(target_nega_vec_index == vec_index):
                            correct_normal_index.append(i)
                            normals[i] = \
                                self.reverse_vector(normals[i], vec_index)

        self.log.add(title="Invert Normal Executed", log="True")
        return normals, correct_normal_index

    def edit_normal(self, points: np.ndarray, normals=None) -> None:
        """法線ベクトルを修正する関数.
        Args:
            points: 点群座標
            normals: 法線ベクトル
        """
        # 値が少数なので処理しやすいように正規化
        work_points = points * 1000
        work_points = np.floor(work_points).astype(int)

        """点群を法線の向きでグループ分け"""
        # vector_index_list: 法線が'self.vectors_26'の中で一番近いベクトルのインデックスを格納
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

        # 確認用
        # for i, count in enumerate(count_list):
        #     print(f"{i}: {count}")

        """椅子の側面を修正"""

        # """
        # 左右方向の法線ベクトルを修正
        correct_normals = self.correct_direct_outside(
            points, normals, vector_index_list, coordi_index=Coordinate.X.value)
        correct_normals = self.correct_direct_outside(
            points, correct_normals, vector_index_list, coordi_index=Coordinate.Y.value)
        if correct_normals is not None:
            normals = correct_normals
        # """

        """椅子の面を見つけて編集する"""

        correct_point = None
        # """
        # 側面の画像を描画する
        img = self.draw_point_cloud_axes(
            work_points, vector_index_list, coordi_index=Coordinate.X.value)

        # 側面から線(面)を出力する
        lines, vertical_line, horizontal_line = self.detect_line(
            img, coordi_index=Coordinate.X.value)

        # 側面方向に見ていく(椅子の背もたれの面のベクトル方向はZ)
        correct_normals, correct_normal_index = self.inversion_normal(
            work_points, normals, vertical_line, vector_index_list, face_axis=Coordinate.Z.value)
        if correct_normals is None:
            return normals, None, None
        else:
            normals = correct_normals

        # 椅子の座る部分の面を見つけて法線ベクトルの補正を加える
        correct_normals, correct_normal_index = self.inversion_normal(
            work_points, normals, horizontal_line, vector_index_list, face_axis=Coordinate.Y.value)
        # if correct_normals is None:
        #     return normals, None, None
        # else:
        #     normals =  correct_normals

        if correct_normal_index is not None:
            correct_point = points[correct_normal_index]

        return normals, None, correct_point
