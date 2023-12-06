import datetime
# import os
import sys

# from PIL import Image
# import cv2

def main(image_path="None"):
    print("Execute Python")
    print(datetime.datetime.now())
    
    print("image_path:", image_path)
    
    """
    path = os.path.join("/var/www/html/public", "image_data", image_name)
    image = cv2.imread(path)
    print(image.shape)
    # """

# def convert_image(input_path, output_path):
#     image = Image.open(input_path)
#     image = image.convert("RGB")
#     image.save(output_path, "JPEG")

if __name__ == "__main__":
    image_path = sys.argv[1]
    # image_path = "bbb"
    main(image_path)
    # output_image = input_image.replace('.png', '.jpg')
    # convert_image(f"storage/public/{input_image}", f"storage/public/{output_image}")
    # print(output_image)