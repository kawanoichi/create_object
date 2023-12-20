#!/bin/bash

# カウンタの初期化
counter=0

# ループで各画像ファイルに番号を付ける
for file in *.png; do
    # 新しいファイル名を生成
    new_name="${counter}_${file}"

    # ファイル名を変更
    mv "$file" "$new_name"

    # カウンタをインクリメント
    ((counter++))
done
