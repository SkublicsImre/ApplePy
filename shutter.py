from PIL import Image
from random import randrange as rr
import numpy as np
import math as mt
import time

def save_img(npdata, outfilename):
    img = Image.fromarray(np.asarray(npdata, dtype="uint8"))
    img.save(outfilename)

def gen_rand_img(X,Y):
    img = []
    for x in range(X):
        imrow=[]
        for y in range(Y):
            R = (((y+rr(-9,10)/10)/Y))*255 
            G = 20
            B = 80
            imrow.append([R,G,B])
        img.append(imrow)
    return img

while True:
    print('gen')
    img = gen_rand_img(10,10)
    print('disp')
    save_img(img,'frame.png')
    print('sleep')
    time.sleep(1)