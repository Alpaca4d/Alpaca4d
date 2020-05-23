import math
import Grasshopper as gh

def doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, ta, material):
    sectionName = sectionName
    shape = "doubleT"
    Bsup, tsup, Binf, tinf, H, ta = Bsup/1000, tsup/1000, Binf/1000, tinf/1000, H/1000, ta/1000     # Input value in mm ---> Output m
    A1, y1 = Bsup*tsup, (H-tsup/2)
    A2, y2 = ( H - tsup -tinf )*ta, (H-tsup-tinf)/2
    A3, y3 = Binf*tinf, tinf/2
    yg = ( A1*y1 + A2*y2 + A3*y3 )/(A1 + A2 + A3 )
    Area = A1 + A2 + A3
    Ay = Area*0.2 # da cambiare
    Az = Area*0.2 # da cambiare
    Iyy = Bsup*tsup**3 + ( Bsup*tsup )*( H - yg - tsup/2 )**2 + ( H -tsup - ta )**3*ta + ( H - tsup - ta )*ta*( (H - tsup - ta)/2 - yg ) + Binf*tinf**3 + Binf*tinf*( yg - tinf )**2
    Izz = Iyy # da cambiare
    J = Iyy + Izz

    material = material

    return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, Bsup, tsup, Binf, tinf, H, ta, yg], sectionName ]]



doubleTCrossSection = doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, ta, material)

