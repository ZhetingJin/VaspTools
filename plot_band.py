# The bash script extracts data of band structure from OUTCAR file, and write the output file band.dat The python script use the band.dat to plot band structure with the output file band.jpg

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['agg.path.chunksize']=10000

arg_num=len(sys.argv)

if arg_num!=5:
    print("wrong inputs!!!\n")
    print("format:")
    print("plot_band filename band_num E_fermi")
    exit()

filename=sys.argv[1]
band_num=int(sys.argv[2])
E_fermi=float(sys.argv[3])
split=int(sys.argv[4])

data=np.loadtxt(filename)

#plt.figure(figsize=(10,10))


for i in range(1,band_num+1):
    #plt.plot(data[:,0],data[:,i],'.b')
    plt.plot(data[:,0],data[:,i]-E_fermi,'-g',linewidth=3,alpha=0.4)

min=10
max=-10
for (x,y),val in np.ndenumerate(data):
    val=val-E_fermi
    if val>0 and val<min:
        min=val
        minx=x
        miny=y
    elif val<0 and val>max:
        max=val
        maxx=x
        maxy=y
plt.plot(minx,min,'or')
plt.plot(maxx,max,'or')
ax=plt.gca()
ax.annotate(" "+str(minx)+"  "+str(min),xy=(minx+x/30,min),color='r',bbox=dict(boxstyle='round,pad=0.2', fc='w', alpha=0.7))
ax.annotate(" "+str(maxx)+"  "+str(max),xy=(maxx+x/30,max),color='r',bbox=dict(boxstyle='round,pad=0.2', fc='w', alpha=0.7))
if minx==maxx:
      text="Direct band gap with gap of "+str(min-max)+" eV"
else:
      text="Indirect band gap with gap of "+str(min-max)+" eV"
plt.title(text)
plt.ylabel('Energy/eV')
plt.ylim(-4,4)
plt.xlim(data[0,0],data[-1,0])
plt.axhline(0.0,label='E-fermi',color='r',alpha=0.2)
for i in range(1,split):
      plt.axvline(i*data[-1,0]/split,color='k',alpha=0.2)
#plt.savefig("band.jpg",dpi=300)
plt.show()
