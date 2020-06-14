import cv2 as c
import numpy as np
from helpers import *
from CBC_mode import *
import tkinter as tk
import venv
from Communication import *
import struct
import socket
import pickle

HOST, PORT = "localhost", 8000



def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        client, addr1 = s.accept()
        reciever, addr2 = s.accept()
        print(client)
        print(reciever)
        with client and reciever:
            print('Connected by', addr1)
            print('Connected by', addr2)
            while True:
                cipherImage = recv_msg(client)
                cipherdPixels =recv_msg(client)
                send_msg(reciever,cipherImage)
                send_msg(reciever,cipherdPixels)



if __name__ == "__main__":
    main()