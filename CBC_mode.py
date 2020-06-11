import cv2
import numpy as np
from numpy import long
from encrypt import *
from decrypt import *
from helpers import *
import os
import io
from array import array



def convertToBin(message):
    block = []
    for pixel in message:
        tmp = ""
        for digit in pixel:
            tmp = bin(int(digit))[2:]
            tmp = "0" * (8 - len(tmp)) + tmp
        block.append(tmp)
    for i in range(len(block) % 4):
        block.append('0' * 8)
    return block

#Key add (CBC takes a key to perform encryption)
def CBC_encrypt(message,key):
    blocks = message
    answer = xor_two_str(blocks[0]+blocks[1]+blocks[2]+blocks[3] , "123456789abcdefg")

    orgi,encrypted_block = encrypt(answer, key)
    cipher = list(encrypted_block[0:])

    for k in range(4, len(blocks) , 4):
        #eCipher = deBlocker(cipher)
        #cipherBlocks = StringToBlocks(eCipher)
        answer = xor_two_str(blocks[k] + blocks[k+1] + blocks[k+2] + blocks[k+3], deBlocker(encrypted_block))

        #answer = xor_two_str(blocks[k] + blocks[k + 1] + blocks[k + 2] + blocks[k + 3], "123456789abcdefg")

        orgi,encrypted_block = encrypt(answer, key)
        cipher.append(encrypted_block[0])
        cipher.append(encrypted_block[1])
        cipher.append(encrypted_block[2])
        cipher.append(encrypted_block[3])
        # print("encryption number " + str(k))
    return cipher



#Key add (CBC takes a key to perform decryption)
def CBC_decrypt(message,key):
    blocks = message
    print("********************************DECRYPTING*********************************")
    orgi,decrypted_block = decrypt((blocks[0:4]), key)
    answer = xor_two_str(deBlocker(decrypted_block), "123456789abcdefg")
    orginal = [answer[:4],answer[4:8],answer[8:12],answer[12:16]]

    for k in range(4, len(blocks) , 4):
        orgi,decrypted_block = decrypt((blocks[k:k + 4]), key)
        answer = xor_two_str(blocks[k-4]+ blocks[k-3] + blocks[k-2] + blocks[k-1], deBlocker(decrypted_block))
        #answer = xor_two_str("1234567891234567", deBlocker(decrypted_block))

        print("[",k,"] answer ",answer)
        print(answer[:4]," ",answer[4:8]," " ,answer[8:12]," ",answer[12:16])
        orginal.append(answer[:4])
        orginal.append(answer[4:8])
        orginal.append(answer[8:12])
        orginal.append(answer[12:16])
        # print("decryption number " + str(k))
    return orginal

