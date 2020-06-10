import cv2
import numpy as np
from numpy import long
import os
import io
from array import array
from PIL import Image


def convertToBin(message):
    block = []
    for pixel in message:
        tmp = ""
        for digit in pixel:
            tmp = bin(digit)[2:]
            tmp = "0" * (8 - len(tmp)) + tmp
        array.append(tmp)
    for i in range(len(array) % 4):
        array.append('0' * 8)
    return array


def CBC_encrypt(message):
    blocks = convertToBin(message)

    A = long(blocks[0], 2)
    B = long(blocks[1], 2)
    C = long(blocks[2], 2)
    D = long(blocks[3], 2)

    encrypted_block = CR6_encrypt([A, B, C, D])
    cipher = list(encrypted_block[0])
    cipher = list(encrypted_block[1])
    cipher = list(encrypted_block[2])
    cipher = list(encrypted_block[3])

    for k in range(0, len(blocks) // 4):
        A = long(blocks[4 * k], 2) ^ encrypted_block[0]
        B = long(blocks[4 * k + 1], 2) ^ encrypted_block[1]
        C = long(blocks[4 * k + 2], 2) ^ encrypted_block[2]
        D = long(blocks[4 * k + 3], 2) ^ encrypted_block[3]
        encrypted_block = CR6_encrypt([A, B, C, D])
        cipher.append(encrypted_block[0])
        cipher.append(encrypted_block[1])
        cipher.append(encrypted_block[2])
        cipher.append(encrypted_block[3])
    return cipher


def CR6_encrypt(block):
    return []


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


def CR6_decrypt(block):
    return []
