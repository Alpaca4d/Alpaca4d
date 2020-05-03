import math

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


rectangularCrossSection = RectangularCrossSection(sectionName, base, height, material)