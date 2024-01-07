import os
import cv2
import numpy as np
from itertools import cycle


from param_create_surface import Param
from calculator import Calculator
from coordinate import Coordinate

SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)
WORK_DIR_PATH = os.path.join(PROJECT_DIR_PATH, "data")


class EditNormalMethod:
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

    def correct_direct_outside(self, points, normals, vector_index_list,
                               coordi_index: int, symmetry="point"):
        """法線ベクトルを外側に向ける関数.
        Args:
            points: 点群座標
            normals: 法線ベクトル
            vector_index_list: 26方位のベクトルを比較
            coordi_index: 外側に向ける座標軸
            symmetry: 線対称or点対称(line or point)
        """
        """条件を決定"""
        target_posi_vec_index = np.where(
            self.vectors_26[:, coordi_index] == 1)[0]
        target_nega_vec_index = np.where(
            self.vectors_26[:, coordi_index] == -1)[0]

        for i, vec_index in enumerate(vector_index_list):
            if np.any(target_nega_vec_index == vec_index) and points[i, coordi_index] > 0:
                if symmetry == "point":
                    normals[i] = self.reverse_vector(normals[i], vec_index)
                if symmetry == "line":
                    normals[i, coordi_index] *= -1
            elif np.any(target_posi_vec_index == vec_index) and points[i, coordi_index] < 0:
                if symmetry == "point":
                    normals[i] = self.reverse_vector(normals[i], vec_index)
                if symmetry == "line":
                    normals[i, coordi_index] *= -1
        # return normals

    def draw_point_cloud_axes(self, points, vector_index_list, coordi_index: int, all_point=False):
        """各座標軸に対して描画する関数."""

        """画像のサイズを決定する"""
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

        """画像に点を記述"""
        # NOTE: img[y,x]に注意
        # 側面画像
        correct_value = 2
        if coordi_index == Coordinate.X.value:
            for point, vec_index in zip(points, vector_index_list):
                if not all_point and (
                        vec_index == self.right_vector_index or
                        vec_index == self.left_vector_index):
                    continue
                _, y, z = point
                # 点を描画
                img[y-correct_value:y+correct_value,
                    z-correct_value:z+correct_value] = [0, 0, 0]
            img_name = "beside_yz.png"
        # 上面画像
        elif coordi_index == Coordinate.Y.value:
            for point, vec_index in zip(points, vector_index_list):
                if not all_point and (
                    vec_index == self.upper_vector_index or
                        vec_index == self.lower_vector_index):
                    continue
                x, _, z = point
                # 点を描画
                img[z-correct_value:z+correct_value,
                    x-correct_value:x+correct_value] = [0, 0, 0]
            img_name = "upper_zx.png"
        # 正面画像
        elif coordi_index == Coordinate.Z.value:
            for point, vec_index in zip(points, vector_index_list):
                if not all_point and (
                    vec_index == self.front_vector_index or
                        vec_index == self.back_vector_index):
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

    def detect_line(self, img, line_thre=150):
        """線を検出する関数.
        Args:
            img: 点群を描画した画像
        """

        """ライン検出"""
        print(f"img.shape: {img.shape}")

        # エッジ検出
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        reversed_gray = cv2.bitwise_not(gray)
        # cv2.imwrite(os.path.join(WORK_DIR_PATH, 'bitwise.png'), reversed_gray)

        # 線分検出
        # 参考: https://way2se.ringtrees.com/py_cv2-004/#toc7
        lines = cv2.HoughLinesP(reversed_gray, rho=1,
                                theta=np.pi/180, threshold=line_thre,
                                minLineLength=int(img.shape[0]*0.25), maxLineGap=200)
        lines = lines[:, 0, :]

        # 線が見つからない場合
        if lines is None:
            if Param.work_process and Param.output_image and self.develop:
                detect_line_img = img.copy()
                cv2.imwrite(os.path.join(WORK_DIR_PATH,
                            'detect_line.png'), detect_line_img)
            self.log.add(title="Detect lines", log="None")  # ログ
            return None, None, None
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
        # lineマージ用
        diff_coordi_thre = int(img.shape[0] / 50)  # x1座標の閾値
        dis_thre = int(img.shape[0] / 40)  # 直線と点の距離の閾値
        self.log.add(title="diff_coordi_thre", log=diff_coordi_thre)  # ログ
        self.log.add(title="dis_thre", log=dis_thre)  # ログ
        pre_line = None
        # 縦線用
        vertical_lines = lines[np.argsort(lines[:, 0])]
        vertical_line_index = []
        # 横線用1
        horizontal_line_index = []

        # 縦線だけを見ていく
        for i, line in enumerate(vertical_lines):
            # 横線は無視
            if Calculator.calculate_slope(line) < 45:
                horizontal_line_index.append(i)
            elif pre_line is None:  # 最初の縦線
                pre_line = line
                vertical_line_index.append(i)
            else:
                """採用するラインの条件を設定"""
                # ライン同士の距離で比較
                condition = Calculator.distance_point_to_line(pre_line, line[:2]) > dis_thre\
                    or Calculator.distance_point_to_line(pre_line, line[2:]) > dis_thre

                """削除するラインのindexを保持"""
                if condition:
                    vertical_line_index.append(i)
                    pre_line = line

        # 横線用2
        self.log.add(title="len(horizontal_line_index)",
                     log=len(horizontal_line_index))
        horizontal_lines = np.array([]).reshape([0, 4])
        horizontal_index = []
        pre_line = None
        if len(horizontal_line_index) > 1:
            horizontal_lines = vertical_lines[horizontal_line_index]
            horizontal_lines = horizontal_lines[np.argsort(
                horizontal_lines[:, 1])]
            # 横線だけを見ていく
            for i, line in enumerate(horizontal_lines):
                if pre_line is None:  # 最初の縦線
                    pre_line = line
                    horizontal_index.append(i)
                else:
                    """採用するラインの条件を設定"""
                    # ライン同士の距離で比較
                    condition = Calculator.distance_point_to_line(pre_line, line[:2]) > dis_thre\
                        or Calculator.distance_point_to_line(pre_line, line[2:]) > dis_thre
                    """削除するラインのindexを保持"""
                    if condition:
                        horizontal_index.append(i)
                        pre_line = line
            horizontal_lines = horizontal_lines[horizontal_index]

        elif len(horizontal_line_index) == 1:
            horizontal_lines = vertical_lines[horizontal_line_index]

        # ラインの選定
        vertical_lines = vertical_lines[vertical_line_index]
        horizontal_lines = np.array(horizontal_lines)  # list to numpy

        lines = np.concatenate([vertical_lines, horizontal_lines])

        self.log.add(title="Vertical lines", log=vertical_lines.shape)  # ログ
        self.log.add(title="Horizontal lines",
                     log=horizontal_lines.shape)  # ログ
        self.log.add(title="Mearged Detect lines", log=lines.shape)  # ログ

        if Param.work_process and Param.output_image and self.develop:
            # 結果を表示
            detect_line_img = img.copy()
            colors = cycle([(0, 0, 255), (0, 255, 0),
                           (255, 0, 0)])  # (B, G, R)
            for line in lines:
                x1, y1, x2, y2 = map(int, line)
                color = next(colors)
                cv2.line(detect_line_img, (x1, y1), (x2, y2), color, 5)
            # diff_coordi_threの閾値の幅の確認
            detect_line_img[:, 50:52] = [0, 0, 255]
            detect_line_img[:, 50+diff_coordi_thre:52 +
                            diff_coordi_thre] = [0, 0, 255]
            # dis_threの閾値の幅の確認
            detect_line_img[50:52, :] = [0, 0, 255]
            detect_line_img[50+dis_thre:52+dis_thre,
                            :] = [0, 0, 255]
            cv2.imwrite(os.path.join(WORK_DIR_PATH,
                        'detect_line_mearged.png'), detect_line_img)

        return lines, vertical_lines, horizontal_lines

    def reverse_vector(self, normal, vector_26_index, face_axis=None):
        """ベクトルを逆にする関数."""
        vector = self.vectors_26[vector_26_index]
        reversed_vector = normal.copy()
        if face_axis is None:
            for i, element in enumerate(vector):
                if element != 0:
                    reversed_vector[i] *= -1
        else:
            reversed_vector[face_axis] *= -1
        return reversed_vector

    def inversion_normal(self, points, normals, lines, vector_index_list, face_axis):
        """面(線)の本数によって法線ベクトルを修正.
        Args:
            lines: 面を表す線
            vector_index_list: 26方位に分類したときのindexを格納した配列
            face_axis: 面面を表す法線ベクトルの座標系 ※0(x) or 1(y) or 2(z)
        """

        if lines.shape[0] == 1:
            return

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

        if lines.shape[0] % 2 == 1:
            diff_s = abs(lines[0, 0] - lines[1, 0])
            diff_e = abs(lines[-1, 0] - lines[-2, 0])
            if diff_s < diff_e:
                lines = lines[:-1]
            else:
                lines = lines[1:]

        correct_even_index = []
        correct_odd_index = []
        # 閾値は実際にやってうまく言った数値
        diff_coordi_thre = 30
        for i, (point, vec_index) in enumerate(zip(points, vector_index_list)):
            # 対象としている法線ベクトルの場合
            if np.any(target_posi_vec_index == vec_index) or np.any(target_nega_vec_index == vec_index):
                # 各ラインについて見ていく
                near_line_index = None
                min_dis = 1000
                for j, line in enumerate(lines):
                    dis = abs(point[face_axis] - line[line_axis])  # ラインとの距離を算出
                    if dis < min_dis:
                        near_line_index = j  # 一番近いラインの更新
                        min_dis = dis

                # ラインから点が近い場合
                if near_line_index is not None and min_dis < diff_coordi_thre:
                    # 偶数本の場合(Even Number)
                    if near_line_index % 2 == 0:
                        if normals[i, face_axis] > 0:
                            normals[i] = self.reverse_vector(
                                normals[i], vec_index, face_axis)
                            correct_even_index.append(i)  # 赤

                    # 奇数本の場合(Odd Number)
                    else:
                        if normals[i, face_axis] < 0:
                            normals[i] = self.reverse_vector(
                                normals[i], vec_index, face_axis)
                            correct_odd_index.append(i)  # 青

        # return normals, correct_even_index, correct_odd_index

    def correct_edge_point(self, points, normals, axis=Coordinate.X.value):
        """一番端にある点群を外側に向ける関数.

        NOTE
        行ごとの端を見ると斜めの判定を間違ってしまうため一番端の座標のみを見る

        """

        p_range = 10
        max = np.amax(points[:, axis], axis=0)
        min = np.amin(points[:, axis], axis=0)

        condision1 = max - p_range < points[:, axis]
        condision2 = min + p_range > points[:, axis]
        outside_index_max = np.where(condision1)[0]
        outside_index_min = np.where(condision2)[0]

        # 修正するベクトルの作成
        truth_normal = np.zeros(3)
        truth_normal[axis] += 1

        for index in outside_index_max:
            normals[index] *= 0
            normals[index, axis] += 1

        for index in outside_index_min:
            normals[index] *= 0
            normals[index, axis] -= 1

    def correct_edge_point_detail(self, points, normals, correct_axis=Coordinate.X.value):
        """一番端にある点群を外側に向ける関数.
        未完成
        うまくできていない理由が良く分かっていない
        同じ行に点が一個だった場合の判定が難しい？


        """

        range_thre = 5

        if correct_axis == Coordinate.X.value or correct_axis == Coordinate.Z.value:
            # 行としてみる軸の決定
            line_axis = Coordinate.Y.value
        elif correct_axis == Coordinate.Y.value:
            line_axis = Coordinate.Z.value

        axis_max = np.amax(points[:, line_axis], axis=0)
        axis_min = np.amin(points[:, line_axis], axis=0)

        correct_index = []

        for line_coordi in range(axis_min, axis_max):
            # 行にある点を抽出
            range_points_index = np.where(
                points[:, line_axis] == line_coordi)[0]
            if range_points_index.shape[0] == 0:
                continue

            # 行の中の最大値、最小値を求める
            max_point_index = range_points_index[np.argmax(
                points[range_points_index, line_axis])]
            min_point_index = range_points_index[np.argmin(
                points[range_points_index, line_axis])]

            print(f"range_points_index: {range_points_index}")
            count = 0
            for index in range_points_index:
                if points[index, line_axis] > points[max_point_index, line_axis]-range_thre:
                    # print(points[index, line_axis], points[max_point_index, line_axis]-range_thre)
                    normals[index] *= 0
                    normals[index, line_axis] += 1
                    correct_index.append(index)
                elif points[index, line_axis] < points[min_point_index, line_axis]+range_thre:
                    normals[index] *= 0
                    normals[index, line_axis] -= 1
                    correct_index.append(index)
                    count += 1
                # else:
            # if count != 0: print(count)

            # condition2 = max - p_range < points[:, axis] # 最大
            # condition3 = points[:, axis] < p_range + min # 最小

            # # 法線ベクトルの補正
            # max_range_index = np.where(condition1 & condition2)[0]
            # normals[max_range_index] *= 0
            # normals[max_range_index, axis] += 1

            # # 法線ベクトルの補正
            # min_range_index = np.where(condition1 & condition3)[0]
            # normals[min_range_index] *= 0
            # normals[min_range_index, axis] += 1

            # # y行の点を抽出
            # range_points_index = np.where(points[:, Coordinate.Y.value] == y)[0]
            # if range_points_index.shape[0] == 0:
            #     continue
            # # 特定のy座標に対応する行のデータ
            # selected_rows = points[range_points_index]

            # # 最大の要素のインデックスを取得
            # max_index_within_selected_rows = np.argmax(selected_rows[:, Coordinate.Y.value])
            # # 元の配列での最大の要素のインデックス
            # max_index = range_points_index[max_index_within_selected_rows]
            # # 法線ベクトルの補正
            # normals[max_index] *= 0
            # normals[max_index, axis] += 1

            # # 最小の要素のインデックスを取得
            # min_index_within_selected_rows = np.argmin(selected_rows[:, Coordinate.Y.value])
            # # 元の配列での最大の要素のインデックス
            # min_index = range_points_index[min_index_within_selected_rows]
            # # 法線ベクトルの補正
            # normals[min_index] *= 0
            # normals[min_index, axis] -= 1

        # correct_index.append(max_range_index)
        # correct_index.append(min_range_index)

        return normals, correct_index
