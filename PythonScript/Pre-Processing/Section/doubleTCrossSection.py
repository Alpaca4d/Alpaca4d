import math
import Grasshopper as gh

def doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, ta, uniaxialMaterial):
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
    Iyy = Bsup*tsup**3 + ( Bsup*tsup )*( H - yg - tsup/2 )**2 + ( H -tsup - tinf )**3*ta + ( H - tsup - tinf )*ta*( (H - tsup - tinf)/2 - yg ) + Binf*tinf**3 + Binf*tinf*( yg - tinf )**2
    Izz = tsup*Bsup**3 + tinf*Binf**3 + ( H -tsup - tinf )*ta**3
    J = Iyy + Izz

    material = uniaxialMaterial

    return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, Bsup, tsup, Binf, tinf, H, ta, yg], sectionName ]]

checkData = True

if sectionName is None:
    checkData = False
    msg = "input 'sectionName' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Bsup is None:
    checkData = False
    msg = "input 'Bsup' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if tsup is None:
    checkData = False
    msg = "input 'tsup' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Binf is None:
    checkData = False
    msg = "input 'Binf' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if tinf is None:
    checkData = False
    msg = "input 'tinf' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if H is None:
    checkData = False
    msg = "input 'H' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if ta is None:
    checkData = False
    msg = "input 'ta' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if uniaxialMaterial is None:
    checkData = False
    msg = "input 'uniaxialMaterial' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    CrossSection = doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, ta, uniaxialMaterial)

