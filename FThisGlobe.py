import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import pandas as pd

# Create fake data
def spoofData(Npoints,freqRange,dominantFreq,noise,lenght):
    data=np.zeros((lenght,Npoints))
    freqs=[]
    for row in range(lenght):
        freq=(row/lenght)*(freqRange[1]-freqRange[0])+freqRange[0]
        freqs.append(freq)
        for point in range(Npoints):
            if freq<=dominantFreq:data[row,point]=-60-np.random.randint(10,10+noise)-100*(1-(freq/dominantFreq))
            else:data[row,point]=-60-np.random.randint(10,10+noise)-100*(1-(dominantFreq/freq))
    return [np.array(freqs),data]

# Generate all heatmap values
def pregenMaps():
    maps=[]
    for frameData in frame_values:
        maps.append(map_color_spacing(frameData))
    return np.array(maps)

# Create a list of target coordinates based on the number of layers and points
def equally_spaced_points_on_globe(radius, l, N):
    points = []
    for i in range(l):
        for j in range(N):
            if l == 1:
                phi = 1.5  # Special case: one layer, latitude is 0
            else:
                phi = np.pi * (i / (l - 1) - 0.65)  # Equally spaced latitudes from -pi/2 to pi/2
            theta = 2*np.pi * j / N  # Equally spaced angles around the horisontal slice
            ex = radius * np.sin(phi) * np.cos(theta) # Transfer to x,y,z coordinates
            ey = radius * np.sin(phi) * np.sin(theta)
            ez = radius * np.cos(phi)
            points.append([ex, ey, ez]) # Return a list of target coordinates
    return np.array(points)

# Check target coordinates against single point
def near(p, pntList, vals):
    cnt=0 # intensity counter
    itercnt=0 # value index counter
    for pj in pntList:
        dist=np.linalg.norm( p - pj ) # Calculate distance between targetpoint and current point
        d0=vals[itercnt] # Assign intensity limit to target point
        if dist < d0: # If the current point is within bounds, raise intensity
            cnt += 1 - dist/d0
        itercnt+=1 # Move to the next value (the number of points and values in a single frame are allways the same)
    return cnt

# Mao Color values for the heatmap
def map_color_spacing(values):
    Dvalues = np.zeros(x.shape) # Empty 2D map
    for i in range(len(Dvalues)):
        for j in range(len(Dvalues[0])): # Iter trough all points
            X=x[i,j]
            Y=y[i,j]
            Z=z[i,j]
            Dvalues[i,j] = near(np.array( [X, Y, Z ] ), mypointlist, values) # Check against target points
    return Dvalues 

# Update the plot for each frame of the animation
def update(frame):
    ax.cla()  # Clear the previous frame
    # Set visuals
    ax.set_title(f'Frequency {int(freqs[frame])}')
    #ax.text(1.05, 1.05, 1.05, f'Value: {current_frame_values[0, 0]:.2f}', fontsize=10, color='black')
    ax.set_xlim(-Radius, Radius)
    ax.set_ylim(-Radius, Radius)
    ax.set_zlim(-Radius, Radius)
    # Display Frame
    ax.plot_surface(x, y, z, facecolors=plt.cm.jet(mapValues[frame]), rstride=1, cstride=1, alpha=1)
    
# Load data from a CSV file with a semicolon separator
csv_filename = 'proba_csv_heatmap.csv'
data = pd.read_csv(csv_filename, sep=';')

# Global Presets
n = 6  # Number of points on each slice of the sphere
L = 2  # Number of slices taken from the sphere
intensity = 300 # size of color diffusion (choose carefully, overlapping may cause artifacts)
Radius = 10 # Size of displayed sphere (for spherical coordinate conversion) 
spoofed = True #if data is manufactured

# Create a global grid
phi, theta = np.linspace(0, 2 * np.pi, 120), np.linspace(0, np.pi, 60) # Set resolution here
phi, theta = np.meshgrid(theta, phi)
x = Radius*np.sin(phi) * np.cos(theta)
y = Radius*np.sin(phi) * np.sin(theta)
z = Radius*np.cos(phi)

# Extract and reshape frequency range and db measurements into frame-by-frame data
frame_values = []
freqs=[]
for index, row in data.iterrows():  # Iterate trough extracted rows
    values = row[1:].values.astype(float) # Separate db values
    freqs.append(row.iloc[0]) # Separate frequencies
    frame_values.append(values)
if spoofed:
    [freqs,frame_values]=spoofData(12,(1200,1350),1275,3,50)

frame_values = np.array(frame_values) # Normalise db values to a positive constant coefficient
frame_values = (frame_values/np.linalg.norm(frame_values))*intensity*Radius
frame_values = abs(np.min(frame_values))+frame_values

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z))) #set aspect ratio

# Set the number of frames for the animation
num_frames = frame_values.shape[0]

# Create target points
mypointlist=equally_spaced_points_on_globe(Radius,L,n)

#pre gemmerate colormaps for smoother animation
mapValues=pregenMaps()

# Animate
animation = FuncAnimation(fig, update, frames=num_frames, interval=1)

# Display the animation
plt.show()