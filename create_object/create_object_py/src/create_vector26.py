"""26方位のベクトルを作成して保存するモジュール."""
import os
import numpy as np


def vector_26(save_path):
    """26方位ベクトル作成関数."""
    kinds_of_coodinate = [-1, 0, 1]
    # 26方位のベクトル(終点座標)を作成
    vectors_26 = np.array([])
    for x in kinds_of_coodinate:
        for y in kinds_of_coodinate:
            for z in kinds_of_coodinate:
                if not x == y == z == 0:
                    append_coordinate = np.array([x, y, z])
                    vectors_26 = np.append(
                        vectors_26, append_coordinate, axis=0)
    vectors_26 = vectors_26.reshape(
        (len(kinds_of_coodinate) ^ 3)-1, 3)

    np.save(save_path, vectors_26)
    return vectors_26


def show_vector(npy_path):
    # ファイルからデータを読み込む
    loaded_data = np.load(npy_path)

    # 読み込んだデータを表示
    for i, data in enumerate(loaded_data):
        print(f"{i}: {data}")


if __name__ == "__main__":
    SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    print(f"SCRIPT_DIR_PATH : {SCRIPT_DIR_PATH}")
    npy_path = os.path.join(SCRIPT_DIR_PATH, "vector26.npy")
    # vector_26(npy_path)
    print(f"npy_path : {npy_path}")
    show_vector(npy_path)
