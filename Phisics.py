import vpython as vp

def BuildOrb(m,p,v,a,r,c):
    print('building Orb Num: '+str(myObjects.__len__()+1))
    myObjects.append(vp.sphere(ppos=vp.vector(p[0],p[1],p[2]),mass=m,name=myObjects.__len__()+1,acc=vp.vector(a[0],a[1],a[2]),vel=vp.vector(v[0],v[1],v[2]),pos=vp.vector(p[0],p[1],p[2]),radius=r,color=c))
    vavg.append(1)

def CollisionCheck(O,boxed):
    loss=.002
    mult=1-loss
    if vp.sqrt(O.vel.x**2+O.vel.y**2+O.vel.z**2)>=100:O.vel*=0.1;print("speed ERROR") #lightspeed?

    if boxed:
        #X
        if O.pos.x<-Border+O.radius:
            O.vel.x*=-mult
            O.pos.x=-Border+O.radius
            #print('Hit -X plane limit')
        elif O.pos.x>Border-O.radius:
            O.vel.x*=-mult
            O.pos.x=Border-O.radius
            #print('Hit +X plane limit')
        
        #Y
        if O.pos.y<-Border+O.radius:
            O.vel.y*=-mult
            O.pos.y=-Border+O.radius
            #print('Hit -Y plane limit')
        elif O.pos.y>Border-O.radius:
            O.vel.y*=-mult
            O.pos.y=Border-O.radius
            #print('Hit +Y plane limit')

        #Z
        if O.pos.z<-Border+O.radius:
            O.vel.z*=-mult
            O.pos.z=-Border+O.radius
            #print('Hit -Z plane limit')
        elif O.pos.z>Border-O.radius:
            O.vel.z*=-mult
            O.pos.z=Border-O.radius
            #print('Hit +Z plane limit')

    iscol=True
    while iscol:
        iscol=False
        for I in myObjects:
            if O.name!=I.name:
                d=vp.sqrt(((I.pos.x-O.pos.x)**2)+((I.pos.y-O.pos.y)**2)+((I.pos.z-O.pos.z)**2))
                if d<O.radius+I.radius:
                    iscol=False
                    mult=1-(O.mass/(O.mass+I.mass))/2
                    O.pos=I.pos-((I.pos-O.pos)/d)*(I.radius+O.radius)
                    #I.pos=I.pos+((I.pos-O.pos)/d)*(O.radius)
                    O.vel=((O.mass-I.mass)/(O.mass+I.mass))*O.vel+((2*I.mass)/(O.mass+I.mass))*I.vel*mult
                    #I.vel=(2*O.mass*O.vel-O.mass*I.vel+I.mass*I.vel)/(O.mass+I.mass)

def Tick(O):
    atrc=vp.vector(0,0,0)
    d=(atrc-O.pos)
    dabs=vp.sqrt(d.x**2+d.y**2+d.z**2)
    R=vp.sqrt(O.vel.x**2+O.vel.y**2+O.vel.z**2)/100
    if dabs==0:O.acc=vp.vector(0,0,0)
    else:O.acc=(d/dabs)*g
    O.vel+=O.acc*dt#*(1-R)
    O.ppos=O.pos
    O.pos+=O.vel*dt
    c=R*255
    O.color=vp.vector(c,0,0)

def FillVoid(dens,rad):
    l=int(dens*Border)
    for x in range(l):
        for y in range(l):
            for z in range(l):
                m=vp.random()
                d=dens/2
                D=Border
                BuildOrb(m*10,[x/d-D,y/d-D,z/d-D],[vp.random(),vp.random(),vp.random()]*2,[0,0,0],rad,vp.color.blue)

def spitIn(x,y,z):
    m=vp.random()
    BuildOrb(m*10,[x,y,z],[vp.random(),vp.random(),vp.random()]*15,[0,0,0],.08,vp.color.blue)

def main():
    global Border,dt,myObjects,g,vavg,t
    vp.canvas(title='Elastic collision sim',width=1250,height=550)
    vp.scene.background=vp.color.black
    runSim=True
    #Time
    runTime=1000
    dt=0.05
    t=0
    ct=0
    vavg=[1]

    #Sandbox
    Border=1.5
    g=0.2
    #vp.box(pos=vp.vector(0,0,0),size=vp.vector(2*Border,2*Border,2*Border),opacity=.3)
    myObjects=[]
    #FillVoid(2,.1)
    spitIn(1.5,1.5,1.5)
    count=0
    once=True
    while runSim:
        vp.rate(100)
        for i in myObjects:
            CollisionCheck(i,False)
        for i in myObjects:
            Tick(i)
        if t>=runTime:runSim=False
        else:t+=dt;ct+=dt

        if t>=10 and ct>=.5 and t<=25:
            spitIn(1.5,1.5,1.5)
            ct=0

        if t>=100 and ct>=.5 and t<=115:
            spitIn(1.5,1.5,1.5)
            ct=0
    
main()

