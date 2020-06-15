import socket
import pickle
import time
from tkinter.ttk import Progressbar
import D_H
import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *
import tkinter as tk
import venv
from Communication import *
import threading
import D_H

HOST, PORT = "localhost", 8000

# a thread class used to update the GUI when the Image is receiver
class App(threading.Thread):

    def __init__(self, tk_root,frame,iframe6,sock,key):
        self.root = tk_root
        self.frame = frame
        self.iframe6 = iframe6
        self.sock = sock
        self.key = key
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        cipherImage = pickle.loads(recv_msg(self.sock))
        cipheredPixels = pickle.loads(recv_msg(self.sock))
        cv2.imwrite("Resources/reciedImage.png", cipherImage)
        self.iframe6.destroy();
        iframe7 = tk.Frame(self.frame, bd=2, relief=tk.RAISED)
        iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe7, text='Encrypted Image').pack()
        canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
        B = tk.Button(iframe7, text="Decrypt",
                      command=lambda: startDecrypting(self.root, self.frame, iframe7, cipherImage, cipheredPixels, self.sock,
                                                      progress,self.key)).pack()
        canvas.pack()
        pic1 = tk.PhotoImage(file="Resources/reciedImage.png")
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        canvas.image = pic1
        progress = Progressbar(iframe7, orient=tk.HORIZONTAL,
                               length=100, mode='determinate')
        progress.pack(pady=10)

# callback fuction to decrypt the Image
def startDecrypting(root, frame, iframe6, cipherImage,cipheredPixels, s,progress,key):
    progress['value'] = 10
    root.update_idletasks()
    time.sleep(0.2)

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
    cv2.imwrite('Resources/Recieverdecrypted.png', cipherImage)
    progress['value'] = 100
    root.update_idletasks()
    time.sleep(0.1)

    iframe6.destroy()
    iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(iframe7, text='Decrypted Image').pack()
    canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
    B = tk.Button(iframe7, text="Exit", command=lambda : root.destroy()).pack()
    canvas.pack()
    pic1 = tk.PhotoImage(file="Resources/Recieverdecrypted.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
    canvas.image = pic1




def main():
    # Client code:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (HOST, PORT)
        s.connect(server_address)

        send_msg(s,pickle.dumps('reciever'))

        DH = D_H.new(14)  # used diffie hellman to get the key used in the encryption
        key = DH.negotiate(s)  # smeding the public key to the reciever and recieving the public key of the reciever

        root = tk.Tk()
        root.title("RECIEVER")
        frame = tk.Frame(root, width=20, height=30, bd=1)
        frame.pack()
        iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe7, text='Please wait until the photo is recieved').pack()

        App(root,frame,iframe7,s,key)





        tk.mainloop()

if __name__ == "__main__":
    main()