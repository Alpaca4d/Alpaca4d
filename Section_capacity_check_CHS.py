#section capacity check CHS

import Rhino.Geometry as rg
import math

"""
input:
    Diameter
    thickness
    material properties
    gammaM0

output:
    tensionUtilisation
    bendingUtilisation
"""

gamma_M0 = 1.0
gamma_M1 = 1.0

if t>=d:
    raise valueerror('thickness greater than radius')

I = math.pi*(math.pow(d,4) - math.pow(t,4))/64

alpham = [0.13, 0.21, 0.34, 0.49, 0.76]


def class_Section_CHS(d,t,fy):
    epsilon = math.sqrt(235/fy)
    
    if d/t <= 50 * math.pow(epsilon, 2):
        classSection = 1
    elif d/t <= 70 * math.pow(epsilon, 2):
        classSection = 2
    elif d/t <= 90 * math.pow(epsilon, 2):
        classSection = 3
    else:
        raise ValueError('section in class 4')
    return classSection

classSection = class_Section_CHS(d,t,fy)

classSection = class_Section_CHS(d,t,fy)
if classSection == 1 or classSection == 2:
    Wpl = (math.pow(d,3) - math.pow(d - 2*t,3)) / 6
elif classSection == 3:
    Wel = math.pi*( math.pow(d,4) - math.pow(d - 2*t,4)) / (32 * d)


if t == 0 or t == d / 2:
    Area = math.pow(d,2)/4  * math.pi
elif t < d/2 and t >= 0:
    Area = (pow(d,2)-pow((d-2*t),2))/4 * math.pi
else:
    Area = None

I = math.pi*(math.pow(d,4)- math.pow(2*t,4))/64
It= 2*I     # saint venant torsional constant



# tension check
def tensionCheck(Ned, Area, fy, gammaM0):
    NplRd = (Area * fy) / gammaM0    #require sign to be assigned to tesion force
    return NplRd


NtRd = tensionCheck(Ned, Area, fy, gamma_M0)

# shear Check

def shearCheck(Ved, Area, fy, gammaM0, T):
    shearArea = 2 * Area / math.pi
    VplRd = (shearArea * (fy/math.sqrt(3)) ) / gammaM0
    if T !=0 :
        taued = T*t/It   #shear stress due to torsion
    VplRd = (1-(taued/(fy/math.sqrt(3)/ gammaM0)))*VplRd
    shearUtilisation = Ved/ VplRd
    
    return VplRd, shearUtilisation

VplRd = shearCheck(Ved, Area, fy, gamma_M0, T)[0]


if Ved/VplRd < 0.5:
    rho = 0
else:
    rho = math.pow( ((2*Ved / VplRd) -1),2)
fy = (1-rho)*fy

# compression Check

def compressioncheck(Ned,Area,fy,Lcr,gammaM0,E):
    Ncpl =  Area*fy
    Ncr = math.pow(math.pi,2)*E*I/math.pow(Lcr,2)   #euler critical buckling
    Lamda = math.sqrt((Area*fy)/Ncr)
    for fy in range(0,420) :
        if type==0:
            alpha = alpham[1]
        else:
            alpha = alpham[3]
    for fy in range(420,) :
        if type ==1:
            alpha = alpham[0]
        else:
            alpha = alpham[3]
    phi= 0.5*(1 + alpha*(Lamda - 0.2) + math.pow(Lamda,2))
    gamma = 1/(phi+ math.sqrt(math.pow(phi,2) - math.pow(Lamda,2)))
    Nbrd= gamma*Ncpl
    Nrd= min(Ncpl, Nbrd)

    return Nrd


Nrd = compressioncheck(Ned,Area,fy,Lcr,gamma_M0,E)

print("classSection: {}".format(classSection))
print("Ved/VplRd = {}".format(Ved/VplRd))
print("reduced yield strength= {}".format(fy))

# bending check

if classSection == 1 or classSection == 2:
    Wpl = (math.pow(d,3) - math.pow(d - 2*t,3)) / 6
    MRd = (Wpl * fy) / gamma_M1
elif classSection == 3:
    Wel = math.pi*( math.pow(d,4) - math.pow(d - 2*t,4)) / (32 * d)
    MRd = (Wel * fy) / gamma_M1



# bending-normal force check      probably can igonore it, have to confirm with marco

#n = Ned/Nrd
#MnRd = Wpl*fyred*(1-math.pow(n,1.7))


print("Nrd: {} kN".format(round(Nrd/1000)))
print("VplRd: {} kN".format(round(VplRd/1000)))
print("MRd: {} kNm".format(round(MRd/1000000,2)))
#print("MnRd: {} kNm".format(round(MnRd/1000000,2)))  do not need to reduce moment from compression?


if Ned>0:
    combine_Utilisation = abs(Ned)/NtRd
elif Ned <= 0:
    combine_Utilisation = abs(Ned)/Nrd + Medy/MRd + Medz/MRd
print(combine_Utilisation)