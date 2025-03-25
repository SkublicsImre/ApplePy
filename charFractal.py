import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image

#declare global variables
div = 1			 	#image scaleing
shift = [1.5,2]		#image shift from midpoint
zm= 1				#zoom
X = int(170/div)  	#image width
Y = int(80/div)  	#image height
ex=10				#limit for z absolute value before exiting the complex loop
bl=30				#number of iterations before exiting the complex loop 

def main(a1,a2,a3,a4):

	#grayscale character list Bright to dark
	gscale=["$","@","B","%","8","&","W","M","#","*","o","a","h","k","b","d","p","q","w","m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","(",")","1","{","}","[","]","?","-","_","+","~","<",">","i","!","l","I",";",":","^","`","'","."," "]
	gres=gscale.__len__()-1 #scale lenght

	#function to generate 2d 0-list
	def nullField():
		field=[]
		for i in range(Y):
			line=[]
			for j in range(X):
				line.append(0)
			field.append(line)
		return field

	#Function to normalise 2d list	
	def norm(field,target):
		nfield=nullField()
		#find minimum and maximum values
		maxpoint = 0
		minpoint  = 100000
		for line in field:
			for point in line:
				if point < minpoint: minpoint=point
				if point > maxpoint: maxpoint=point
		maxpoint-=minpoint
		if maxpoint==0:return nfield 
		#exclude homogen
		else:
			#normalise
			y=0
			for line in field:
				x=0
				for point in line:
					nfield[y][x]=1-((point-minpoint)/maxpoint)*target
					x+=1	
				y+=1
		return nfield

	#function to draw image
	def displayField(field):
		nfield=""
		for line in field:
			nline=""
			for point in line:
				nline+=" "+gscale[int(point)]
				#match to gscale
			nfield+=nline+"\n"
		print('\r\033['+str(Y+10)+'A') 
		#move cursor to print over previous image
		print(nfield)

	#function to generate points in fractal
	def F(x,y,exit,bail,zoom,n1,n2,n3,n4):
		#match points to image scale
		i=((x/X)*3-shift[0])*zoom
		j=((y/Y)*4-shift[1])*zoom
		#declare local variables
		c=complex(i,j)
		z=c
		count=0
		#iterate the mandelbrot equation
		while count<=bail:
			z=z**n4-z**n3+z**n2-z**n1+c
			count+=1
			if abs(z)>=exit: break
		return abs(z) #return value at exit or bail

	#set up slideshow	
	run=True
	Field=nullField()
	
	#iterate trough 2d list
	for y in range(Y):
		for x in range(X):
			Field[y][x]=F(x,y,ex,bl,zm,a1,a2,a3,a4)
			#find mandelbrot values
	displayField(norm(Field,gres))
	#draw the set

def SaveImage(a1,a2,a3,a4):
	w=1140
	h=660
	shape=(h,w,3)
	imgArr=np.zeros(shape)
	#function to generate points in fractal
	def F(x,y,exit,bail):
		#match points to image scale
		i=((x/w)*3-shift[0])*zm
		j=((y/h)*4-shift[1])*zm
		#declare local variables
		c=complex(i,j)
		z=c
		count=0
		#iterate the mandelbrot equation
		while count<=bail:
			z=z**a4-z**a3+z**a2-z**a1+c
			count+=1
			if abs(z)>=exit: break
		return [count,abs(z),abs(c)] #return value at exit or bail
	
	for i in range(h):
		for j in range(w):
			val=F(j,i,50,80)
			imgArr[i][j][0]=val[0]
			imgArr[i][j][1]=val[1]
			imgArr[i][j][2]=val[2]
	
	img_a = imgArr[:, :, 0]
	img_b = imgArr[:, :, 1]
	img_c = imgArr[:, :, 2]

	max_a=np.max(img_a);max_b=np.max(img_b);max_c=np.max(img_c)
	min_a=np.min(img_a);min_b=np.min(img_b);min_c=np.min(img_c)
	
	img_a = 1-(img_a - np.min(img_a)) / (np.max(img_a) - np.min(img_a))
	img_b = 1-(img_b - np.min(img_b)) / (np.max(img_b) - np.min(img_b))
	img_c = 1-(img_c - np.min(img_c)) / (np.max(img_c) - np.min(img_c))

	# putting the 3 channels back together:
	img_norm = np.zeros(shape,dtype=int)
	img_norm[:, :, 0] = img_a*255
	img_norm[:, :, 1] = img_b*255
	img_norm[:, :, 2] = img_c*255

	img_norm = (np.rint(img_norm)).astype(np.uint8)

	PILimg=Image.fromarray(img_norm)
	PILimg.save('frc_shift.jpg')

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Fractal morfing')
root.columnconfigure(4, weight=1)
root.columnconfigure(1, weight=3)

# slider current value
current_value1 = tk.DoubleVar()
current_value2 = tk.DoubleVar()
current_value3 = tk.DoubleVar()
current_value4 = tk.DoubleVar()

def get_current_value1():
    return '{: .2f}'.format(current_value1.get())
def get_current_value2():
    return '{: .2f}'.format(current_value2.get())
def get_current_value3():
    return '{: .2f}'.format(current_value3.get())
def get_current_value4():
    return '{: .2f}'.format(current_value4.get())


def slider1_changed(event):
	value_label1.configure(text=get_current_value1())
	main(current_value1.get(),current_value2.get(),current_value3.get(),current_value4.get())
def slider2_changed(event):
	value_label2.configure(text=get_current_value2())
	main(current_value1.get(),current_value2.get(),current_value3.get(),current_value4.get())
def slider3_changed(event):
	value_label3.configure(text=get_current_value3())
	main(current_value1.get(),current_value2.get(),current_value3.get(),current_value4.get())
def slider4_changed(event):
	value_label4.configure(text=get_current_value4())
	main(current_value1.get(),current_value2.get(),current_value3.get(),current_value4.get())

#  slider
slider1 = ttk.Scale(root,from_=0,to=4,orient='horizontal',command=slider1_changed,variable=current_value1)
slider1.grid(column=1,row=0,sticky='we')
slider2 = ttk.Scale(root,from_=0,to=4,orient='horizontal',command=slider2_changed,variable=current_value2)
slider2.grid(column=1,row=1,sticky='we')
slider3 = ttk.Scale(root,from_=0,to=4,orient='horizontal',command=slider3_changed,variable=current_value3)
slider3.grid(column=1,row=2,sticky='we')
slider4 = ttk.Scale(root,from_=0,to=4,orient='horizontal',command=slider4_changed,variable=current_value4)
slider4.grid(column=1,row=3,sticky='we')

# value label
value_label1 = ttk.Label(root,text=get_current_value1())
value_label1.grid(row=4,columnspan=2,sticky='n')
value_label2 = ttk.Label(root,text=get_current_value2())
value_label2.grid(row=5,columnspan=2,sticky='n')
value_label3 = ttk.Label(root,text=get_current_value3())
value_label3.grid(row=6,columnspan=2,sticky='n')
value_label4 = ttk.Label(root,text=get_current_value4())
value_label4.grid(row=7,columnspan=2,sticky='n')


root.mainloop()
SaveImage(current_value1.get(),current_value2.get(),current_value3.get(),current_value4.get())
