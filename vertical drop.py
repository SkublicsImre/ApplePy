import math
g = float(9.81)
h = 'height'
t = 'time'
V0 = 'starting velocity'
Vmax = 'impact velocity'

print ("hi")

def check_info_and_calculate():
    print ("if a piece is missing, type x")
    h = input ("drop height: ")
    t = input ("falling time: ")
    V0 = 
    Vmax = 0

    if h == 'x' and t == 'x':
        print ("We can't calculate values without any given time and height")
        h = 0
        t = 0
    if h == 'x':
        cock = 'a'
    if t == 'x':
        cock = 'b'
    if t != 'x' and h != 'x':
        cock = 'c'

    if cock == 'a':
        h = (g/2*(float(t)*float(t)))
        Vmax = (g*float(t))
    if cock == 'b':
        ins = (2*float(h)/g)
        t = (ins**2)
        Vmax = (g*float(t))
    if cock == 'c':
         Vmax = (g*float(t))

    print ("")
    print ("height = " + str(h) + "m")
    print ("time spent falling: " + str(t) + "s")
    print ("impact velocity = " + str(Vmax) + " m/s")
    print ("")

while (True):
    check_info_and_calculate()
    ask = input ("would you like to repeat? _")
    if ask == 'no':
        break
print ("bye")