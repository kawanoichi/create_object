import os
import json
SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.dirname(SCRIPT_DIR_PATH)

"""
# JSONファイルからデータを読み込む
json_path = os.path.join(SCRIPT_DIR_PATH, 'param.json')
with open(json_path, 'r') as json_file:
    Param = json.load(json_file)

# データの変更
Param['web'] = True

# 変更したデータをJSONファイルに書き込む
with open(json_path, 'w') as json_file:
    json.dump(Param, json_file, indent=2)

print(Param.web)
# """

# # JSONファイルからデータを読み込む
# with open('zikken.json', 'r') as json_file:
#     Param = json.load(json_file)

# # データの変更
# Param['web'] = True

# # 変更したデータをJSONファイルに書き込む
# with open('zikken.json', 'w') as json_file:
#     json.dump(Param, json_file, indent=2)

flag = True

print(not flag)

if 0:
    print("1")
else:
    print(2)