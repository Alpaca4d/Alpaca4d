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

if Material is None:
    checkData = False
    msg = "input 'Material' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    genericCrossSection = GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, material)