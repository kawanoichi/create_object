#!/bin/bash

# 引数1にデフォルト値"0"を設定
arg1="${1:-0}"

# 実行コマンドの表示
echo "poetry run python3 src/create_surface.py --catecory_number $arg1"

# 実行
poetry run python3 src/create_surface.py --catecory_number $arg1