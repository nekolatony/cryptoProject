import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *


def main():
    print("Please enter image url:")
    #url = input()
    url = "tiger.jpg"
    img = c.imread(url,0)
    orginalPixels = ConvertImageToStringArray(img)
    key = DiffeHellman()
    RCKey = generateKey(key)
    print(orginalPixels)

    cipheredPixels = CBC_encrypt(orginalPixels , RCKey)








if __name__ == "__main__":
    main()