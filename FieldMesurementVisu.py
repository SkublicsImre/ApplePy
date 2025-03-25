# 3d library
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

from random import randrange as rr

# simple calculations
import math as M

# for surface plotting
import numpy as np 

def ReadDronePath():
    # prepare containing lists (if only i knew numpy better...)
    xData=[]
    yData=[]
    zData=[]

    # Take user input for filename
    filename = input("Fájlnév: ")+".csv"
    f = open(filename,'r')
    data = f.read()
    f.close()

    # Unpack data
    data = data.replace(",",".")
    data = data.split("\n")
    for DataLine in data:
        DataPoints = DataLine.split("\t")
        taglimit = DataPoints.__len__()
        tag=1 #É,K,H,D,M
        for DataPoint in DataPoints:
                num = DataPoint
                print(num)
                if num != '':
                    if tag==1:xData.append(float(num))
                    elif tag==2:yData.append(float(num))
                    elif tag==3:zData.append(float(num))
                    tag+=1
                    if tag>=taglimit:tag=1

    return [xData,yData,zData]

def GenGain(res,dev,targetF,x,y,z):
    r = 10
    dev+=rr(-9,10)
    targetF+=rr(-10,11)
    dist = M.sqrt((0-x)**2+(r+0.1-y)**2+(20-z)**2)
    mdist = M.sqrt((0)**2+(r)**2+(20)**2)
    amp=abs(mdist-dist)*20
    print(str(targetF)+"\t"+str(dev)+"\t"+str(amp))
    mList = []
    step = 240/res
    for i in range(res):
        mList.append( ( 1/ (dev*M.sqrt(2*M.pi)) ) * M.e**(-1/2 * ((((i*step-targetF)/dev))**2) )*amp+rr(0,3) )
    return mList



def GenerateTestData():
    xData=[]
    yData=[]
    zData=[]
    mData=[]
    
    x = 0
    y = 0
    z = 20
    R = 10
    nVertical = 5
    nHorisontal = 7
    FieldAngle = 1

    stepList = []
    VerticalStep = FieldAngle*2*R/nVertical
    HorisontalStep = 2*M.pi/nHorisontal #rads
    midx = x
    midy = y
    midz = z

    res = 20

    #starting from the top down we approach the object
    z += R

    #calculate measuring coordinates (+= iterator is needed so we dont start measuring from a 0 Radius)
    for nHstep  in range(nVertical):
        #calculate plane radius at given height ((R-nStep)^2 + PlaneRadius^2 = R^2)
        nHstep += 1
        PlaneRadius = M.sqrt(R**2-(R - VerticalStep*nHstep)**2)
        x = midx+PlaneRadius
        y = midy
        z -= VerticalStep
        stepList.append([x,y,z,GenGain(50,10,100,x,y,z)])

        #Calculate single points for the given plane
        for nDeg in  range(nHorisontal):
            deg = HorisontalStep*nDeg

            rot = deg+M.pi
            if rot>2*M.pi:rot-=2*M.pi
            rot=(rot/(2*M.pi))*360
            
            y = midy+PlaneRadius*M.sin(deg)
            x = midx+PlaneRadius*M.cos(deg)
            stepList.append([x,y,z,GenGain(50,10,100,x,y,z)])
    
    for i in stepList:
        xData.append(i[0])
        yData.append(i[1])
        zData.append(i[2])
        mData.append(i[3])

    return [xData,yData,zData,mData,R*111000.0001]


def Display(xData,yData,zData,mData,r):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.ion()

    resLen = mData[0].__len__()
    dLen = mData.__len__()
    pointer = 0
    inc = 1
    d = r/10
    s = 1.5*r
    Mx = max(mData[0])
    while True:#plt.fignum_exists(1):#pointer <= resLen:
        R = []
        for i in mData:
            #mn = min(i)
            mx = max(i)
            R.append((i[pointer]/mx)*d+r)
        pointer += inc
        if pointer>=resLen: pointer=resLen-1; inc=-1
        if pointer<0: pointer=0; inc=1

        # draw measured field  
        R = np.array(R)
        R = np.outer(R,R)
        u = np.linspace(0, 2*np.pi, dLen)
        v = np.linspace(0, np.pi, dLen)
        xs = R * np.outer(np.cos(u), np.sin(v))
        ys = R * np.outer(np.sin(u), np.sin(v))
        zs = R * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(xs, ys, zs, color='red',alpha=0.9, zorder=0.7)

        ax.plot3D([-(s**2+Mx),(s**2+Mx)],[-(s**2+Mx),(s**2+Mx)],[-(s**2+Mx),(s**2+Mx)],alpha=0.01)

        #if plt.fignum_exists(1):break
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_aspect('equal')
        plt.show()
        plt.pause(0.001)
        plt.cla()

def displayGain(mData):
    fig = plt.figure()
    ax = plt.axes()
    plt.ion()
    while True:
        for dataset in mData:
            xs=(list(range(0,dataset.__len__())))
            ys=dataset
            ax.plot(xs,ys,color='red')
            plt.show()
            plt.pause(0.01)
            plt.cla()
       

d = GenerateTestData()
#displayGain(d[3])
Display(d[0],d[1],d[2],d[3],d[4])

