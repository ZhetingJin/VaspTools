# This python script calculate ZPE/TS/H using frequency info in OUTCAR

from monty.re import regrep

def get_frequency(outcar):
    pattern = {"frequency": "^\s+[\d]+\s+f+\s+=\s+([\d\-\.]+)\sTHz+\s+([\d\-\.]+)\s2PiTHz+\s+([\d\-\.]+)\s+cm-1+\s+([\d\-\.]+)+\smeV"}
    d = regrep(outcar, pattern)
    # float string and rename index
    data = []
    for index, d in enumerate(d['frequency']):
        d[0] = [float(i) for i in d[0]]
        d[1] = '{} f'.format(index + 1)
        data.append(d)
    return data



dd = get_frequency('OUTCAR')
meV_data = [d[-1] for d, index in dd]
l=len(meV_data)
Kb = 8.6173324E-2  #Boltzmann constant unit is meV/K
T  = 298       #Absolute temperature unit is K
R  = 8.3144598     #Gas constant unit is J/(k.mol)
Tran = 1.0364E-5   #J/mol unit to eV


D = []
S = []
C = []
import numpy as np
for i in xrange(0,l):
    d =meV_data[i]/(Kb*T)
    D.append(d)
    s = (d/(np.exp(d)-1))-np.log1p(-np.exp(-d))
    S.append(s)
    c = meV_data[i]/(Kb*(np.exp(d)-1))
    C.append(c)
entropy= sum(S)
TS= R*T*entropy*Tran
ZPE= 0.5*sum(meV_data)*1E-3
U = R*Tran*sum(C)
print "ZPE =", ZPE, "eV"
print "TS =", TS, "eV"
print  "U =", U, "eV"
