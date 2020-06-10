import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *


def main():
    print("Please enter image url:")
    url = input()
    img = c.imread(url,0)
    orginalPixels = ConvertImageToStringArray(img)
    print(orginalPixels)

    cipheredPixels = CBC_encrypt(orginalPixels)








if __name__ == "__main__":
    main()