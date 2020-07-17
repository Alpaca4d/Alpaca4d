"""Generate a  double T cross Section
    Inputs:
        sectionName: Name of the section.
        Bsup: Width upper Flange
        Binf: Width lower Flange
        H: Depth of section [ mm ]
        tsup: upper Flange thickness [ mm ]
        tinf: lower Flange thickness [ mm ]
        tw: Web thickness [ mm ]
        uniaxialMaterial: Material element.
    Output:
       CrossSection: CrossSection element.
       """

import math
import Grasshopper as gh

def doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, tw, uniaxialMaterial):
    sectionName = sectionName
    shape = "doubleT"
    Bsup, tsup, Binf, tinf, H, ta = Bsup/1000, tsup/1000, Binf/1000, tinf/1000, H/1000, tw/1000     # Input value in mm ---> Output m
    A1, y1 = Bsup*tsup, (H - tsup/2 )
    A2, y2 = ( H - tsup -tinf )*ta, (H-tsup-tinf)/2 + tinf
    A3, y3 = Binf*tinf, tinf/2
    yg = ( A1*y1 + A2*y2 + A3*y3 )/(A1 + A2 + A3 )
    Area = A1 + A2 + A3
    ky = Area/ A2
    kz = Area/ ( A1 + A3 )
    Ay = Area/ky # da riguardare
    Az = Area/ky # da riguardare
    Iyy = Bsup*tsup**3/12 + ( Bsup*tsup )*( H - yg - tsup/2 )**2 + ( H -tsup - tinf )**3/12 + ( H - tsup - tinf )*ta*( math.fabs(( H - tsup - tinf )/2 - yg) )**2 + Binf*tinf**3/12 + Binf*tinf*( yg - tinf/2 )**2
    Izz = tsup*Bsup**3/12 + tinf*Binf**3/12 + ( H -tsup - tinf )*ta**3/12
    #J = Iyy + Izz
    J = 1/3*( Bsup*tsup**3 + Binf*tinf**3 + ( H - tsup - tinf )*ta**3 ) # Prandt per sezioni sottile aperte

    material = uniaxialMaterial
    print( Iyy, Izz, yg )

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

if tw is None:
    checkData = False
    msg = "input 'tw' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if uniaxialMaterial is None:
    checkData = False
    msg = "input 'uniaxialMaterial' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    CrossSection = doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, tw, uniaxialMaterial)

