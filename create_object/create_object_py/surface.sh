#!/bin/bash

# 引数1にデフォルト値"0"を設定
arg1="${1:-0}"
arg2="${2:-0}"

# 実行コマンドの表示
echo "poetry run python3 src/create_surface.py --catecory_number $arg1 --image_number $arg2"

# 実行
poetry run python3 src/create_surface.py --catecory_number $arg1 --image_number $arg2