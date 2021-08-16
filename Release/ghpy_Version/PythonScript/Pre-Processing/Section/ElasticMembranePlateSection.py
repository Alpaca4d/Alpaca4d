"""Generate a Plate cross section
    Inputs:
        sectionName: Name of the section.
        thickness: Height of the cross section [mm].
        nDMaterial: Material element.
    Output:
       CrossSection: Elastic Plate Section element.
       """

import math
import Grasshopper as gh

def ElasticMembranePlateSection(sectionName, thickness, nDMaterial):
    
    sectionName = sectionName
    thickness = thickness / 1000		# Input value in mm ---> Output m
    material = nDMaterial
    sectionType = "ElasticMembranePlateSection"
    sectionProperties = sectionName + "_" + sectionType
    return [[sectionProperties, thickness, material]]

checkData = True

if sectionName is None:
    checkData = False
    msg = "input 'sectionName' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if thickness is None:
    checkData = False
    msg = "input 'thickness' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if nDMaterial is None:
    checkData = False
    msg = "input 'nDMaterial' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    CrossSection = ElasticMembranePlateSection(sectionName, thickness, nDMaterial)