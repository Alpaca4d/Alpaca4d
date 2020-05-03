def ElasticMaterial(matName, E, G, v, rho, fy):

    E = E * 1000                               # Input value in N/mm2 ---> Output kN/m2
    if v == None:
    	G = G * 1000                           # Input value in N/mm2 ---> Output kN/m2
    	v = (E / (2 * G)) - 1
    else:
    	G = E / (2 * (1 + v))

    rho = rho                                  # Input value kN/m3
    
    fy = fy                                    # Input value in N/mm2
    materialDimension = "uniaxialMaterial"
    materialType = "Elastic"
    matName = matName + "_" + materialDimension + "_" + materialType
    
    return [[matName, E, G, v, rho, fy, materialType]]


elasticMaterialWrapper = ElasticMaterial(matName, E, G, v, rho, fy)
