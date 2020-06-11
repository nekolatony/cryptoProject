import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *

import venv
import PySimpleGUI as sg


def main():

    print("Please enter image url:")
    #url = input()
    url = "tiger.jpg"
    img = c.imread(url,0)
    cv2.imshow("Original Photo", img)
    popupmsg("Click OKAY to ENCRYPT!")
    cv2.waitKey(0)
    #img = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    orginalPixels = ConvertImageToStringArray(img)
    print(len(orginalPixels))
    user1 = venv.DH_Endpoint(197, 151, 199)
    user2 = venv.DH_Endpoint(197,151,157)
    alicePartialKey = user1.generate_partial_key()
    bobPartialKey = user2.generate_partial_key()
    key = user1.generate_full_key(alicePartialKey)
    key = user2.generate_full_key(bobPartialKey)
    key = str(key)
    if len(key) <16:
        key = key + " "*(16-len(key))
    key = key[:16]
    RCKey = generateKey(key)
    print(orginalPixels)

    encrypted = []
    cipheredPixels = CBC_encrypt(orginalPixels , RCKey)

    cipherImage = np.empty([len(img) + 1, len(img[0]) + 1], dtype=int)

    k=0
    for i in range(len(img)):
        for j in range(len(img[0])):
            cipherImage[i][j] = cipheredPixels[k] % 256
            k = k + 1

    cv2.imwrite('encrypted.png', cipherImage)
    img2 = cv2.imread('encrypted.png',0)
    cv2.imshow("Encrypted Photo" , img2)
    popupmsg("Click OKAY to DECRYPT!")
    cv2.waitKey(0)


    print("Original pixels (String): " + str(orginalPixels))
    print("Encrypted pixels (long): " + str(cipheredPixels))
    print("Encrypted pixels (String): " + str(encrypted))
    enc = []
    de = deBlocker(cipheredPixels)
    for i in range (0,len(de),4):
        enc.append(de[i:i+4])
   # print("deBlocker (String): " +de)
    decryptedM =  CBC_decrypt(enc,RCKey)
    print("Decrypted pixels: "+ str(decryptedM))
    print("Original pixels : " + str(orginalPixels))

    for i in range(0,len(decryptedM)):
        if decryptedM[i] != orginalPixels[i]:
            print(decryptedM[i])

    k = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            cipherImage[i][j] = int(decryptedM[k],base=10) % 256
            k = k + 1
        # print(cipherImage)

    cv2.imwrite('decrypted.png', cipherImage)

    img3 = cv2.imread('decrypted.png',0)
    cv2.imshow("Decrypted Photo" , img3)

    popupmsg("Click OKAY to Exit!")
    cv2.waitKey(0)
if __name__ == "__main__":
    main()



