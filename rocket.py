#nice
import time
import sys
import math
import msvcrt

delay = 0.05 #[accuracy]
terminate = 0

r = 6371*10**3 #[m]
M = 5.9736*(10**24) #[kg]
gamma = 6.674*(10**-11) #[Nm^2/kg^2]

def reset():
    global Ft, Fcp, Fg, Flx, Fly, Vx, Vy, t, a, h, d, m, m2, stage, gap,once
    global alpha, Ro, full_thrust, fuel_consumption, fuel_m, vehicle_m, full_thrust2, fuel_consumption2, fuel_m2, vehicle_m2, throttle_up_time, throttle_up_time2,  throttle_down_time, throttle_down_time2, burning_time, burning_time2, runtime, speed, runtime2
    global A, Cw, count, st_fuel_m, st_fuel_m2, hmax,hprev,Vxprev,Vxmax,Vyprev,Vymax, pich_start,pich_half1,pich_half2,pich_speed1,pich_speed2
    once=0
    hmax=0
    hprev=0
    Vxprev=0
    Vxmax=0
    Vyprev=0
    Vymax=0
    stage = 1
    gap = 0
    Ft = 0
    Fcp = 0
    Flx = 0
    Fly = 0
    Vy = 0
    Vx = 0
    t = -10
    a = 0.00
    h = 0
    alpha = math.pi/2 
    Ro = 1.2045 

    full_thrust = 4420000 #[N]
    fuel_consumption = 2000 #[kg/s]
    fuel_m = 420000 #[kg]
    vehicle_m = 22000 #[kg]

    full_thrust2 = 27000 #[N]
    fuel_consumption2 = 5#[kg/s]
    fuel_m2 = 2000 #[kg]
    vehicle_m2 = 2000 #kg

    A = 10.5 #[m^2]
    Cw = 0.0237 #[drag coefficient]
    speed = 1 #real time speed multiplier
    count = t
    st_fuel_m = fuel_m
    st_fuel_m2 = fuel_m2
    m = fuel_m + vehicle_m
    m2 = fuel_m2 + vehicle_m2
    d = h + r
    Fg = -gamma*((m*M)/(d**2))

    throttle_up_time = 5/delay
    throttle_down_time = 10/delay
    burning_time = (fuel_m/fuel_consumption)/delay
    runtime = (throttle_up_time+throttle_down_time+burning_time)

    throttle_up_time2 = 2/delay
    throttle_down_time2 = 2/delay
    burning_time2 = (fuel_m2/fuel_consumption2)/delay
    runtime2 = (throttle_up_time2+throttle_down_time2+burning_time2)

    pich_start = 0
    pich_half1 = 0.3333333333333
    pich_half2 = 0.67777777777777
    pich_speed1 = 1.2
    pich_speed2 = 2

def setup():
    global Ft, Fcp, Fg, Flx, Fly, Vx, Vy, t, a, h, d, m, m2, stage, gap,once
    global alpha, Ro, full_thrust, fuel_consumption, fuel_m, fuel_m2, st_fuel_m2, vehicle_m2, vehicle_m, throttle_up_time,  throttle_down_time, burning_time, runtime
    global A, Cw, count, st_fuel_m, hmax,hprev,Vxprev,Vxmax,Vyprev,Vymax
    Ft = 0
    stage = 1
    gap = 0
    once=0
    Fcp = 0
    Flx = 0
    Fly = 0
    Vy = 0
    Vx = 0
    t = -10
    a = 0.00
    h = 0
    alpha = math.pi/2
    Ro = 1.2045
    count = -10
    fuel_m = st_fuel_m
    fuel_m2 = st_fuel_m2
    m = fuel_m + vehicle_m
    m2 = fuel_m2 + vehicle_m2
    d = h + r
    Fg = -gamma*((m*M)/(d**2))
    hmax=0
    hprev=0
    Vxprev=0
    Vxmax=0
    Vyprev=0
    Vymax=0

def options():
    global full_thrust, fuel_consumption, fuel_m, vehicle_m, throttle_up_time,  throttle_down_time, A, Cw, speed, st_fuel_m
    print("\nOPTIONS:\n[1]full_thrust = "+str(full_thrust)+"\n[2]fuel_consumption = "+str(fuel_consumption)+"\n[3]fuel mass = "+str(fuel_m)+"\n[4]vehicle mass = "+str(vehicle_m)+"\n[5]throttle up time = "+str(throttle_up_time*delay)+"\n[6]throttle down time = "+str(throttle_down_time*delay)+"\n[7]surface area = "+str(A)+"\n[8]drag coefficient = "+str(Cw)+"\n[9]real time speed multiplier = "+str(speed)+"\n[10]reset\n[11]show changes\n[12]pich options\n[13]second stage options\n[14]back")
    while terminate==0:
        x = (input("\nchoose option: "))
        if x=="1":full_thrust = float( input("\nfull thrust = "))
        elif x=="2":fuel_consumption = float( input("fuel consumption = "))
        elif x=="3":fuel_m = float( input("fuel mass = "));st_fuel_m = fuel_m
        elif x=="4":vehicle_m = float( input("vehicle mass = "))
        elif x=="5":throttle_up_time = float( input("throttle up time = "))/delay
        elif x=="6":throttle_down_time = float( input("throttle down time = "))/delay
        elif x=="7":A = float( input("surface area = "))
        elif x=="8":Cw = float( input("drag coefficient = "))
        elif x=="9":speed = float( input("real time speed multiplier = "))
        elif x=="10":reset()
        elif x=="11":print("\n[1]full_thrust = "+str(full_thrust)+"\n[2]fuel_consumption = "+str(fuel_consumption)+"\n[3]fuel mass = "+str(fuel_m)+"\n[4]vehicle mass = "+str(vehicle_m)+"\n[5]throttle up time = "+str(throttle_up_time*delay)+"\n[6]throttle down time = "+str(throttle_down_time*delay)+"\n[7]surface area = "+str(A)+"\n[8]drag coefficient = "+str(Cw)+"\n[9]real time speed multiplier = "+str(speed))
        elif x=="14":break
        elif x=="12":pitch_options()
        elif x=="13":sec_stage_options()
        else: print("\ninvalid command")
    ask()

def sec_stage_options():
    global full_thrust2, fuel_consumption2, fuel_m2, vehicle_m2, throttle_up_time2,  throttle_down_time2, st_fuel_m2
    print("\nSECOND STAGE:\n[1]full thrust = "+str(full_thrust2)+"\n[2]fuel consumption = "+str(fuel_consumption2)+"\n[3]fuel mass = "+str(fuel_m2)+"\n[4]second stage mass = "+str(vehicle_m2)+" 'cannnot be bigger than vehicle mass'\n[5]throttle up time = "+str(throttle_up_time2*delay)+"\n[6]throttle down time = "+str(throttle_down_time2*delay)+"\n[7]show changes\n[8]back")
    while terminate==0:
        x=input("choose option: ")
        if x=="1":full_thrust2 = int(input("full thrust = "))
        elif x=="2":fuel_consumption2 = int(input("fuel consumption = "))
        elif x=="3":fuel_m2 = int(input("fuel mass = ")); st_fuel_m2 = fuel_m2
        elif x=="4":vehicle_m2 = int(input("second stage mass = "))
        elif x=="5":throttle_up_time2 = int(input("thorttle up time"))
        elif x=="6":throttle_down_time2= int(input("thorttle down time"))
        elif x=="7":print("[1]full thrust = "+str(full_thrust2)+"\n[2]fuel consumption = "+str(fuel_consumption2)+"\n[3]fuel mass = "+str(fuel_m2)+"\n[4]second stage mass = "+str(vehicle_m2)+" 'cannnot be bigger than vehicle mass'\n[5]throttle up time = "+str(throttle_up_time2)+"\n[6]throttle down time = "+str(throttle_down_time2)+"\n[7]show changes\n[8]back")
        elif x=="8":print("\nOPTIONS:");break
        else: print("\ninvalid command")

def pitch_options():
    global pich_start,pich_half1,pich_half2,pich_speed1,pich_speed2
    print("\nPITCH PROGRAM:")
    print("\n[1]pich start = "+str(pich_start)+"\n[2]pich half1 = "+str(pich_half1)+"\n[3]pich half2 = "+str(pich_half2)+"\n[4]pich speed1 = "+str(pich_speed1)+"\n[5]pich speed2 = "+str(pich_speed2)+"\n[6]show changes\n[7]back")
    while terminate==0:
        x = input("choose option: ")
        if x=="1":pich_start = float(input("pich start = "))
        elif x=="2":pich_half1 = float(input("pich half1 = "))
        elif x=="3":pich_half2 = float(input("pich half2 = "))
        elif x=="4":pich_speed1 = float(input("pich speed1 = "))
        elif x=="5":pich_speed2 = float(input("pich speed2 = "))
        elif x=="6":print("\n[1]pich start = "+str(pich_start)+"\n[2]pich half1 = "+str(pich_half1)+"\n[3]pich half2 = "+str(pich_half2)+"\n[4]pich speed1 = "+str(pich_speed1)+"\n[5]pich speed2 = "+str(pich_speed2))
        elif x=="7":print("\nOPTIONS:");break




def sea_engine():
    global Ft, m, fuel_m
    if count<=throttle_up_time:
        Ft += full_thrust/throttle_up_time      #throttle up
        fuel_m -= st_fuel_m/runtime
    if count>throttle_up_time and count<=burning_time+throttle_up_time:
        fuel_m -= st_fuel_m/runtime                #burn //no changes//
    if count>burning_time+throttle_up_time and count<=runtime:
        Ft -= full_thrust/throttle_down_time    #throttle down
        fuel_m -= st_fuel_m/runtime
    m = fuel_m+vehicle_m

def vac_engine():
    global  Ft, m, fuel_m2
    if count-runtime-gap<=throttle_up_time2:
        Ft += full_thrust2/throttle_up_time2      #throttle up
        fuel_m2 -= st_fuel_m2/runtime2
    if count-runtime-gap>throttle_up_time2 and count-runtime-gap<=burning_time2+throttle_up_time2:
        fuel_m2 -= st_fuel_m2/runtime2                #burn //no changes//
    if count-runtime-gap>burning_time2+throttle_up_time2 and count-runtime-gap<=runtime2:
        Ft -= full_thrust2/throttle_down_time2    #throttle down
        fuel_m2 -= st_fuel_m2/runtime2
    m = fuel_m2+vehicle_m2

def stage_sep():
    global m
    m = m2
    print("\n\n/Stage separation/\n")
    return 2

def pich_program():
    global alpha
    if count>runtime*pich_start and count<=runtime*pich_half1:#1/3
        alpha -= (math.pi/2)/(runtime/pich_speed1)#3
        if alpha<(math.pi/4):alpha=(math.pi/4)
    elif count>runtime*(pich_half2):#2/3
        alpha -= (math.pi/2)/(runtime/pich_speed2)#1.1
        if alpha<0:alpha=0




def calculate(status):
    global Ft, Vy, Vx, t, a, h, d, Fg, Fcp, Ro, Flx, Fly, hmax, hprev, Vxprev, Vxmax, Vyprev, Vymax, stage
    if stage==0:Ft=0
    t = float(count*delay)
    Fy = Ft*math.sin(alpha)+Fg+Fcp-Flx
    Fx = Ft*math.cos(alpha)-Fly
    Fe = (Fx,Fy)
    a = [Fe[0]/m,Fe[1]/m]
    DVy = a[1]*delay
    DVx = a[0]*delay
    Dh = (a[1]/2)*(delay**2)+(Vy*delay)
    Vyprev=Vy
    Vy += DVy
    Vxprev=Vx
    Vx += DVx
    hprev=h
    h += Dh
    d = h + r
    Ro -=  1.2045/100000
    if h > 100000: Ro = 0
    Fcp = (m*(Vx**2))/d
    Flx = (1/2*Ro*A*Cw*Vx)
    Fly = (1/2*Ro*A*Cw*Vy)
    Fg = -gamma*((m*M)/(d**2))
    if Vy < 0 and count<throttle_up_time: Vy = 0; h = 0
    if hmax<h:hmax=h
    if Vxmax<Vx:Vxmax=Vx
    if Vymax<Vy:Vymax=Vy
    if Fe[1]/m<0.05 and Fe[1]/m>-0.05 and status==2:stage=0;Ft=0

def countdown():
    global count, t, Vy
    while(count<=0):
        calculate(1)
        t = count
        Vy = 0
        sys.stdout.write("<--type for exit |fuel = %d[kg]| |acceleration = x:%d y:%d[m/s^2]| |speed = x:%d y:%d[m/s]| |altitude = %d[m]| |thrust = %d[N]| |T %d[s]|   \r" % (fuel_m,a[0],a[1],Vx,Vy,h,Ft,t))
        sys.stdout.flush()
        count += 1
        time.sleep(1/speed)
        if msvcrt.kbhit(): print("\n\n/currently flying/\n"); break
    print("\n\n/ignition/\n")

def ask():
    global terminate
    x=(input("\nMENU\n1[Run Sim] 2[Options] 3[Exit] "))
    if x =="1":Run_Sim()
    elif x=="2":options()
    elif x=="3":terminate=1
    else:print("invalid command"); ask()
    

def feedback(status):
    global once
    if count==throttle_up_time: print("\n\n/engine at full power/\n")
    if count==throttle_up_time2+runtime+gap and status==2: print("\n\n/vacuum engine at full power/\n")
    if Vy==a[1]*delay and count<throttle_up_time: print("\n\n/liftoff/\n")
    if count==throttle_up_time+burning_time: print("\n\n/throttle down/\n")
    if count==throttle_up_time2+burning_time2+runtime+gap and status==2: print("\n\n/vacuum engine throttle down/\n")
    if count==runtime: print("\n\n/engine shutoff/\n")
    if count==runtime+runtime2+gap and status==2: print("\n\n/vacuum engine shutoff/\n")
    if stage==0 and once==0:once=1;print("\n\n/vacuum engine shutoff/\n\n/achieved stable orbit/\n")

    if status==1:
        sys.stdout.write("<--type for exit |fuel = %d[kg]| |acceleration = x:%d y:%d[m/s^2]| |speed = x:%d y:%d[m/s]| |altitude = %d[m]| |thrust = %d[N]| |T + %d[s]|   \r" % (fuel_m,a[0],a[1],Vx,Vy,h,Ft,t))
        sys.stdout.flush()

    if status==2 or status==0:
        sys.stdout.write("<--type for exit |fuel = %d[kg]| |acceleration = x:%d y:%d[m/s^2]| |speed = x:%d y:%d[m/s]| |altitude = %d[m]| |thrust = %d[N]| |T + %d[s]|   \r" % (fuel_m2,a[0],a[1],Vx,Vy,h,Ft,t))
        sys.stdout.flush()

def analytics():
    print("flight time: "+str(t/60)+"[min]")
    print("highest altitude: "+str(hmax/1000)+"[km]")
    if h>100000:print("passed the karman line")
    print("highest vertical speed: "+str(Vymax/3.6)+"[km/h]")
    print("highest horizontal speed: "+str(Vxmax/3.6)+"[km/h]")
    print("leftover first stage fuel: "+str(int(fuel_m))+"[kg]")
    print("leftover second stage fuel: "+str(int(fuel_m2))+"[kg]")




def ROCKET(status):
    global count
    if status == 1:sea_engine()
    if status == 2:vac_engine()
    pich_program()
    calculate(status)
    time.sleep(delay/speed)
    count += 1

def Run_Sim():
    global stage, gap
    print("\n")
    setup()
    countdown()
    while(terminate==0):
        ROCKET(stage)
        feedback(stage)
        if terminate==1:break
        if h<0: print("\n\n/crashed/\n"); break
        if msvcrt.kbhit(): print("\n\n/currently flying/\n"); break
        if Vx>math.sqrt((2*M*gamma)/d): print("\n\n/escaped earth's gravitational field/\n"); break
        if h>100000 and Ft<1 and stage==1 and count<=runtime+gap+1: stage=stage_sep()
        if stage==1 and count>runtime:gap += 1
    print("\n______________________________________________________________________________________________________________________________________________\n")
    analytics()
    setup()
    print("\n")
    time.sleep(1)

reset()
while terminate==0:
    ask()
print("closing program...")
time.sleep(1)