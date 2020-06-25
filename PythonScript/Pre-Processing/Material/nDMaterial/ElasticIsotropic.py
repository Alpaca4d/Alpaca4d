"""Generate a n-Dimensional Elastic Isotropic Material
    Inputs:
        matName: Name of the material.
        E: Young's Modulus [MPa].
        G: Tangential Modulus [MPa].
        v: Poisson ratio.
        rho: specific weight [kN/m3].
        fy: Yield stress value of the material [MPa]
    Output:
       elasticMaterialWrapper: Material element.
       """


import Grasshopper as gh

def ElasticMaterial(matName, E, G, v, rho, fy):

    E = E * 1000                               # Input value in N/mm2 ---> Output kN/m2
    if v == None:
    	G = G * 1000                           # Input value in N/mm2 ---> Output kN/m2
    	v = (E / (2 * G)) - 1
    else:
    	G = E / (2 * (1 + v))

    rho = rho                                  # Force Density
    fy = fy                                    # Input value in N/mm2
    materialDimension = "nDMaterial"
    materialType = "ElasticIsotropic"
    matName = matName + "_" + materialDimension + "_" + materialType

    return [[matName, E, G, v, rho, fy, materialType]]

checkData = True

if matName is None:
    checkData = False
    msg = "input 'matName' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if E is None:
    checkData = False
    msg = "input 'E' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

"""
if G or v is None:
    checkData = False
    msg = "input 'G' or 'v' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
"""

if rho is None:
    checkData = False
    msg = "input 'rho' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    elasticMaterialWrapper = ElasticMaterial(matName, E, G, v, rho, fy)
