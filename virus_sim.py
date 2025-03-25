import random
import time
import sys

n = int(input("\nnumber of the population:\n"))
inf = int(input("possibilty of infection:\n"))
heal = int(input("possybility of recovery:\n"))
rec = int(input("estimated time between becoming a carrier and isolation:\n"))
t = int(input("meeting rate:\n(on awrage how many people get in touch with one infected person)\n"))
print("------------------------------------------------------------------\n")

hum_list = [*range(0,n,1)] #controll
x = [2] * n #status
y = [0] * n #infection date

infected = 1
infected_prew = 0
count = 0
days = 1
cured = 0
deaths = 0

A = 0
B = 0
i = 0

def hum():
    olh = [*range(1,101,1)]
    k = int(random.choice(olh))
    return k
            
x[i] = 1
        
while infected > 0:
    
    if rec-days == 0:
        rec = rec/2

    for i in hum_list:
       
        if hum() < heal and x[i] == 1 and y[i]-days < -1*rec: #cured
            cured += 1
            infected -= 1
            x[i] = 4
        if hum() >= heal and x[i] == 1 and y[i]-days < -1*rec: #death
            infected -= 1
            deaths += 1
            x[i] = 3 
        if hum() < inf and x[i] == 2 and count < infected_prew*t: #infected
            infected += 1
            y[i] = days
            x[i] = 1
        
        count += 1

       
    
    infected_prew = infected
    count = 0
    time.sleep(0.08)
    days += 1

    sys.stdout.write("current situation = day: %d infected: %d deaths: %d cured: %d    \r" % (int(days),int(infected),float(deaths),int(cured)))
    sys.stdout.flush()
    
print ("\n\nthe sim is done\n")
if deaths != n:
    print ("the virus was defeated in " + str(days) + " days")
else:
    print ("the virus killed the entire population in " + str(days) + " days")
years = days/365
print (str(float(round(years, 2))) + " year(s)\n")
print (str(float(round((deaths/n*100), 2))) + "% " + "of the population is dead (" + str(deaths) + " people)")
print (str((deaths+cured)/n*100) + "% " + "of the population was infected overall (" + str(deaths+cured) + " people)")
print (str(((n-(deaths+cured))/n)*100) + "% " + "of the population avoided the virus (" + str(n-(deaths+cured)) + " people)\n")
