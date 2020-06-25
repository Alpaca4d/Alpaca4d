"""Generate a Rectangular cross section
    Inputs:
        sectionName: Name of the section.
        base: Base of cross section [mm].
        height: Height of cross section [mm].
        material: Material element.
    Output:
       CrossSection: CrossSection element.
       """


import math
import Grasshopper as gh

def RectangularCrossSection(sectionName, base, height, material):
    
    sectionName = sectionName
    shape = "rectangular"
    base = base / 1000                      # Input value in mm ---> Output m
    height = height / 1000                  # Input value in mm ---> Output m
    Area = base * height
    Ay = Area * 5/6
    Az = Area * 5/6
    Iyy = base*pow(height,3)/12
    Izz = pow(base,3)*height/12
    if height < base:
        k = 1 / (3+4.1*pow((height/base),3/2))
        J = k*base*pow(height,3)
    else:
        k = 1 / (3+4.1*pow((base/height),3/2))
        J = k*height*pow(base,3)
    material = material

    return [[Area, Ay, Az, Iyy, Izz, J, material, [shape, base, height], sectionName ]]

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

if material is None:
    checkData = False
    msg = "input 'material' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    CrossSection = RectangularCrossSection(sectionName, base, height, material)

    print( CrossSection )