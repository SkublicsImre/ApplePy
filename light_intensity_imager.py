from matplotlib import pyplot as plt
from random import randrange as rr
from msvcrt import kbhit as kbh
import math as M
import serial

def presets():
    global COM, begin, t_out, savefile, area, cmap, w, h, x, y
    COM =  'COM3'
    begin = 115200
    t_out = 0.5
    savefile = 'LII_data.txt'
    x = 30
    y = 30
    area = x*y
    cmap = 'jet'
    w = 1
    h = 1

def get_ser_line():
    raw=ser.readline()
    raw=raw.decode("utf-8") 
    raw=raw.replace("'","")
    raw=raw.replace("b","")
    return raw

def call_colormap():
    global color_range #intiger
    global color #map reference
    color = plt.cm.get_cmap(cmap)
    print("calling colormap: "+str(cmap)+" ["+str(color.N)+"]")
    color_range = color.N

def getcolor(intensity):
    return color(intensity)

def write_measurements():
    global ser
    try:
        ser = serial.Serial(COM,begin,timeout=t_out)
    except serial.serialutil.SerialException:
        print("\nDevice not connected on "+ COM)
        menu()
    if not ser.isOpen():
        ser.open()
    print(COM + ' is open ->', ser.isOpen())
    f=open(savefile,'w')
    print("savefile "+savefile+" is open")
    print("waiting for data stream...")
    count=0
    firstdata=0
    while True:
        line = get_ser_line()
        f.write(line)
        if kbh():break
        if count==area:break
        if line!="":
            count+=1
            if firstdata==0:
                firstdata=1
                print("saving data stream...\n")
            print("\033[Fsaved lines:"+str(count)+" "+ str(int((count/area)*100))+" [%] ")
    print("data packet saved")
    f.close()

class pixel():
    def __init__(self,X_cord,Y_cord,intensity,width,height,highest,lowest):
        self.x=X_cord
        self.y=Y_cord
        self.i=((intensity-lowest)/(highest-lowest))
        self.w=width
        self.h=height
        self.color=getcolor(self.i)
    def plot(self):
        rectangle=plt.Rectangle((self.x,self.y), self.w, self.h, fc=self.color, ec=self.color)
        plt.gca().add_patch(rectangle)
        plt.axis('scaled')

def getmax(lst):
    mx = 0
    for i in lst:
        if i>mx: mx=i
    return mx

def getmin(lst):
    mn = 1024
    for i in lst:
        if i<mn: mn=i
    return mn

def read_measurements(name):
    global intensity_list
    global cord_list
    cord_list = []
    intensity_list = []
    print("opening file: " + name)
    f = open(name,'r')
    raw=f.read().replace("⸮","0")
    raw_list = raw.split('\n')
    print("copy file contents...")
    for i in raw_list:
        if i!='':
            I = i.split('\t')
            intensity_list.append(float(I[0]))
            cord_list.append([int(I[1]),int(I[2])])
    f.close()
    print("closing file " + name)

def gen_pixels():
    global pixel_list
    pixel_list = []
    mx = getmax(intensity_list)
    mn = getmin(intensity_list)
    print("generating pixels...\n")
    fin = intensity_list.__len__()
    for i in range(fin):
        pixel_list.append(pixel(cord_list[i][0],cord_list[i][1],intensity_list[i],w,h,mx,mn))
        print("\033[F"+str(int((i/fin)*100))+" [%] ")

def plot_pixels():
    print("drawing map...\n")
    count=0
    fin=pixel_list.__len__()
    for i in pixel_list:
        i.plot()
        count+=1
        print("\033[F"+str(int((count/fin)*100))+" [%] ")
    plt.show()
    menu()

def measure_live():
    call_colormap()
    write_measurements()
    read_measurements(savefile)
    gen_pixels()
    plot_pixels()

def gen_test_map(hp_num,noise):
    hp = []
    I = 0
    X = 0
    Y = 0
    count = 0
    fin = area
    print("\ngenerating random heatmap...\n")
    for i in range(hp_num):
        hp.append([rr(0,x),rr(0,y)])
    f = open(savefile,'w')
    for i in range(x):
        for j in range(y):
            Ilst = []
            for d in hp:
                Ilst.append(M.sqrt((d[0]-i)**2+(d[1]-j)**2))
            I = getmin(Ilst) + rr(-noise,noise)
            X = i
            Y = j
            f.write(str(I)+'\t'+str(X)+'\t'+str(Y)+"\n")
            print("\033[F"+str(int((count/fin)*100))+" [%] ")
            count += 1
    f.close()
    call_colormap()
    read_measurements(savefile)
    gen_pixels()
    plot_pixels()

def options():
    global COM, begin, savefile, area, cmap, x, y
    command = int(input("\n[1] Change port from "+COM+"\n[2] Change baudrate from "+str(begin)+"\n[3] Change savefile directory from "+savefile+"\n[4] Change colormap from "+cmap+"\n[5] Change dimensionsv from "+str(x)+", "+str(y)+"\n[6] Reset to default\n[7] Menu\n "))
    if command==1: COM = "COM" + str(input("\nSet "+COM+" to: "))
    elif command==2: begin = int(input("\nNew baudrate: "))
    elif command==3: savefile = input("\nNew savefile name ")
    elif command==4: 
        maplist = plt.colormaps()
        for i in maplist:
            print(i)
        cmap = input("Change colormap from "+cmap+" to: ")
    elif command==5: x = int(input("map width: ")); y = int(input("map height: ")); area = x*y; print(area)
    elif command==6: main()
    elif command==7: menu()
    else: print("Invalid command")
    options()

def Save_run(name):
    f = open(savefile,'r')
    raw = f.read()
    f.close
    f = open(name,'w')
    f.write(raw)

def Open_run(name):
    call_colormap()
    read_measurements(name)
    gen_pixels()
    plot_pixels()

def menu():
    x = int(input("\n[1] Run live\n[2] Options\n[3] Testrun\n[4] Save run\n[5] Open saved run\n[6] Exit\n "))
    if x==1:measure_live()
    elif x==2: options()
    elif x==3: num = int(input("number of heatpoints: ")); gen_test_map(num)
    elif x==4: sname = input("Save as: "); Save_run(sname)
    elif x==5: oname = input("Open file: "); Open_run(oname)
    elif x==6: exit()
    else: print("\ninvalid command")
    menu()

def main():
    presets()
    menu()

if __name__=='__main__':
    main()

print("NOOOO YOU CANT MULTIPLY STRINGS!")
print("haha python go b" + "r"*10)
#>> haha pytthon go brrrrrrrrrr
