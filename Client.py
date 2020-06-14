import socket
import pickle
import time
import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *
import tkinter as tk
from tkinter.ttk import *
import venv
from Communication import *
from tkinter.filedialog import askopenfilename

HOST, PORT = "localhost", 8000


def closeWindow(root):
    root.destroy()


def startEncrypting(root, frame, iframe5, img, sock, progress):
    orginalPixels = ConvertImageToStringArray(img)
    print(len(orginalPixels))
    user1 = venv.DH_Endpoint(197, 151, 199)
    user2 = venv.DH_Endpoint(197, 151, 157)
    alicePartialKey = user1.generate_partial_key()
    bobPartialKey = user2.generate_partial_key()
    key = user1.generate_full_key(alicePartialKey)
    key = user2.generate_full_key(bobPartialKey)
    key = str(key)
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    progress['value'] = 10
    root.update_idletasks()

    RCKey = generateKey(key)
    print(orginalPixels)

    encrypted = []
    cipheredPixels = CBC_encrypt(orginalPixels, RCKey)

    progress['value'] = 20
    root.update_idletasks()
    time.sleep(0.1)
    progress['value'] = 30
    root.update_idletasks()
    time.sleep(0.1)

    cipherImage = np.empty([len(img), len(img[0])], dtype=int)

    progress['value'] = 40
    root.update_idletasks()
    time.sleep(0.1)
    progress['value'] = 60
    root.update_idletasks()
    time.sleep(0.1)

    k = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            cipherImage[i][j] = cipheredPixels[k] % 256
            k = k + 1

    progress['value'] = 80
    root.update_idletasks()
    time.sleep(0.1)

    progress['value'] = 100
    root.update_idletasks()
    time.sleep(0.1)

    cv2.imwrite('encrypted.png', cipherImage)
    print('len original' + str(len(orginalPixels)))

    BcipherImage = pickle.dumps(cipherImage)
    BcipheredPixel = pickle.dumps(cipheredPixels)
    send_msg(sock, BcipherImage)
    send_msg(sock, BcipheredPixel)

    iframe5.destroy()
    iframe6 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe6.pack(expand=1, fill=tk.X, pady=10, padx=5)
    B = tk.Button(iframe6, text="Exit", command=lambda: closeWindow(root)).pack()
    label = tk.Label(iframe6, text='Original Image').pack()
    canvas = tk.Canvas(iframe6, width=len(img[0]) + 20, height=len(img) + 20)
    canvas.pack()
    pic1 = tk.PhotoImage(file="original.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
    canvas.image = pic1


def OpenPicture(root, frame, iframe5, s):
    url = askopenfilename()
    print(url)
    if url.endswith(".png") or url.endswith(".jpg"):
        img = c.imread(url, 0)
        c.imwrite("original.png",img)
        img = c.imread('original.png',0)
        url = 'original.png'
        iframe5.destroy()

        iframe6 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe6.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe6, text='Orginal Image').pack()
        canvas = tk.Canvas(iframe6, width=len(img[0]) + 20, height=len(img) + 30)
        B = tk.Button(iframe6, fg='#85D426', bg='#e0163b', text="Encrypt and SEND",
                      command=lambda: startEncrypting(root, frame, iframe6, img, s, progress)).pack()
        global pic1
        pic1 = tk.PhotoImage(file=url)
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        progress = Progressbar(iframe6, orient=tk.HORIZONTAL,
                               length=100, mode='determinate')
        canvas.pack()

        progress.pack(pady=10)



def main():
    # Client code:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (HOST, PORT)
        s.connect(server_address)
        # url = input()
        # url = "tiger.jpg"
        # img = c.imread(url, 0)
        # # Checking if the img is exist
        # if img is None:
        #     popupmsg("No photo found!")
        #     return;
        # cv2.imwrite('1111.png', img)


        root = tk.Tk()
        root.title("SENDER")
        frame = tk.Frame(root, width=20, height=20, bd=1)
        frame.pack()
        iframe5 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe5.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe5, text='Please choose picture to encrypt and send').pack()
        B = tk.Button(iframe5, fg='#85D426', bg='#e0163b', text="Open File",
                      command=lambda: OpenPicture(root, frame, iframe5, s)).pack()

        tk.mainloop()


if __name__ == "__main__":
    main()
