import serial
import time
from matplotlib import pyplot as plt
import msvcrt 

def presets():
    global COM, begin, t_out, start, Tlst, tlst
    COM =  'COM3'
    begin = 9600
    t_out = 1
    start = time.time()
    Tlst = []
    tlst = []

def get_ser_line():
    print("reading...")
    raw=ser.readline()
    #time.sleep(0.1)
    raw=raw.decode("utf-8") 
    raw=raw.replace("'","")
    raw=raw.replace("b","")
    raw=raw.replace("\n","")
    if raw is None or raw == "":get_ser_line()
    else: return raw

def write_measurements():
    global ser, start, tlst, Tlst
    
    try:
        ser = serial.Serial(COM,begin,timeout=t_out)
    except serial.serialutil.SerialException:
        print("\nDevice not connected on "+ COM)
        exit()
    if not ser.isOpen():
        ser.open()
    print(COM + ' is open ->', ser.isOpen())
    
    #etime.sleep(5)
    start = time.time()
    plt.ion()
    while True:
        line = get_ser_line()
        print(line)
        if line is not None:
            Tlst.append(float(line))
            ctime = time.time()
            tlst.append(ctime-start)
            plt.cla()
            plt.plot(tlst,Tlst)
            plt.draw()
            plt.pause(0.001)
        if msvcrt.kbhit():break




if __name__ == '__main__':
    presets()
    write_measurements()
