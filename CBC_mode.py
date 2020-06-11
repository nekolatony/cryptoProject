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
    #no need to convert to binnarry here
    #blocks = convertToBin(message)
    blocks = message
    A = blocks[0][0] #long(blocks[0], 2)
    B = blocks[0][1] #long(blocks[1], 2)
    C = blocks[0][2] #long(blocks[2], 2)
    D = blocks[0][3] #long(blocks[3], 2)
    answer = xor_two_str(blocks[0]+blocks[1]+blocks[2]+blocks[3] , "1234567891234567")

    orgi,encrypted_block = encrypt(answer, key)
    cipher = list(encrypted_block)
    #cipher = list(encrypted_block[0])
    #cipher = list(encrypted_block[1])
    #cipher = list(encrypted_block[2])
    #cipher = list(encrypted_block[3])

    for k in range(4, len(blocks) , 4):
        answer = xor_two_str(blocks[k] + blocks[k+1] + blocks[k+2] + blocks[k+3], cipher[(k-4)]+cipher[(k-4)+1]+cipher[(k-4)+2]+cipher[(k-4)+3])
        orgi,encrypted_block = encrypt(answer, key)
        cipher.append(encrypted_block[0])
        cipher.append(encrypted_block[1])
        cipher.append(encrypted_block[2])
        cipher.append(encrypted_block[3])
    return cipher




def CBC_decrypt(cipher):
    blocks = convertToBin(cipher)

    A = long(blocks[0], 2)
    B = long(blocks[1], 2)
    C = long(blocks[2], 2)
    D = long(blocks[3], 2)

    decrypted_block = CR6_decrypt([A, B, C, D])
    message = list(decrypted_block[0])
    message = list(decrypted_block[1])
    message = list(decrypted_block[2])
    message = list(decrypted_block[3])

    for k in range(0, len(blocks) // 4):
        A = long(blocks[4 * k], 2)
        B = long(blocks[4 * k + 1], 2)
        C = long(blocks[4 * k + 2], 2)
        D = long(blocks[4 * k + 3], 2)
        decrypted_block = CR6_encrypt([A, B, C, D])
        message.append(decrypted_block[0] ^ cipher[4 * k - 4])
        message.append(decrypted_block[1] ^ cipher[4 * k - 3])
        message.append(decrypted_block[2] ^ cipher[4 * k - 2])
        message.append(decrypted_block[3] ^ cipher[4 * k - 1])
    return message

