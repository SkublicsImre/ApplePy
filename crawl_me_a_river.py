from matplotlib import pyplot as plt
import math as M
import numpy as np

x=[]
y=[]

for i in range(50):
    n=i+1
    try:
        d=n*M.ceil(M.log2(n))
    except:
        d=20
    if d<0:d=0
    x.append(n)
    y.append(d)

plt.scatter(x,y,marker='.',s=90,zorder=2)
plt.xlabel('Kezelendő jelek száma')
plt.ylabel('Kontrol pinek száma')
plt.title('Kontrol pinek száma ha Ni = No')
#plt.xticks(np.arange(min(x), max(x)+1, 1))
#plt.yticks(np.arange(np.floor(min(y)), np.ceil(max(y))+1, 1))
plt.legend()
plt.grid(True)
plt.show()