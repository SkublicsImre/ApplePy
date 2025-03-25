#import:
import time
import math

#változók:
print ("\nAdja meg 10 q pont töltés nagyságát és helyzetét vesszővel elválasztva a következő módon:\n\nelső szám: a töltés nagysága 'vessző' második szám: x koordináta 'vessző' harmadik szám: y koordináta\n\n(a rendszer O pontját az origóban vesszük fel)\n")
q1 = input("q1: ").split(",")#[0.0000000001,1000,-800]
q2 = input("q2: ").split(",")#[-0.0000000002,-3000,-800]
q3 = input("q3: ").split(",")#[0.0000000002,3250,1250]
q4 = input("q4: ").split(",")#[0.0000000001,-600,2500]
q5 = input("q5: ").split(",")#[-0.0000000003,-2500,-2500]
q6 = input("q6: ").split(",")#[-0.0000000001,3000,0]
q7 = input("q7: ").split(",")#[0.0000000002,0,-3150]
q8 = input("q8: ").split(",")#[-0.0000000001,0,2800]
q9 = input("q9: ").split(",")#[0.0000000002,2300,1200]
q10 = input("q10: ").split(",")#[0.0000000001,2000,-2900]
p = input("Adja meg a vizsgálni kivánt pont x és y koordinátáit: ").split(",")#[-4000,4000]
eta_r = float(input("Adja meg a közeg dielektromos állandójának értékét:"))#(0.0006)
p[0] = float(p[0])
p[1] = float(p[1])

#funkciók:
    #listák számmá konvertálása:
def numerate_q(q):
    count = 0
    while (count<=2): 
        q[count] = float(q[count])
        count += 1
    #vektor nagysága
def lenght(r):
    return math.sqrt(float(r[0])**2+float(r[1])**2)
    #p-q táv
def rqp(q):
    a = float(p[0])-float(q[1])
    b = float(p[1])-float(q[2])
    return [a, b]
    #Az egyes pontokhoz tartozó térerősség
def Evektor(r, q):
    return [(k*float(q[0])*r[0])/lenght(r), (k*float(q[0])*r[1])/lenght(r)]
    #A térerősségek összege
def sum_E(E):
    Térerősség[0] += float(E[0])
    Térerősség[1] += float(E[1])

#numerate:
numerate_q(q1)
numerate_q(q2)
numerate_q(q3)
numerate_q(q4)
numerate_q(q5)
numerate_q(q6)
numerate_q(q7)
numerate_q(q8)
numerate_q(q9)
numerate_q(q10)

#számolások:
eta0 = float(8.854*(10**(-12)))
eta = float(eta0*eta_r)
pi = 3.141592658
k = 1 / (4*pi*eta)
    #p-q távolság (Mivel az O pont 0,0 ezért minden pont koordinátája egyben helyvektorának a koordinátája is.)
r1 = rqp(q1) 
r2 = rqp(q2)
r3 = rqp(q3)
r4 = rqp(q4)
r5 = rqp(q5)
r6 = rqp(q6)
r7 = rqp(q7)
r8 = rqp(q8)
r9 = rqp(q9)
r10 = rqp(q10)
    #Az egyes pontokhoz tartozó térerősség
E1 = Evektor(r1, q1)
E2 = Evektor(r2, q2)
E3 = Evektor(r3, q3)
E4 = Evektor(r4, q4)
E5 = Evektor(r5, q5)
E6 = Evektor(r6, q6)
E7 = Evektor(r7, q7)
E8 = Evektor(r8, q8)
E9 = Evektor(r9, q9)
E10 = Evektor(r10, q10)
    #A teljes térerősség előre kijelölt "helye"
Térerősség = [0, 0]
    #összegzés
sum_E(E1)
sum_E(E2)
sum_E(E3)
sum_E(E4)
sum_E(E5)
sum_E(E6)
sum_E(E7)
sum_E(E8)
sum_E(E9)
sum_E(E10)

#végeredmény:
print ("\na térerősség: " + str(Térerősség) + "N/C\n")

#Végeredmény kirajzolása:
    #rajz import:
import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes()
    #rajz def
def E_draw(a, b, count):
    ax.arrow(int(p[0]), int(p[1]), int(a[0]), int(a[1]), head_width=60, head_length=100, fc='black', ec='black')
    if int(b[0]) < 0:
        ax.annotate('-q' + str(count), (int(b[1]),int(b[2])),fontsize=10)
    else:
        ax.annotate('+q' + str(count), (int(b[1]),int(b[2])),fontsize=10)
    #time.sleep(0.5)
    #rajz értékek
E_draw(E1, q1, 1)
E_draw(E2, q2, 2)
E_draw(E3, q3, 3)
E_draw(E4, q4, 4)
E_draw(E5, q5, 5)
E_draw(E6, q6, 6)
E_draw(E7, q7, 7)
E_draw(E8, q8, 8)
E_draw(E9, q9, 9)
E_draw(E10, q10, 10)
ax.annotate('P', (p[0],p[1]),fontsize=10)
ax.arrow(int(p[0]), int(p[1]), int(Térerősség[0]), int(Térerősség[1]), head_width=60, head_length=100, fc='red', ec='red')
plt.grid()

plt.xlim(-5000,5000)
plt.ylim(-5000,5000)

plt.title('Erőtér:',fontsize=20)
plt.show()

time.sleep(60)

plt.close()

#PL:
    #q1: 0.000000001 20 30
    #q2: 0.000000002 60 70
    #q3: 0.000000001 -20 40
    #q4: -0.000000001 20 -40
    #q5: -0.000000002 -60 -40
    #q6: 0.000000003 10 20
    #q7: -0.000000002 -40 -10
    #q8: -0.000000001 -50 30
    #q9: -0.000000002 30 -90
    #q10: 0.000000002 -90 30
    #adja meg a vizsgálni kivánt pont x és y koordinátáit: 0 11
    #adja meg a közeg dielektromos állandójának értékét:0.0006

    #a térerősség: [-29132002.859871984, -3295103.5998395905]