# clear terminal
print("\033c", end="\033[A")

# import libs
import wave 
from scipy.fft import fft
import numpy as np
import math as M
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip as ISC
import tkinter as tk

from time import sleep as hold

# Declare global variables
div = 1		        # image scaleing
shift = [0.5,0.65]	# image shift from midpoint
X = int(80/div)    # image width (1480)
Y = int(80/div)     # image height (720)

zm = 6  # zoom
ex = 3  # exit condition
bl = 5 # bail condition
cnt = 0 # counter for wave iteration
step = 0.063 # step size

# Wave property matrix
A1 = 1.80;  A2 = 1.70;  A3 = 1.90;  A4 = 1.40
f1 = 1.00; f2 = 1.00;  f3 = 4.00;  f4 = 2.00
o1 = 0.30;  o2 = 1.80;  o3 = 2.20;  o4 = 20.20
l1 = 1.80;  l2 = 1.50;  l3 = 1.60;  l4 = 1.30

# Greyscale character list Bright to dark
#gscale = ["$","@","B","%","8","&","W","M","#","*","o","a","h","k","b","d","p","q","w","m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","(",")","1","{","}","[","]","?","-","_","+","~","<",">","i","!","l","I",";",":","^","`","'","."," "]
gscale = ["B","8","W","M","o","a","h","k","b","d","p","q","w","m","Z","O","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","(",")","1","[","]","-","+","<",">","i","l","I",":","."," "]
gres = gscale.__len__()-1 #scale lenght

filename = 'output'
cmapName = 'plasma'
soundFileName = 'Snow Crystal'

# Function to generate 2d 0-list
def nullField():
	global X, Y
	field=np.zeros((X, Y))
	return field

def mapToRGB(vals):
	global cmapName

	cmap=plt.get_cmap(cmapName)

	rgba = cmap(vals)

	r_weight = 0.7
	g_weight = 0.8
	b_weight = 0.6
	
	r = ((rgba[:,:,0]) * 255 * r_weight).astype(int)
	g = ((rgba[:,:,1]) * 255 * g_weight).astype(int)
	b = ((rgba[:,:,2]) * 255 * b_weight).astype(int)

	return r, g, b

# Function to normalise 2d list	
def norm(field,target,roundTo,isColor):
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres
	nfield=nullField()

	# Find maximum value
	maxpoint = np.max(field)
	minpoint =  np.min(field)
	
	# Exclude homogen
	if maxpoint-minpoint == 0: return nfield 
	else: # Normalise as specified
		if roundTo!=0:
			nfield = np.round(((field - minpoint) / (maxpoint - minpoint) * target), roundTo)
		elif isColor:
			nfield = 1 - ((field - minpoint) / (maxpoint - minpoint))
			ncfield = np.zeros((X, Y, 3))
			Rvals, Gvals, Bvals = mapToRGB(nfield)
			ncfield[:,:,0]=nfield*Rvals
			ncfield[:,:,1]=nfield*Gvals
			ncfield[:,:,2]=nfield*Bvals
			nfield = np.round(ncfield).astype(int)
		else:
			nfield = np.round(((field - minpoint) / (maxpoint - minpoint) * target)).astype(int)
	return nfield

# Function to draw image
def PreviewField(field):
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres
	field=np.rot90(field,k=3)
	nfield = ""
	for line in field:
		nline = ""
		for point in line:
			nline += " " + gscale[point] # match to gscale
		nfield += nline + "\n"
	return nfield

# Function to generate points in fractal
def F(x,y,n1,n2,n3,n4):
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres
	
	# Match points to image scale
	i = ( (x/X)*1 - shift[0])*zm
	j = ( (y/Y)*1 - shift[1])*zm
	
	# Declare local variables
	c = complex(j,i)
	z = c
	count = 0
	
	# Iterate the mandelbrot equation
	if z != 0:
		while count <= bl:
			z = ( z**n4 + z**n3 + z**n2 + z**n1 + c)/(n1-n2-n3-n4)
			count += 1
			if abs(z) >= ex: break
			
	return abs(z) # return value at exit or bail

def runDemo(vidLenght):
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres, filename
	
	Fps = 30
	nFr=vidLenght*Fps
	Gif=np.zeros((nFr,X,Y,3))
	
	for i in range(nFr):

		# Wave values
		a1 = A1*M.sin(cnt*f1 + o1) + l1
		a2 = A2*M.sin(cnt*f2 + o2) + l2
		a3 = A3*M.sin(cnt*f3 + o3) + l3
		a4 = A4*M.sin(cnt*f4 + o4) + l4
		
		# Iterate trough 2d list
		VideoFrame = nullField()
		for y in range(Y):
			for x in range(X):
				VideoFrame[y][x] = F(x,y,a1,a2,a3,a4) # find mandelbrot values

		validFrame = abs((norm(VideoFrame,256,0,True)))
		Gif[i,:,:,:]=(validFrame)

		cnt += step

	Gif = np.array(Gif)
	return Gif
		
	# save Gif
	clip=ISC(list(Gif),fps=Fps)
	clip.write_gif(filename + '.gif', Fps)


def Render(vidLenght):
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres, filename
	
	Fps = 30
	nFr=vidLenght*Fps
	Gif=np.zeros((nFr,X,Y,3))
	
	print("Rendering...\n")
	for i in range(nFr):

		# Wave values
		a1 = A1*M.sin(cnt*f1 + o1) + l1
		a2 = A2*M.sin(cnt*f2 + o2) + l2
		a3 = A3*M.sin(cnt*f3 + o3) + l3
		a4 = A4*M.sin(cnt*f4 + o4) + l4
		
		# Iterate trough 2d list
		VideoFrame = nullField()
		for y in range(Y):
			for x in range(X):
				VideoFrame[y][x] = F(x,y,a1,a2,a3,a4) # find mandelbrot values

		validFrame = abs((norm(VideoFrame,256,0,True)))
		Gif[i,:,:,:]=(validFrame)

		cnt += step

		print('\r\033['+str(3)+'A') # move cursor to print over previous line
		print("Generated "+str(round(((i+1)/nFr*100),2))+"%\n") # display progress
		#print(validFrame)
		
	# save Gif
	clip=ISC(list(Gif),fps=Fps)
	clip.write_gif(filename + '.gif', Fps)

def BuiuldUI():
	global root	# root window
	root = tk.Tk()
	root.geometry('1000x600')
	root.resizable(False, False)
	root.title('Frequency-based feature extraction to 4 polinome fractal')

def extractAudio():
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres 
	
	wav_file = wave.open(soundFileName + '.wav', 'rb')
	params = wav_file.getparams()
	sample_rate = params.framerate
	num_channels = params.nchannels
	sample_width = params.sampwidth
	num_samples = params.nframes
	frames = wav_file.readframes(params.nframes)
	signal = np.frombuffer(frames, dtype=np.int16)
	wav_file.close()

	ngFrames = int(30*(num_samples/sample_rate)) - 15

	a1=[]
	a2=[]
	a3=[]
	a4=[]

	for i in range(ngFrames):

		subFreqDomain = fft(signal[i:i+14])
		freqRange = len(subFreqDomain)
		a1.append(np.max(subFreqDomain[0:int(freqRange/4)]))
		a2.append(np.max(subFreqDomain[int(freqRange/4):int(freqRange/2)]))
		a3.append(np.max(subFreqDomain[int(freqRange/2):int(freqRange/4*3)]))
		a4.append(np.max(subFreqDomain[int(freqRange/4*3):int(freqRange)]))

	print(subFreqDomain)

def main():
	global div, shift, X, Y, zm, ex, bl, cnt, A1, A2, A3, A4, f1, f2, f3, f4, o1, o2, o3, o4, l1, l2, l3, l4, gscale, gres 
	
	vidLenght=10
	
	print("Starting up...")
	hold(1)
	print("Building user interface...")
	BuiuldUI() # build UI window

	# slider example
	#def slider_changed(event=None):
	#	slider_label.configure(text='{: .2f}'.format(slider_value.get()))
	#slider_value = tk.DoubleVar()
	#slider = ttk.Scale(root,from_=0,to=4,orient='horizontal',command=slider_changed,variable=slider_value)
	#slider.grid(column=10,row=5,sticky='we')
	#slider_label = ttk.Label(root,text='{: .2f}'.format(slider_value.get()))
	#slider_label.grid(row=5,columnspan=2,sticky='n')

	# open soundfile button
	def openCallback():
		extractAudio()
	gen=tk.Button(root, text="Open", command=openCallback)
	gen.place(x=50,y=0)

	# soundfile name input
	def savesFilename(event=None):
		global filename
		try:
			soundFileName = str(sfileEntry.get())
			sfileLabel.config(text='sound-file name: '+soundFileName)
		except:
			print('Invalid sound filename')
	sfileEntry=tk.Entry(root, width=10)
	sfileEntry.bind('<Return>',savesFilename)
	sfileEntry.place(x=100,y=0)
	sfileLabel=tk.Label(root, text='sound-file name: '+soundFileName)
	sfileLabel.place(x=150,y=0)

	# generate button
	def genCallback():
		global cnt
		cnt=0
		print("\033c", end="\033[A")
		Render(vidLenght)
		print("\033c", end="\033[A")
	gen=tk.Button(root, text="Render", command=genCallback)
	gen.place(x=50,y=50)

	# savefile name input
	def saveFilename(event=None):
		global filename
		try:
			filename = str(fileEntry.get())
			fileLabel.config(text='filename: '+filename)
		except:
			print('Invalid filename')
	fileEntry=tk.Entry(root, width=10)
	fileEntry.bind('<Return>',saveFilename)
	fileEntry.place(x=100,y=55)
	fileLabel=tk.Label(root, text='filename: '+filename)
	fileLabel.place(x=150,y=55)

	# preview button
	canvas=tk.Canvas(root, height=X, width=2*Y)
	canvas.place(x=400,y=0)
	#TxtBx.pack()
	def preCallback():
		global cnt
		cnt=0
		Fields=runDemo(vidLenght)
		for Field in Fields:
			canvas.create_image(20, 20, anchor='nw', image=Field)
			canvas.update()
			hold(0.05)
			canvas.delete(1.0,tk.END)
		
	prevButton=tk.Button(root, text="Preview", command=preCallback)
	prevButton.place(x=50,y=100)

	# zoom variable input
	def saveZoomVal(event=None):
		global zm
		try:
			zm = float(zoomEntry.get())	
			zoomLabel.config(text='zoom:\t'+str(round(zm,2)))
		except:
			print('Invalid zoom value')
	zoomEntry=tk.Entry(root, width=10)
	zoomEntry.bind('<Return>',saveZoomVal)
	zoomEntry.place(x=50,y=150)
	zoomLabel=tk.Label(root, text='zoom:\t'+str(round(zm,2)))
	zoomLabel.place(x=100,y=150)

	# exit variable input
	def saveExitVal(event=None):
		global ex
		try:
			ex = float(exitEntry.get())	
			exitLabel.config(text='exit:\t'+str(round(ex,2)))
		except:
			print('Invalid exit value')
	exitEntry=tk.Entry(root, width=10)
	exitEntry.bind('<Return>',saveExitVal)
	exitEntry.place(x=50,y=175)
	exitLabel=tk.Label(root, text='exit:\t'+str(round(ex,2)))
	exitLabel.place(x=100,y=175)

	# bail variable input
	def saveBailVal(event=None):
		global bl
		try:
			bl = int(bailEntry.get())	
			bailLabel.config(text='bail:\t'+str(round(bl,2)))
		except:
			print('Invalid bail value')
	bailEntry=tk.Entry(root, width=10)
	bailEntry.bind('<Return>',saveBailVal)
	bailEntry.place(x=50,y=200)
	bailLabel=tk.Label(root, text='bail:\t'+str(round(bl,2)))
	bailLabel.place(x=100,y=200)
	
	# image midpoint x variable input
	def saveSWidthVal(event=None):
		global shift
		try:
			shift[0] = float(shiftxEntry.get())	
			shiftxLabel.config(text='midX:\t'+str(round(shift[0],2)))
		except:
			print('Invalid midpoint value')
	shiftxEntry=tk.Entry(root, width=10)
	shiftxEntry.bind('<Return>',saveSWidthVal)
	shiftxEntry.place(x=50,y=225)
	shiftxLabel=tk.Label(root, text='midX:\t'+str(round(shift[0],2)))
	shiftxLabel.place(x=100,y=225)

	# image midpoint y variable input
	def saveSHeightVal(event=None):
		global shift
		try:
			shift[1] = float(shiftyEntry.get())	
			shiftyLabel.config(text='midY:\t'+str(round(shift[1],2)))
		except:
			print('Invalid midpoint value')
	shiftyEntry=tk.Entry(root, width=10)
	shiftyEntry.bind('<Return>',saveSHeightVal)
	shiftyEntry.place(x=50,y=250)
	shiftyLabel=tk.Label(root, text='midY:\t'+str(round(shift[1],2)))
	shiftyLabel.place(x=100,y=250)

	# image width variable input
	def saveWidthVal(event=None):
		global X
		try:
			X = int(xEntry.get())	
			xLabel.config(text='width:\t'+str(round(X,2)))
		except:
			print('Invalid width value')
	xEntry=tk.Entry(root, width=10)
	xEntry.bind('<Return>',saveWidthVal)
	xEntry.place(x=50,y=275)
	xLabel=tk.Label(root, text='width:\t'+str(round(X,2)))
	xLabel.place(x=100,y=275)

	# image height variable input
	def saveHeightVal(event=None):
		global Y
		try:
			Y = int(yEntry.get())	
			yLabel.config(text='height:\t'+str(round(Y,2)))
		except:
			print('Invalid height value')
	yEntry=tk.Entry(root, width=10)
	yEntry.bind('<Return>',saveHeightVal)
	yEntry.place(x=50,y=300)
	yLabel=tk.Label(root, text='height:\t'+str(round(Y,2)))
	yLabel.place(x=100,y=300)

	# save colormap input
	def saveColormap(event=None):
		global cmapName
		try:
			cmapName = str(cmapEntry.get())
			cmapLabel.config(text='colormap: '+cmapName)
		except:
			print('Invalid colormap')
	cmapEntry=tk.Entry(root, width=10)
	cmapEntry.bind('<Return>',saveColormap)
	cmapEntry.place(x=50,y=325)
	cmapLabel=tk.Label(root, text='colormap: '+cmapName)
	cmapLabel.place(x=100,y=325)

	print("Done\nStarting window display ")
	root.mainloop() #begin loop

	print('Session ended\nShutting down...')
	hold(3)

main()
		