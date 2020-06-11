import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *


def main():

    print("Please enter image url:")
    #url = input()
    url = "five.png"
    img = c.imread(url,0)
    #img = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    orginalPixels = ConvertImageToStringArray(img)
    print(len(orginalPixels))
    key = DiffeHellman()
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
        #print(cipherImage)

    cv2.imwrite('encrypted.png', cipherImage)

    #cipheredPixels = [cipheredPixels[i:i+4] for i in range(0, len(cipheredPixels), 4)]

    #for i in range(0,len(cipheredPixels)):
     #   encrypted.append(deBlocker(cipheredPixels[i]))


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
    temp = cv2.imread('decrypted.png',0)



if __name__ == "__main__":
    main()