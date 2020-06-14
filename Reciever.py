import socket
import pickle
import time
from tkinter.ttk import Progressbar

import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *
import tkinter as tk
import venv
from Communication import *

HOST, PORT = "localhost", 8000


def closeWindow(root):
    root.destroy()

def startDecrypting(root, frame, iframe6, cipherImage,cipheredPixels, s,progress):
    progress['value'] = 10
    root.update_idletasks()
    time.sleep(0.2)

    user1 = venv.DH_Endpoint(197, 151, 199)
    user2 = venv.DH_Endpoint(197, 151, 157)
    alicePartialKey = user1.generate_partial_key()
    bobPartialKey = user2.generate_partial_key()
    key = user1.generate_full_key(alicePartialKey)
    key = user2.generate_full_key(bobPartialKey)
    progress['value'] = 20
    root.update_idletasks()
    time.sleep(0.1)

    key = str(key)
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    RCKey = generateKey(key)
    progress['value'] = 30
    root.update_idletasks()
    time.sleep(0.1)

    enc = []
    de = deBlocker(cipheredPixels)
    for i in range(0, len(de), 4):
        enc.append(de[i:i + 4])
    # print("deBlocker (String): " +de)

    progress['value'] = 40
    root.update_idletasks()
    time.sleep(0.1)
    progress['value'] = 60
    root.update_idletasks()
    time.sleep(0.1)

    decryptedM = CBC_decrypt(enc, RCKey)

    print('len decrypted ' + str(len(decryptedM)))

    k = 0
    print(len(cipherImage)* len(cipherImage[0]))
    for i in range(len(cipherImage)):
        for j in range(len(cipherImage[0])):
                cipherImage[i][j] = int(decryptedM[k], base=10) % 256
                k = k + 1
        # print(cipherImage)
    progress['value'] = 80
    root.update_idletasks()
    time.sleep(0.1)
    cv2.imwrite('Recieverdecrypted.png', cipherImage)
    progress['value'] = 100
    root.update_idletasks()
    time.sleep(0.1)

    iframe6.destroy()
    iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(iframe7, text='Decrypted Image').pack()
    canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
    B = tk.Button(iframe7, text="Exit", command=lambda: closeWindow(root)).pack()
    canvas.pack()
    pic1 = tk.PhotoImage(file="Recieverdecrypted.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
    canvas.image = pic1




def main():
    # Client code:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (HOST, PORT)
        s.connect(server_address)

        root = tk.Tk()
        root.title("RECIEVER")
        frame = tk.Frame(root, width=400, height=500 + 20, bd=1)
        frame.pack()
        cipherImage = pickle.loads(recv_msg(s))
        cipheredPixels = pickle.loads(recv_msg(s))
        cv2.imwrite("reciedImage.png", cipherImage)
        iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe7, text='Encrypted Image').pack()
        canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
        B = tk.Button(iframe7, text="Decrypt",
                      command=lambda: startDecrypting(root, frame, iframe7, cipherImage, cipheredPixels, s,
                                                      progress)).pack()
        canvas.pack()
        pic1 = tk.PhotoImage(file="reciedImage.png")
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        canvas.image = pic1
        progress = Progressbar(iframe7, orient=tk.HORIZONTAL,
                               length=100, mode='determinate')
        progress.pack(pady=10)





        tk.mainloop()

if __name__ == "__main__":
    main()