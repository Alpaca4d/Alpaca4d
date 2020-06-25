"""Generate a circular cross section
    Inputs:
        sectionName: Name of the section.
        thickness: Height of the cross section [mm].
        material: Material element.
    Output:
       plateFiberSection: Elastic Membrane Plate Section element.
       """

import math
import Grasshopper as gh

def ElasticMembranePlateSection(sectionName, thickness, material):
    
    sectionName = sectionName
    thickness = thickness / 1000		# Input value in mm ---> Output m
    material = material
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

if material is None:
    checkData = False
    msg = "input 'material' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    plateFiberSection = ElasticMembranePlateSection(sectionName, thickness, material)