from PIL import Image
import numpy as np
import datetime
from werkzeug.utils import secure_filename
import sys
import codecs


count = 0

# Encode the image
def encode(image, data):
    # iterate the image pixels
    # store user input in LSB(least significant bit) of each pixels RGB depending on need
    # start with B then G then R..

    arr = np.array(image)
    # print(arr.shape) ...to see size of img

    # 3d array....2d pixel array with 3 channels
    red = arr[..., 0]  # All Red values
    green = arr[..., 1]  # All Green values
    blue = arr[..., 2]  # All Blue values

    # pixels can be odd or even

    height, width = blue.shape
    incompBlue = True
    incompGreen = True
    incompRed = True

    blue[0][0] = 193
    blue[0][2] = 882
    i = 0
    j = -1
    global count
    c = 0
    for char in data:
        for bit in char:
            count += 1
            if incompBlue == True:
                if i < height:
                    if j < width:
                        j += 1
                    if j >= width:
                        i += 1
                        j = 0
                    # print("{0:b}".format(blue[i][j]))
                    # if bit of char is 1

                    # print(i,j)
                    if i < height:
                        if bit == "1":
                            blue[i][j] = blue[i][j] | 1  # set the last bit to 1
                        elif bit == "0":
                            blue[i][j] = blue[i][j] & (
                                blue[i][j] - 1
                            )  # set the last bit to 0
                        c += 1
                    else:
                        incompBlue = False
                        i = 0
                        j = -1

                    # print("{0:b}".format(blue[i][j]))
                    # print('\n')

                else:
                    incompBlue = False
                    i = 0
                    j = -1

            if incompBlue == False and incompGreen == True:
                if i < height:
                    if j < width:
                        j += 1
                    if j >= width:
                        i += 1
                        j = 0
                    # print("{0:b}".format(green[i][j]))
                    # if bit of char is 1
                    # print("g",i,j)
                    if i < height:
                        if bit == "1":
                            green[i][j] = green[i][j] | 1  # set the last bit to 1
                        elif bit == "0":
                            green[i][j] = green[i][j] & (
                                green[i][j] - 1
                            )  # set the last bit to 0
                        c += 1
                    else:
                        incompGreen = False
                        i = 0
                        j = -1

                    # print("{0:b}".format(green[i][j]))
                    # print('\n')
                else:
                    incompGreen = False
                    i = 0
                    j = -1
            if incompBlue == False and incompGreen == False:
                if i < height:
                    if j < width:
                        j += 1
                    if j >= width:
                        i += 1
                        j = 0
                    # print("{0:b}".format(red[i][j]))
                    # if bit of char is 1
                    # print("r",i,j)
                    if i < height:
                        if bit == "1":
                            red[i][j] = red[i][j] | 1  # set the last bit to 1
                        elif bit == "0":
                            red[i][j] = red[i][j] & (
                                red[i][j] - 1
                            )  # set the last bit to 0
                        c += 1
                    else:
                        incompRed = False
                        sys.exit("Choose a higher quality image")

                    # print("{0:b}".format(red[i][j]))
                    # print('\n')
                else:
                    incompRed = False
                    i = 0
                    j = -1
                    break

    if incompRed == False:
        sys.exit("Choose a higher quality image")

    w, h = image.size
    test = np.zeros((h, w, 3), dtype=np.uint8)

    # reconstructing image
    test[:, :, 0] = red
    test[:, :, 1] = green
    test[:, :, 2] = blue

    # current time and filename
    ct = datetime.datetime.now()
    # filename = secure_filename("encoded_image " + str(ct) + ".jpg")
    filename = secure_filename("encoded_image.jpg")

    # saving image
    img = Image.fromarray(test, "RGB")
    img.save("./resources/" + filename)
    # img.show()
    return [img, filename]


# Decode the image
def decode(image):
    arr = np.array(image)
    red = arr[..., 0]  # All Red values
    green = arr[..., 1]  # All Green values
    blue = arr[..., 2]  # All Blue values

    height, width = blue.shape
    total_size = height * width
    data = []
    bit_size = 0
    data_byte = ""

    if count < total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):
                if new_count <= count:
                    if bit_size < 8:
                        data_byte = data_byte + str((blue[i][j] & 1))
                        bit_size += 1
                    else:
                        data.append(data_byte)
                        bit_size = 0
                        data_byte = ""

                        data_byte = data_byte + str((blue[i][j] & 1))
                        bit_size += 1

                    new_count += 1
                else:
                    break

    elif count > total_size and count < 2 * total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):
                if bit_size < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size += 1
                else:
                    data.append(data_byte)
                    bit_size = 0
                    data_byte = ""

                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size += 1
        bit_size = 0
        data_byte = ""

        for i in range(height):
            for j in range(width):
                if new_count <= count:
                    if bit_size < 8:
                        data_byte = data_byte + str((green[i][j] & 1))
                        bit_size += 1
                    else:
                        data.append(data_byte)
                        bit_size = 0
                        data_byte = ""

                        data_byte = data_byte + str((green[i][j] & 1))
                        bit_size += 1

                    new_count += 1
                else:
                    break
    else:
        new_count = 0
        for i in range(height):
            for j in range(width):
                if bit_size < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size += 1
                else:
                    data.append(data_byte)
                    bit_size = 0
                    data_byte = ""

                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size += 1
        bit_size = 0
        data_byte = ""

        for i in range(height):
            for j in range(width):
                if bit_size < 8:
                    data_byte = data_byte + str((green[i][j] & 1))
                    bit_size += 1
                else:
                    data.append(data_byte)
                    bit_size = 0
                    data_byte = ""

                    data_byte = data_byte + str((green[i][j] & 1))
                    bit_size += 1
        bit_size = 0
        data_byte = ""

        for i in range(height):
            for j in range(width):
                if new_count <= count:
                    if bit_size < 8:
                        data_byte = data_byte + str((red[i][j] & 1))
                        bit_size += 1
                    else:
                        data.append(data_byte)
                        bit_size = 0
                        data_byte = ""

                        data_byte = data_byte + str((red[i][j] & 1))
                        bit_size += 1

                    new_count += 1
                else:
                    break
    return data
