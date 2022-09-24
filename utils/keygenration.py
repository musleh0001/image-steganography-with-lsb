def keygen(x, r, size):
    """
    x: range = [0.0, 0.1]
    r: range = [3.0, 4.0]
    Function to generate key using a chaotic map for an encryption process
    """
    key = []

    for i in range(size):
        x = r * x * (1 - x)  # logistic map
        key.append(int((x * pow(10, 16)) % 256))  # key

    return key
