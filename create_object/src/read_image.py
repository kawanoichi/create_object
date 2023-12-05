# """
import datetime
import os


def main():
    print("Execute Python")
    print(datetime.datetime.now())

if __name__=="__main__":
    main()
# """    

"""  
from PIL import Image
import sys

def convert_image(input_path, output_path):
    image = Image.open(input_path)
    image = image.convert("RGB")
    image.save(output_path, "JPEG")

if __name__ == "__main__":
    input_image = sys.argv[1]
    output_image = input_image.replace('.png', '.jpg')
    convert_image(f"storage/public/{input_image}", f"storage/public/{output_image}")
    print(output_image)
"""