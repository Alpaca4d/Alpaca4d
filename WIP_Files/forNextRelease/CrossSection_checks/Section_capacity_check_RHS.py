#section capacity check RHS

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

#if t>= dy or dz:  #raise ValueError('Thickness t is greater than section depth') 

Iy = (dz* math.pow(dy,3)/12) - ((dz-2*t)*math.pow((dy-2*t),3)/12)
Iz = (dy*math.pow(dz,3)/12) - ((dy-2*t)*math.pow((dz-2*t),3)/12)

alpham = [0.13, 0.21, 0.34, 0.49, 0.76]  #buckling curves


def classSection_RHS_Compression_Y(dy,t,fy):  #class section for compression in Y
    epsilon = math.sqrt(235/fy)
    
    if (dy-2*t)/t <= 33 * math.pow(epsilon, 2):
        classSection = 1
    elif (dy-2*t)/t <= 38 * math.pow(epsilon, 2):
        classSection = 2
    elif (dy-2*t)/t <= 42 * math.pow(epsilon, 2):
        classSection = 3
    else:
        raise ValueError('section in class 4')
    return classSection


def classSection_RHS_Compression_Z(dz,t,fy):  #class section for compression in Z
    epsilon = math.sqrt(235/fy)
    
    if (dz-2*t)/t <= 33*math.pow(epsilon, 2):
        classSection = 1
    elif (dz-2*t)/t <= 38 * math.pow(epsilon, 2):
        classSection = 2
    elif (dz-2*t)/t <= 42 * math.pow(epsilon, 2):
        classSection = 3
    else:
        raise ValueError('section in class 4')
    return classSection

classSection_Compression_Y = classSection_RHS_Compression_Y(dy,t,fy)
classSection_Compression_Z = classSection_RHS_Compression_Z(dz,t,fy)

def classSection_RHS_Moment_Y(dy,t,fy):  #class section for pure moment in Y
    epsilon = math.sqrt(235/fy)
    
    if (dy-2*t)/t <= 72 * math.pow(epsilon, 2):
        classSection = 1
    elif (dy-2*t)/t <= 83 * math.pow(epsilon, 2):
        classSection = 2
    elif (dy-2*t)/t <= 124 * math.pow(epsilon, 2):
        classSection = 3
    else:
        raise ValueError('section in class 4')
    return classSection

def classSection_RHS_Moment_Z(dz,t,fy):  #class section for pure moment in Z
    epsilon = math.sqrt(235/fy)
    
    if (dz-2*t)/t <= 72 * math.pow(epsilon, 2):
        classSection = 1
    elif (dz-2*t)/t <= 83 * math.pow(epsilon, 2):
        classSection = 2
    elif (dz-2*t)/t <= 124 * math.pow(epsilon, 2):
        classSection = 3
    else:
        raise ValueError('section in class 4')
    return classSection

classSection_Compression_Y = classSection_RHS_Moment_Y(dy,t,fy)
classSection_Compression_Z = classSection_RHS_Moment_Z(dz,t,fy)


classSection = classSection_RHS_Moment_Y(dy,t,fy)
if classSection == 1 or classSection == 2:
    Wly = dz*math.pow(dy,2)/4 - ((dz-2*t)*math.pow(dy-2*t,2)/4) #plastic capacity, Wply
elif classSection == 3: 
    Wly = Iy/(dy/2)                                              #elastic capacity, Wely

classSection = classSection_RHS_Moment_Z(dz,t,fy)
if classSection == 1 or classSection == 2:       
    Wlz = dy*math.pow(dz,2)/4 - ((dy-2*t)*math.pow(dz-2*t,2)/4)       #plastic capacity, Wplz
elif classSection == 3:
    Wlz = Iz/(dz/2)                                                 #elastic capacity, Welz


if t < dy/2 and t < dz/2:
    Area = 2*t*(dy + dz - 2*t)
else:
    Area = None

#Shear Area
Av_z = Area*dy/(dy+dz)
Av_y = Area*dz/(dy+dz)

#Torsional property
h0 =2*((dy-t) + (dz-t))
Ah = (dy-t)*(dz-t)
k=2*Ah*t/h0
It= (math.pow(t,3)*h0/3) + 2*k*Ah  #torsional constant
Wt= It/(t+ k/t)    #torsional modulus
Trd= Wt*(fy/math.sqrt(3))/gamma_M0

# tension check
def tensionCheck(Ned, Area, fy, gammaM0):
    NplRd = (Area * fy) / gammaM0    #require sign to be assigned to tesion force
    return NplRd


NtRd = tensionCheck(Ned, Area, fy, gamma_M0)

# shear Check

def shearCheck(Vedy,Vedz, Avy,Avz, fy, gammaM0, T):
    VplRdy = (Avy * (fy/math.sqrt(3)) ) / gammaM0
    VplRdz = (Avz * (fy/math.sqrt(3)) ) / gammaM0
    if T !=0 :
        taued = T/Wt   #shear stress due to torsion, where T is saint venant torsion
    VplRdy = (1-(taued/(fy/math.sqrt(3)/ gammaM0)))*VplRdy
    VplRdz = (1-(taued/(fy/math.sqrt(3)/ gammaM0)))*VplRdz
    shearUtilisation = Vedy/VplRdy + Vedz/VplRdz # for combined shear in both direction
    
    return VplRdy, VplRdz, shearUtilisation

shearUtilisation= shearCheck(Vedy,Vedz, Av_y,Av_z, fy, gamma_M0, T)[2]


if shearUtilisation < 0.5:
    rho = 0
else:
    rho = math.pow( ((2*shearUtilisation) -1),2)  # does this make sense? (shear Utilization)
fy = (1-rho)*fy

# compression Check

def compressioncheck(Ned,Area,fy,Lcry,Lcrz,gammaM0, type):
    Ncpl =  Area*fy
    Ncry = (math.pow(math.pi,2)*E*Iy)/math.pow(Lcry,2)   #euler critical buckling y direction
    Ncrz = (math.pow(math.pi,2)*E*Iz)/math.pow(Lcrz,2)   #euler critical buckling z direction
    Ncr= min(Ncry, Ncrz)
    Lamda = math.sqrt((Area*fy)/Ncr)
    if fy <420 :
        if type==0:
            alpha = alpham[1]
        else:
            alpha = alpham[3]
    else :
        if type ==1:    #cold form section
            alpha = alpham[0]
        else:
            alpha = alpham[3]
    phi= 0.5*(1 + alpha*(Lamda - 0.2) + math.pow(Lamda,2))
    gamma = 1/(phi+ math.sqrt(math.pow(phi,2) - math.pow(Lamda,2)))
    Nbrd= gamma*Ncpl
    Nrd= min(Ncpl, Nbrd)

    return Nrd


Nrd = compressioncheck(Ned,Area,fy,Lcry, Lcrz,gamma_M0, type)

print("classSection: {}".format(classSection))
print("Ned/Nrd = {}".format(Ned/Nrd))
print("reduced yield strength= {}".format(fy))

# bending check
MRdy = Wly*fy/gamma_M0
MRdz = Wlz*fy/gamma_M0


# bending-cpmpression reduction in bending capacity due to compression probably can igonore it, have to confirm with marco

#n = Ned/Nrd
#MnRd = Wpl*fyred*(1-math.pow(n,1.7))


print("Nrd: {} kN".format(round(Nrd/1000)))
print("VplRd: {} kN".format(round(shearUtilisation/1000)))
print("Mrdy: {} kNm".format(round(MRdy/1000000,2)))
print("Mrdz: {} kNm".format(round(MRdz/1000000,2)))
#print("MnRd: {} kNm".format(round(MnRd/1000000,2)))  do not need to reduce moment from compression?


if Ned>0:
    combine_Utilisation = abs(Ned)/NtRd
elif Ned <= 0:
    combine_Utilisation = abs(Ned)/Nrd + Medy/MRdy + Medz/MRdz
print(combine_Utilisation)