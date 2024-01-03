import sys

print(f"Python Version: {sys.version}")

try:
    import cv2
except Exception as e:
    print(e)
else:
    print("cv2 is exist")

try:
    import numpy
except Exception as e:
    print(e)
else:
    print("numpy is exist")

try:
    import open3d
except Exception as e:
    print(e)
else:
    print("open3d is exist")

try:
    import torch
except Exception as e:
    print(e)
else:
    print("torch is exist")
try:
    import matplotlib
except Exception as e:
    print(e)
else:
    print("matplotlib is exist")
