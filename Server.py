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

# a server class used to connect the sender and the receiver
# it just forwards the reeived messages from each client to the other

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        client1, addr1 = s.accept()
        client2, addr2 = s.accept()
        print(client1)
        print(client2)
        with client1 and client2:
            print('Connected by', addr1)
            print('Connected by', addr2)
            isSender = pickle.loads(recv_msg(client1))
            isReciever =pickle.loads(recv_msg(client2))
            if isSender == 'sender':
                sender = client1
                reciever = client2
            else:
                sender = client2
                reciever = client1
            while True:

                SenderPublicKey = recv_msg(sender)
                RecieverPublicKey = recv_msg(reciever)
                send_msg(reciever,SenderPublicKey)
                send_msg(sender,RecieverPublicKey)

                print(pickle.loads(SenderPublicKey))
                print(pickle.loads(RecieverPublicKey))

                cipherImage = recv_msg(sender)
                cipherdPixels =recv_msg(sender)
                send_msg(reciever,cipherImage)
                send_msg(reciever,cipherdPixels)



if __name__ == "__main__":
    main()