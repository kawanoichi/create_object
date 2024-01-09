import numpy as np


class Calculator:
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

        theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        # 弧度法から度数法に変換
        return np.degrees(theta_rad)

    @staticmethod
    def distance_point_to_line(line, point):
        """直線と点の距離を求める関数.

        line: 直線(x1, y1, x2, y2 = line)
        point: 座標(x, y = point)
        """
        x1, y1, x2, y2 = line
        x, y = point
        numerator = np.abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1))
        denominator = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distance = numerator / denominator
        return distance

    @staticmethod
    def calculate_slope(line):
        """傾きの角度を求める."""
        # 傾きの差が閾値以下であればほぼ同じとみなす
        line_x = line[2] - line[0]
        line_y = line[3] - line[1]
        cos_value = line_x / np.sqrt(line_x**2 + line_y**2)

        # コサインを度数法に変換
        return np.degrees(np.arccos(cos_value))
