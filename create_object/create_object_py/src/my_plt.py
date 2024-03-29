"""複数画像を表示するためのモジュール
"""
import matplotlib.pyplot as plt
import numpy as np
import math


class MyPlt:
    def __init__(self, max_graph_num):
        # 表示する点群(散布図)に関する変数
        self.fig = plt.figure()  # 表示するグラフ
        self.fig_horizontal = 3
        self.fig_vertical = math.ceil(max_graph_num / self.fig_horizontal)
        self.graph_num = 1  # 横

    def show_point(self, points, title="None") -> None:
        """点群を表示する関数.
        NOTE: 表示する軸方向をopen3dと統一
            x: 右方向
            y: 上
            z: 手前
        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num,
                                  projection='3d')
        plt.xlim(-0.3, 0.3)
        plt.ylim(-0.3, 0.3)
        ax.set_zlim(-0.3, 0.3)
        self.graph_num += 1
        plt.title(title)
        ax.set(xlabel='x', ylabel='y', zlabel='z')
        colors = np.where(points[:, 0] > 0, 'red', 'blue')
        colors1 = np.where(points[:, 0] > 0, 'red', 'blue')
        colors2 = np.where(points[:, 0] > 0, 'purple', 'green')
        colors = np.where(points[:, 1] > 0, colors1, colors2)
        ax.scatter(points[:, 0],
                   points[:, 1],
                   points[:, 2],
                   c=colors)

    def show_point_2D(self, points, title="None") -> None:
        """点群を表示する関数.

        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num)
        self.graph_num += 1

        plt.title(title)
        ax.set(xlabel='x', ylabel='y')

        ax.scatter(points[:, 0],
                   points[:, 1],
                   c='b',
                   s=5)

    def show_correct_point(self, points, index1, index2, title="None") -> None:
        """点群を表示する関数.
        NOTE: 表示する軸方向をopen3dと統一
            x: 右方向
            y: 上
            z: 手前
        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num,
                                  projection='3d')
        plt.xlim(-0.3, 0.3)
        plt.ylim(-0.3, 0.3)
        ax.set_zlim(-0.3, 0.3)
        self.graph_num += 1
        plt.title(title)
        ax.set(xlabel='x', ylabel='y', zlabel='z')
        point = points[index2]
        ax.scatter(point[:, 0],
                   point[:, 1],
                   point[:, 2],
                   c='b')

        point = points[index1]
        ax.scatter(point[:, 0],
                   point[:, 1],
                   point[:, 2],
                   c='r')

    def show_correct_point_2D(self, points, index1, index2, title="None") -> None:
        """2種類の点に分けた点群を表示する.

        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num)
        self.graph_num += 1

        plt.title(title)
        ax.set(xlabel='x', ylabel='y')

        point = points[index2]
        ax.scatter(point[:, 0],
                   point[:, 1],
                   c='b',
                   s=5)

        point = points[index1]
        ax.scatter(point[:, 0],
                   point[:, 1],
                   c='r',
                   s=5)

    def show_normals(self, points, normals, title="None") -> None:
        """点群と法線ベクトルを表示する関数.

        Args:
            points(np.ndarray): 点群
        """
        ax = self.fig.add_subplot(self.fig_vertical,
                                  self.fig_horizontal,
                                  self.graph_num,
                                  projection='3d')
        self.graph_num += 1

        plt.title(title)
        ax.set(xlabel='x', ylabel='y', zlabel='z')

        # 点をプロット
        ax.scatter(points[:, 0], points[:, 1],
                   points[:, 2], c='b', marker='o', label='Points')

        # 法線ベクトルをプロット
        scale = 0.1  # 矢印のスケール
        for i in range(len(points)):
            if points[i, 0] < -0.05:  # 一部を表示
                ax.quiver(points[i, 0], points[i, 1], points[i, 2],
                          normals[i, 0]*scale, normals[i, 1]*scale, normals[i, 2]*scale, color='r', length=1.0, normalize=True)

    @staticmethod
    def show_vector(vector) -> None:
        """原点を視点とした３次元ベクトルを表示する関数."""

        graph_size = 1.5

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.grid()
        ax.set_xlabel("x", fontsize=16)
        ax.set_ylabel("y", fontsize=16)
        ax.set_zlabel("z", fontsize=16)
        ax.set_xlim(-graph_size, graph_size)
        ax.set_ylim(-graph_size, graph_size)
        ax.set_zlim(-graph_size, graph_size)

        # 原点Oを始点にベクトル(-2,3,2)を配置
        for v in vector:
            ax.quiver(0, 0, 0, v[0], v[1], v[2],
                      color="red", length=1,
                      arrow_length_ratio=0.1)

        plt.show()

    def show_result(self) -> None:
        import matplotlib
        matplotlib.use('Agg')
        plt.show()

    def save_result(self, save_path) -> None:
        import matplotlib
        # 最初は以下を実行する
        # $ sudo apt-get install python3-tk
        matplotlib.use('TKAgg')
        plt.savefig(save_path)
