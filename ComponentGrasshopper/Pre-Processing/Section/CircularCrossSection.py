import math

def CircleCrossSection(sectionName, diameter, thickness, material):
    sectionName = sectionName
    shape = "circular"
    diameter = diameter / 1000 			# Input value in mm ---> Output m
    thickness = thickness / 1000 		# Input value in mm ---> Output m
    Area = (diameter/2)**2 * math.pi	
    Ay = Area * 0.9
    Az = Area * 0.9
    Iyy = pow(diameter,4)/64 * math.pi
    Izz = pow(diameter,4)/64 * math.pi
    J = pow(diameter,4)/32 * math.pi
    material = material

    return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, diameter, thickness], sectionName ]]

CircleCrossSection = CircleCrossSection(sectionName, diameter, thickness, material)
