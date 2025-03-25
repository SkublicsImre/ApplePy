from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math as mt

def save_img(npdata, outfilename):
    img = Image.fromarray(np.asarray(npdata, dtype="uint8"))
    img.save(outfilename)

cList=[' ','.',"'",':',';','?','+','*','@','&','#']
def cMap(num):
    inum=int((1-num/255)*cList.__len__())
    return cList[inum]


def print_img(dataArray):
    print('\033[0;0H')
    for row in dataArray:
        nRow=''
        for point in row:
            nRow+=cMap((point[0]+point[1])/2)+' '
        print(nRow)

def norm(lst, nVal):
    mx = max(lst)
    mn = min(lst)
    if mn==mx:
        return [1*nVal]*lst.__len__()
    else:mx-=mn
    nlst = []
    for i in lst:
        i-=mn
        i/=mx
        i=1-i
        i*=nVal
        nlst.append(i)
    return nlst

def gen_Fractal(H,W,Y0,Y1,X0,X1,res,exitC,progress):
    if progress:print("generating Field \n"+str(W*H)+" pixels")
    
    def mandelbrot(c):
        z = 0
        n = 0
        while abs(z) <= exitC and n < res:
            #z = z*z + c
            pol=1
            att=(z**0+z+z**2-z**3)*c
            if abs(pol) !=0:z = att/(pol)
            else: z += c
            n += 1
        return [abs(z),n,abs(c)]
        #print(abs(z))
        #return n

    if progress:print("generating pixel values\n")
    img = []
    Ilst = []
    Ilst_2 = []
    Ilst_3 = []
    for x in range(0,W):
        for y in range(0,H):
            c = complex(X0+(x/W)*(X1-X0),Y0+(y/H)*(Y1-Y0))
            data = mandelbrot(c)
            Ilst.append(data[0])
            Ilst_2.append(data[1])
            Ilst_3.append(data[2])
        if progress:print("\033[F"+str(int((x*y/(W*H))*100))+" [%] ")
    
    if progress: print("\nassembling image\n")
    Ilst = norm(Ilst,255)
    Ilst_2 = norm(Ilst_2,255)
    Ilst_3 = norm(Ilst_3,255)
    col = []
    count = 0
    co = 0
    fin = Ilst.__len__()
    for i in range(Ilst.__len__()):
        R = Ilst[i]
        G = Ilst_3[i]
        B = Ilst_2[i]
        col.append([R,G,B])
        count+=1
        if count == H:
            if progress: print("\033[F"+str(int((co/fin)*100))+" [%] ")
            img.append(col)
            col = []
            count = 0
        co += 1

    return img

pngMode=False
printMode=False
tinc=0
mid=(0.64900,0.0107)
zoom=1/1
exitC=2
#size=(2*zoom,3*zoom)
size=(2*zoom,3*zoom)
res=1
depth=80

if pngMode:
    #gen png
    pic = gen_Fractal(int(480*res),int(720*res),mid[0]-size[0]/2,mid[0]+size[0]/2, mid[1]-size[1]/2,mid[1]+size[1]/2, depth,exitC,True)
    save_img(pic,'img.png')

elif printMode:
    #gen print
    pic = gen_Fractal(int(720*res),int(480*res),mid[0]-size[0]/2,mid[0]+size[0]/2, mid[1]-size[1]/2,mid[1]+size[1]/2, depth,exitC,False)
    print_img(pic)
