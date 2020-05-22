import math
import Grasshopper as gh

def CircleCrossSection(sectionName, diameter, thickness, material):
    sectionName = sectionName
    shape = "circular"
    diameter = diameter / 1000 			# Input value in mm ---> Output m
    thickness = thickness / 1000        # Input value in mm ---> Output m
    if thickness == 0 or thickness == diameter / 2:
        Area = math.pow(diameter,2)/4  * math.pi
        Ay = Area * 0.9
        Az = Area * 0.9
        Iyy = math.pow(diameter,4)/64 * math.pi
        Izz = Iyy
        J = pow(diameter,4)/32 * math.pi
    elif thickness < diameter/2 and thickness >= 0:
        Area = (math.pow(diameter,2)-math.pow((diameter-2*thickness),2))/4 * math.pi
        Ay = Area * 0.9
        Az = Area * 0.9
        Iyy = (math.pow(diameter,4)-math.pow((diameter-2*thickness),4))/64 * math.pi
        Izz = Iyy
        J = (math.pow(diameter,4)-math.pow((diameter-2*thickness),4))/32 * math.pi
    else:
        msg = "Incorrect values. Thickness has to be greater than D/2 and greater than 0"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)

    material = material

    return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, diameter, thickness], sectionName ]]



CircleCrossSection = CircleCrossSection(sectionName, diameter, thickness, material)

