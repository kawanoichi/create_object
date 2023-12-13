# import os
# import sys
# import datetime
# import cv2
# import matplotlib

# # from PIL import Image


# def main(image_path="None"):
#     print("Execute Python")
#     print(datetime.datetime.now())

#     print("image_path:", image_path)

#     if os.path.exists(image_path):
#         print("image is exist")
#     else:
#         print("image is not exist")
#         print("Finish")
#         return
#     image = cv2.imread(image_path)
#     print(image.shape)


# if __name__ == "__main__":
#     print("aaa")
# image_path = sys.argv[1]
# main(image_path)


try:
    # ここにPythonコードを記述
    # import os
    # import sys
    # import datetime
    import cv2
    print("aaa")
except Exception as e:
    import sys
    print(f"An error occurred: {str(e)}", file=sys.stderr)
    sys.exit(1)
