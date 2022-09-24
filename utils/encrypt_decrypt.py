def encrypt_message(message, key):
    """Encrypt message using key"""

    encrypted = []

    for i in range(len(message)):
        encrypted.append(ord(message[i]) ^ key[i])

    return encrypted


def decrypt_message(message, key):
    """Decrypt message using key"""

    # message = message.split(" ")
    decrypted = ""

    for i in range(len(message)):
        decrypted += str(chr(int(message[i]) ^ int(key[i])))

    return decrypted
