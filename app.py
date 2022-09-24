from PIL import Image
import numpy as np
import datetime
from werkzeug.utils import secure_filename
import sys
import codecs

from utils.encoder_decoder import encode, decode
from utils.encrypt_decrypt import encrypt_message, decrypt_message
from utils.helper import bin_to_int, generate_binary, load_img
from utils.keygenration import keygen


# Main function
def main():
    x = 0.003
    r = 3.954

    with open("./resources/input.txt", "r") as file:
        content = file.read()
    # content = input("Enter the content you want to hide:\n")

    # key generate
    key = keygen(x, r, len(content))
    with open("./resources/key.txt", "w") as file:
        str_key = " ".join(str(x) for x in key)
        file.write(str_key)

    # encrypt message
    encrypt_msg = encrypt_message(content, key)
    data = generate_binary(encrypt_msg)

    image = load_img()
    encoded_img, fname = encode(image, data)

    # decrypt message
    decoded_data = decode(encoded_img)
    result_data = bin_to_int(decoded_data)
    decrypt_msg = decrypt_message(result_data, key)

    print("Encoded image is present in output folder with name", fname, "\n")
    print("Decoded message from image is present in output folder with name decode.txt")

    with open("./output/decoded.txt", "w") as file:
        file.write(decrypt_msg)


# Driver code
if __name__ == "__main__":
    main()
