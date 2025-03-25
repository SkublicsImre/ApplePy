import matplotlib.pyplot as plt
import time as tt 

plt.ion()
axes = plt.gca()
boundry = [100,110]
t = 0.0002

class particle():
    def __init__(self, Position, Force, Speed, Mass, marker, markersize, markeredgecolor, markerfacecolor):
        self.N = Mass               #not tick dependent
        self.ma = marker
        self.mas = markersize
        self.maec = markeredgecolor
        self.mafc = markerfacecolor

        self.P = Position           #tick dependent
        self.F = Force
        self.V = Speed
        self.A = [Force[0]/Mass,Force[1]/Mass]

    def tick(self):
        if self.P[0] >= boundry[0]: self.P[0] = boundry[0]; self.V[0] *= -1
        if self.P[1] >= boundry[1]: self.P[1] = boundry[1]; self.V[1] *= -1
        if self.P[0] <= 0: self.P[0] = 0; self.V[0] *= -1
        if self.P[1] <= 0: self.P[1] = 0; self.V[1] *= -1

        self.P[0] += self.V[0]*t
        self.P[1] += self.V[1]*t

    def plot(self):
        axes.plot(self.P[0], self.P[1], marker=self.ma, markersize=self.mas, markeredgecolor=self.maec, markerfacecolor=self.mafc)

def assemble_frame(element_list):
    for i in element_list:
        i.plot()
    
def tick_elements(element_list):
    for i in element_list:
        i.tick()

def display_frame():
    axes.plot(0,0)
    axes.plot(boundry[0],boundry[1])
    plt.draw()
    plt.pause(0.001)
    plt.cla()
    
def run():
    plst = []
    fps = 300
    plst.append(particle([3,1],[0,0],[1,3],10,"o",10,"red","red"))
    start = tt.time()
    while True:
        if 1/fps <= tt.time()-start: assemble_frame(plst); display_frame(); start = tt.time()
        tick_elements(plst)


run()