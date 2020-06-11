import math
import numpy

#rotate right input x, by n bits
def ROR(x, n, bits = 32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

#rotate left input x, by n bits
def ROL(x, n, bits = 32):
    return ROR(x, bits - n,bits)

#convert input sentence into blocks of binary
#creates 4 blocks of binary each of 32 bits.
def blockConverter(sentence):
    encoded = []
    res = ""
    for i in range(0,len(sentence)):
        if i%4==0 and i!=0 :
            encoded.append(res)
            res = ""
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) <8:
            temp = "0"*(8-len(temp)) + temp
        res = res + temp
    encoded.append(res)
    return encoded

#converts 4 blocks array of long int into string
def deBlocker(blocks):
    s = ""
    for ele in blocks:
        temp =bin(ele)[2:]
        if len(temp) <32:
            temp = "0"*(32-len(temp)) + temp
        for i in range(0,4):
            s=s+chr(int(temp[i*8:(i+1)*8],2))
    return s

#generate key s[0... 2r+3] from given input string userkey
def generateKey(userkey):
    r=12
    w=32
    b=len(userkey)
    modulo = 2**32
    s=(2*r+4)*[0]
    s[0]=0xB7E15163
    for i in range(1,2*r+4):
        s[i]=(s[i-1]+0x9E3779B9)%(2**w)
    encoded = blockConverter(userkey)
    #print encoded
    enlength = len(encoded)
    l = enlength*[0]
    for i in range(1,enlength+1):
        l[enlength-i]= numpy.long(encoded[i - 1], 2)
    
    v = 3*max(enlength,2*r+4)
    A=B=i=j=0
    
    for index in range(0,v):
        A = s[i] = ROL((s[i] + A + B)%modulo,3,32)
        B = l[j] = ROL((l[j] + A + B)%modulo,(A+B)%32,32) 
        i = (i + 1) % (2*r + 4)
        j = (j + 1) % enlength
    return s

    #A method that gets an img matrix and convert it to a string list each elemnt size of 32bit
def ConvertImageToStringArray(img):
    temp = '\n'.join('\t'.join('%0.0f' % x for x in y) for y in img)
    imgString = temp.split()
    print("Image pixles number : " + str(len(imgString)))
    for i in range(0, len(imgString)):
        if len(imgString[i]) < 4:
            imgString[i] = "0" * (4 - len(imgString[i])) + imgString[i]
    if len(imgString)%4 != 0:
       imgString = imgString + ["0000"]*(4 - (len(imgString)%4))
    return  imgString

def DiffeHellman():
  #  return "A WORD IS A WORD"
    return  '1234123412341234'


def xor_two_str(Mblocks,Cblocks):
    xored = []
    # print(type(Mblocks))
    # print(type(Cblocks))
    print(Mblocks)
    print(Cblocks)
    print(len(Cblocks))
    for i in range(max(len(Mblocks), len(Cblocks))):
        xored_value = ord(Mblocks[i%len(Mblocks)]) ^ ord(Cblocks[i%len(Cblocks)])
        xored.append(chr(xored_value))
    print(xored)

    return ''.join(xored)

# A method that gets 1 String of lenth 16 chars and convert it to list of 4 block each block 4 chars
def StringToBlocks(cipherString):
    cipherBlocks=[]
    cipherBlocks = [cipherString[i:i+4] for i in range(0, len(cipherString), 4)]
    return cipherBlocks


