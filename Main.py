import cv2 as cv2
import numpy as np
from CBC_mode import *
import tkinter as tk
import venv
import time

def closeWindow(root):
    root.destroy()

def startDecrypting(root,frame,iframe6,cipherImage,cipheredPixels,orginalPixels,encrypted,RCKey,img):
     print("Original pixels (String): " + str(orginalPixels))
     print("Encrypted pixels (long): " + str(cipheredPixels))
     print("Encrypted pixels (String): " + str(encrypted))
     enc = []                            # list of string blocks
     de = deBlocker(cipheredPixels)     # string
     for i in range (0,len(de),4):
         enc.append(de[i:i+4])
    # print("deBlocker (String): " +de)
     decryptedM =  CBC_decrypt(enc,RCKey)
     print("Decrypted pixels: "+ str(decryptedM))
     print("Original pixels : " + str(orginalPixels))

     # for i in range(0,len(decryptedM)):
     #     if decryptedM[i] != orginalPixels[i]:
     #         print(decryptedM[i])

     k = 0
     print("size of image     = ",str(len(img)*len(img[0])) )
     print("size of decrepted = ",len(decryptedM))
     for i in range(len(img)):
         for j in range(len(img[0])):
             cipherImage[i][j] = decryptedM[k]
             k = k + 1
         # print(cipherImage)

     cv2.imwrite('Resources/decrypted.png', cipherImage)

     iframe6.destroy()
     iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
     iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
     label = tk.Label(iframe7, text='Decrypted Image').pack()
     canvas = tk.Canvas(iframe7, width=len(img[0]) + 20, height=len(img) + 20)
     B = tk.Button(iframe7, text="Exit",command = lambda :closeWindow(root)).pack()
     canvas.pack()
     pic1 = tk.PhotoImage(file="Resources/decrypted.png")
     canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
     canvas.image = pic1
     global timer2
     timer2 = time.perf_counter()
     print(f"Downloaded the tutorial in {timer2 - timer1:0.4f} seconds")


def startEncrypting(root,frame,iframe5,img):
    # img = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    global timer1
    timer1 = time.perf_counter()

    orginalPixels = ConvertImageToStringArray(img)    # string list
    print("size of orginalPixels = ", len(orginalPixels))

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
    RCKey = generateKey(key)
    print(orginalPixels)

    encrypted = []
    cipheredPixels = CBC_encrypt(orginalPixels, RCKey)   # long

    cipherImage = np.empty([len(img) , len(img[0]) ], dtype=int)    #long/int

    k = 0
    # for i in range(len(img)):
    #     for j in range(len(img[0])):
    #         cipherImage[i][j] = cipheredPixels[k] % 256
    #         k = k + 1
    #
    # cv2.imwrite('Resources/encrypted.png', cipherImage)
    # B['text'] = 'decrypt'
    # B['command'] = lambda : startDecrypting()
    # pic1['file'] = 'encrypted.png'
    # label['text'] = 'Encrypted pic'
    iframe5.destroy()
    iframe6 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe6.pack( expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(iframe6, text='Encrypted Image').pack()
    canvas = tk.Canvas(iframe6, width=len(img[0]) + 20, height=len(img) + 20)
    B = tk.Button(iframe6,bg = '#85D426',fg = '#e0163b', text="Decrypt", command=lambda: startDecrypting(root,frame,iframe6,cipherImage,cipheredPixels,orginalPixels,encrypted,RCKey,img)).pack()
    canvas.pack()
    pic1 = tk.PhotoImage(file="Resources/encrypted.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
    canvas.image = pic1


def main():

    print("Please enter image url:")
    #url = input()
    url = "Resources/1111.jpg"
    img = cv2.imread(url,0)
    #Checking if the img is exist
    if img is None:
        popupmsg("No photo found!")
        return;
    cv2.imwrite('Resources/1111.png', img)

    root = tk.Tk()
    frame = tk.Frame(root, width=len(img[0]) + 20, height=len(img) + 20, bd=1)
    frame.pack()

    iframe5 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe5.pack( expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(iframe5, text='Orginal Image').pack()
    canvas = tk.Canvas(iframe5, width=len(img[0]) + 20, height=len(img) + 20)
    B = tk.Button(iframe5,fg = '#85D426',bg = '#e0163b' ,text="Encrypt", command=lambda: startEncrypting(root,frame,iframe5,img)).pack()
    canvas.pack()
    pic1 = tk.PhotoImage(file="Resources/1111.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)



    tk.mainloop()
if __name__ == "__main__":
    main()