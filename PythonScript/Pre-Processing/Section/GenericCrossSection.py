import math 

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

genericCrossSection = GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, material)