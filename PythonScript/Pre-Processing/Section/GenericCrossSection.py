"""Generate a Generic cross section
    Inputs:
        sectionName: Name of the section.
        Area: Area of cross section [mm2].
        Ay: Shear area along Y local axis [mm2].
        Az: Shear area along Z local axis [mm2].
        Iyy: Moment of Inertia about Y local axis [mm4].
        Izz: Moment of Inertia about Z local axis [mm4].
        J: Primary torsional moment of Inertia about X local axis [mm4].
        material: Material element.
    Output:
       CrossSection: CrossSection element.
       """


import math
import Grasshopper as gh

def GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, Material):
    sectionName = sectionName
    shape = "Generic"
    Area = Area / 10**6		# Input value in mm2 ---> Output m
    Ay = Ay / 10**6			# Input value in mm2 ---> Output m
    Az = Az / 10**6			# Input value in mm2 ---> Output m
    Iyy = Iyy / 10**12		# Input value in mm4 ---> Output m
    Izz = Izz / 10*12 		# Input value in mm4 ---> Output m
    J = J / 10**12 			# Input value in mm4 ---> Output m
    radius = math.pow(2*math.pi*Area,0.5)
    material = Material

    return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, radius ], sectionName ]]

checkData = True

if sectionName is None:
    checkData = False
    msg = "input 'sectionName' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Area is None:
    checkData = False
    msg = "input 'Area' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Ay is None:
    checkData = False
    msg = "input 'Ay' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Az is None:
    checkData = False
    msg = "input 'Az' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Iyy is None:
    checkData = False
    msg = "input 'Iyy' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Izz is None:
    checkData = False
    msg = "input 'Izz' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if J is None:
    checkData = False
    msg = "input 'J' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if material is None:
    checkData = False
    msg = "input 'material' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    CrossSection = GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, material)