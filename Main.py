import cv2 as c
import numpy as np

img = c.imread('tiger.jpg',0)


print(img)

c.imshow('original image',img)
k = c.waitKey(0)
if k == 27:
    c.destroyAllWindows()
elif k == ord('s'):
    c.imwrite('encrypted_Tiger.jpg' , img-2)
    c.destroyAllWindows()