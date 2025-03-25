import numpy as np
import wave 
import struct
import matplotlib.pyplot as plt

import serial
import time

#arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def read():
    #time.sleep(0.05)
    dt = arduino.readline()
    dt=str(dt)
    dt=list(dt)
    if dt.__len__()>=5:
      dt=dt[2]+dt[3]+dt[4]
    return dt

d=0
data=[]
count=0
while count<=100:
   d=0#read()
   try:
      data.append(int(d))
      #print(d)
      
   except:
      print("invalid value")
   count+=1

data = [np.sin(2*np.pi*(100+np.random.randint(100)/100)*x/9600)+(np.sin(2*np.pi*(120+np.random.randint(100)/100)*x/9600)) for x in range(100000)]
OG_data = data
plt.plot(data)
plt.figure()
amplitude=1
frame_rate = 9600
filename = "sound.wav"

nframes=data.__len__()

freqs=np.abs(np.fft.fft(data))
data=np.zeros(nframes)
mx=max(freqs)
mxin=np.argpartition(freqs, -5)[-5:]
prevf=0
curfreq=0
for f in mxin:
   if (prevf<=f-10 or prevf>=f+10) and (f<=20000 and f>=20):
      data+=[np.sin(2 * np.pi * f * x/frame_rate )*freqs[f] for x in range(nframes)]
      prevf=f


plt.plot(freqs)
plt.figure()
plt.plot(data)
plt.show()

comptype="NONE"
compname="not compressed"
nchannels=1
sampwidth=2
wav_file = wave.open(filename, 'w')
wav_file.setparams((nchannels, sampwidth, int(frame_rate), nframes, comptype, compname))
for s in data:
   wav_file.writeframes(struct.pack('h', int(s*amplitude)))
wav_file.close()

wav_file = wave.open('OG_'+filename, 'w')
wav_file.setparams((nchannels, sampwidth, int(frame_rate), nframes, comptype, compname))
for s in OG_data:
   wav_file.writeframes(struct.pack('h', int(s*amplitude)))
wav_file.close()
