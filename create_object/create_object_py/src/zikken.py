import numpy as np

# ソートしたい配列
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

# ソート後のインデックスを取得
sorted_indices = np.argsort(arr)

# ソート後の配列
sorted_arr = arr[sorted_indices]

# 結果を表示
print("元の配列:", arr)
print("ソート後の配列:", sorted_arr)
print("ソート後のインデックス:", sorted_indices)