from PIL import Image
import numpy as np
import os

def open_and_process(string):
    """
    Open an image whose name is string
    Return (Image object, pixel matrix)
    """
    image = Image.open(string)
    data = list(image.getdata())
    image_matrix = []
    for i in range(image.size[1]):
        image_matrix.append(data[image.size[0] * i : image.size[0] * (i + 1)])
    return (image, image_matrix)

def find_sub_image(test, image):
    """
    test is the test_matrix
    image is the image_matrix
    """
    initial_row = len(test) // 2
    size = len(test[initial_row])
    for i in range(len(test) // 2, len(image)):
        for j in range(len(image[i]) - size):
            if test[initial_row] == image[i][j : j + size]:
                return (j + size // 2, i)

def decorator(f):
    def wrapper(*args):
        ls = [open_and_process(elem)[1] for elem in args]
        return f(*ls)
    return wrapper

@decorator
def find_max_position(espionage_probe, ogame, maxi):
    """
    Return the coordinates of the max in the screen
    """
    p1 = find_sub_image(espionage_probe, ogame)
    p2 = find_sub_image(maxi, ogame)
    return (p2[0], p1[1])

print(find_max_position('espionage_probe.png', 'ogame.png', 'maxi.png'))
