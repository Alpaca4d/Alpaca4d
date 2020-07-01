"""Generate a Rectangular cross section
    Inputs:
        sectionName: Name of the section.
        base: Base of cross section [mm].
        height: Height of cross section [mm].
        uniaxialMaterial: Material element.
    Output:
       CrossSection: CrossSection element.
       """


import math
import Grasshopper as gh

def RectangularHollowCrossSection(sectionName, base, height, thickness, uniaxialMaterial):
    
    sectionName = sectionName
    shape = "rectangularHollow"
    base = base / 1000                      # Input value in mm ---> Output m
    height = height / 1000                  # Input value in mm ---> Output m
    thickness = thickness/1000              # Input value in mm ---> Output m
    Area = base * height - ( base - 2*thickness )*( height - 2*thickness )
    Ay = Area * 5/6
    Az = Area * 5/6
    Iyy = base*(height)**3/12 - ( base - 2*thickness )*( height - 2*thickness )**3/12
    Izz = base**3*height/12 - ( base - 2*thickness )**3*( height - 2*thickness )/12
    J = Iyy + Izz

    material = uniaxialMaterial

    return [[Area, Ay, Az, Iyy, Izz, J, material, [shape, base, height, thickness ], sectionName ]]

checkData = True

if sectionName is None:
    checkData = False
    msg = "input 'sectionName' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if base is None:
    checkData = False
    msg = "input 'base' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if height is None:
    checkData = False
    msg = "input 'height' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if thickness is None:
    checkData = False
    msg = "input 'thickness' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if uniaxialMaterial is None:
    checkData = False
    msg = "input 'uniaxialMaterial' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    CrossSection = RectangularHollowCrossSection(sectionName, base, height, thickness, uniaxialMaterial)