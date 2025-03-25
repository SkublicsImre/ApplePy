from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import pandas as pd

customcords=[[0,0,10],[-10,0,0],[0,0,-10],[10,0,0]]
customintens=[1,2,3,4]

def random_point( r=1 ):
    ct = 2*np.random.rand() - 1
    st = np.sqrt( 1 - ct**2 )
    phi = 2* np.pi *  np.random.rand()
    x = r * st * np.cos( phi)
    y = r * st * np.sin( phi)
    z = r * ct
    return np.array( [x, y, z ] )

def equally_spaced_points_on_globe(radius, l, n):
    points = []
    for i in range(l):
        for j in range(n):
        
            if l == 1:
                phi = 1.5  # Special case: one layer, latitude is 1.5
                ct=(i / (l) - 0.5)
            else:
                ct=(i / (l - 1) - 0.5)
                phi = np.pi * (i / (l - 1) - 0.5)  # Equally spaced latitudes from -pi/2 to pi/2
            st = np.sqrt( 1 - ct**2 )
            theta = 2 * np.pi * j / n - 1 # Equally spaced angles around the equator
            x = radius * st * np.cos( phi)
            y = radius * st * np.sin( phi)
            z = radius * ct
            points.append([x, y, z])
    return np.array(points)

def readcsv(filename,L,n):
    data = pd.read_csv(filename, sep=';')
    frame_values = []
    freqs=[]
    for index, row in data.iterrows():
        values = row[1:].values.astype(float)  # Assuming data is numeric
        freqs.append(row[0])
        values = (values - np.min(values)) / (np.max(values) - np.min(values))  # Normalize to [0, 1]
        frame_values.append(values)
    frame_values = np.array(frame_values).reshape(-1, L, n)
    return [values]


def near( p, pntList, d0 ):
    cnt=0
    for pj in pntList:
        dist=np.linalg.norm( p - pj )
        if dist < d0:
            cnt += 1 - dist/d0
    return cnt


"""
https://stackoverflow.com/questions/22128909/plotting-the-temperature-distribution-on-a-sphere-with-python
"""

rpointList = np.array([ random_point( 10.05 ) for i in range( 4 ) ] )
mypointlist = equally_spaced_points_on_globe(1,1,2)
#print(pointList)

fig = plt.figure()
ax = fig.add_subplot( 1, 1, 1, projection='3d')

u = np.linspace( 0, 2 * np.pi, 120)
v = np.linspace( 0, np.pi, 60 )

# create the sphere surface
XX = 10 * np.outer( np.cos( u ), np.sin( v ) )
YY = 10 * np.outer( np.sin( u ), np.sin( v ) )
ZZ = 10 * np.outer( np.ones( np.size( u ) ), np.cos( v ) )

WW = XX.copy()
#print(len(XX))

count=0
for i in range( len( XX ) ):
    for j in range( len( XX[0] ) ):
        x = XX[ i, j ]
        y = YY[ i, j ]
        z = ZZ[ i, j ]
        WW[ i, j ] = near(np.array( [x, y, z ] ), mypointlist, 5)
        count+=1
if np.amax(WW)!=0: WW = WW / np.amax( WW )
#print(WW)
myheatmap = WW

# ~ ax.scatter( *zip( *pointList ), color='#dd00dd' )
ax.plot_surface( XX, YY,  ZZ, cstride=1, rstride=1, facecolors=cm.jet( myheatmap ) )
plt.show()