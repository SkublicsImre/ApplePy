"""
Pseudo:
1.Take User Input (midpoint, radius, noFly zone, accuracy)
calculate drone path into a list of coordinates
Display calculated path

2.UI for tweaking options about path planning and display methods.

"""
# 3d library
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

# simple calculations
import math as M

# for surface plotting
import numpy as np 

# Take initial values from user
def TakeUserInput():
    print("\nAdja meg a mérni kívánt objektum középpontját, magasságát és szélességét, valamint a mérési sugarat, és a mérési pontok számát.")
    
    # x->longitude y->latitude z->distance from ground level
    x = float(input("\nMérési középpont\nx:"))      #[cord]
    y = float(input("y:"))                          #[cord]
    z = float(input("z:"))/meterDiv                 #[m]
    R = float(input("mérési sugár:"))/meterDiv      #[m]
    L = int(input("gömbszeletek száma:"))           #[db]
    P = int(input("mérési pontok száma:"))          #[db]
    h = float(input("objektum magasság:"))/meterDiv #[m]
    w = float(input("objektum szélesség:"))/meterDiv#[m]

    # The measuring field cannot collide with the ground or the object
    if z-R<0 or R<w/2 or z+R<h:
        print("HIBA: Mérési felület ütközik az objektum dimenziójival\n")
        TakeUserInput()

    return[x,y,z,R,L,P,w,h]

# Calculate a safe path according to the initial conditions for given nPoint values
def CalculatePath(x,y,z,R,nVertical,nHorisontal,shy,FieldAngle):
    if nHorisontal<4:shy=False

    stepList = [] 
    VerticalStep = FieldAngle*2*R/nVertical #meter
    HorisontalStep = 2*M.pi/nHorisontal #rads
    midx = x
    midy = y
    midz = z

    #starting from the top down we approach the object
    z += R

    #calculate measuring coordinates (+= iterator is needed so we dont start measuring from a 0 Radius)
    for nHstep  in range(nVertical):
        rot = 180
        #calculate plane radius at given height ((R-nStep)^2 + PlaneRadius^2 = R^2)
        nHstep += 1
        PlaneRadius = M.sqrt(R**2-(R - VerticalStep*nHstep)**2)
        x = midx+PlaneRadius
        if shy: stepList.append([x,y,z,rot])
        y = midy
        if shy: stepList.append([x,y,z,rot])
        z -= VerticalStep
        stepList.append([x,y,z,rot])

        #Calculate single points for the given plane
        for nDeg in  range(nHorisontal):
            deg = HorisontalStep*nDeg

            rot = deg+M.pi
            if rot>2*M.pi:rot-=2*M.pi
            rot=(rot/(2*M.pi))*360
            
            if (deg > 0 and deg <= M.pi/2) or (deg > M.pi and deg <= 3/2*M.pi):
                y = midy+PlaneRadius*M.sin(deg)
                if shy: stepList.append([x,y,z,rot])
                x = midx+PlaneRadius*M.cos(deg)
                stepList.append([x,y,z,rot])

            if (deg > M.pi/2 and deg <= M.pi) or (deg > 3/2*M.pi and deg <= 2*M.pi):
                x = midx+PlaneRadius*M.cos(deg)
                if shy: stepList.append([x,y,z,rot])
                y = midy+PlaneRadius*M.sin(deg)
                stepList.append([x,y,z,rot])

    return stepList

def PreparePath(lst):
    InstructionList = []

    for i in lst:
        # do something with these
        i[0] # x
        i[1] # y
        i[2] # z
        InstructionList.append() #prepared instruction goes here

    return InstructionList

def Display(CordList,x,y,z,R,w,h):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # draw measuring field    
    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    xs = x + R * np.outer(np.cos(u), np.sin(v))
    ys = y + R * np.outer(np.sin(u), np.sin(v))
    zs = z + R * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(xs, ys, zs, color='grey',alpha=0.4, zorder=0.7)

    # draw object
    radius = w
    z = np.linspace(0, h, 20)
    theta = np.linspace(0, 2*np.pi, 10)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + x
    y_grid = radius*np.sin(theta_grid) + y
    ax.plot_surface(x_grid, y_grid, z_grid, color='b',alpha=0.8, zorder=0.1)

    # draw path
    xLst = []
    yLst = []
    zLst = []
    for i in CordList:
        xLst.append(i[0])
        yLst.append(i[1])
        zLst.append(i[2])
        print('É: '+str(format(i[0],'.6f'))+',\tK: '+str(format(i[1],'.6f'))+',\tmagasság: '+str(format((i[2]*meterDiv),'.6f'))+',\tirány: '+str(format(i[3],'.4f')))
    ax.plot3D(xLst,yLst,zLst,'red',alpha=1,zorder=0.9)
    ax.scatter3D(xLst,yLst,zLst,color='red',alpha=1,zorder=0.9)

    # name axis
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_aspect('equal')

    #display this mess
    plt.show()

# for debugging:
# ERROR: IF LESS THAN 4 MEASURING POINTS ASSIGNED, 
# IT REQUIRES MORE THEN 2 STEPS TO AVOID COLLISION
# therefore shyplanning doesnt aply

# Demo
# [midx,midy,midz,radious,Planes,Points,width,height]
# n = [x,y,z,R,L,P,w,h]
# n = [4,5,20,12,5,10,5,25]

# check if main
if __name__=='__main__':
    print("DRONE PATH PLANNING\n(by ImreSkublics :3)")

    # starting parameters
    Shy = False
    c = 0.6
    path = []
    meterDiv = 111000.0001

    #command loop
    while True:
        command = input('commands:\n /help\n /options\n /run-demo\n /run\n /upload\n /save\n /exit\n>>')
        if command == "/options":
            option = input("options:\n[1]set direct path\n[2]set avoiding path (longer)\n[3]set coverage\n[4]cord to meter exchange\n[5]back\n>>>")
            if option == "1":
                Shy = False
            elif option == "2":
                Shy = True
            elif option == "3":
                c = float(input('how much of the globe to cover [0-100%]:\n>>>>'))/100
            elif option == "4":
                meterDiv = float(input("méter váltószám: \n>>>>"))
            elif option == "5":
                pass
            else:print("option doesnt exsist")
        elif command == "/run":
            n = TakeUserInput()
            path = CalculatePath(n[0],n[1],n[2],n[3],n[4],n[5],Shy,c)
            Display(path,n[0],n[1],n[2],n[3],n[6],n[7])
        elif command == "/run-demo":
            n = [47.23433,53.27714,20,10,5,10,5,25]
            path = CalculatePath(n[0],n[1],n[2],n[3],n[4],n[5],Shy,c)
            Display(path,n[0],n[1],n[2],n[3],n[6],n[7])
        elif command == "/help":
            print("you didnt actually expect me to write a manual for this right?")
        elif command == "/exit":
            exit()
        elif command=="/save":
            if path.__len__() > 0:
                f = open(input("név: ")+".txt",'w')
                for i in path:
                    f.write('É: '+str(format(i[0],'.2f'))+',\tK: '+str(format(i[1],'.2f'))+',\tmagasság: '+str(format(i[2],'.2f'))+',\tirány: '+str(format(i[3],'.2f'))+"\n")
                f.close()
            else:print("No path found \n(run the planning algorythm first)")
        
        # I dont actually know the instruction format for this drone (not even sure if its automatically driven)
        elif command == "/upload": 
            if path.__len__() > 0:
                # DroneInstructions = PreparePath(path)
                print("should upload instruction list to drone via serial port or something\n (not done yet)")
            else:print("No path found \n(run the planning algorythm first)")

        else:print('invalid command')
# nice