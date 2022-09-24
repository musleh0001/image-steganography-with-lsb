import os
from PIL import Image

# Binary to int
def bin_to_int(data):
    encrypt_data = []
    for d in data:
        binary_int = int(d, 2)
        encrypt_data.append(binary_int)
    return encrypt_data


# Convert user input to 8 bit binary using Unicode value of characters
def generate_binary(data):
    # converted data
    new_data = []

    for i in data:
        # converting every character of user input to its binary
        new_data.append(format(i, "08b"))
        # new_data.append(format(ord(i), "08b"))

    # ord returns the unicode of string(of unit length only..so a character basically)
    # character to Unicode to binary
    # unicode preferred over Ascii as superset of ascii and characters of other languages also available
    return new_data


# Load image
def load_img(imageName):
    dir_name = "./resources/"
    # resource_name = "./resources/mangekyo.jpg"
    # image = Image.open(resource_name, "r")
    # return image

    for (root, dirs, files) in os.walk(dir_name):
        if imageName in files:
            img = os.path.join(root, imageName)
            return Image.open(img, "r")
    return None
