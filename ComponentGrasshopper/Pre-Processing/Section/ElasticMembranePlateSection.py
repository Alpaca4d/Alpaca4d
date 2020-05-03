import math

def ElasticMembranePlateSection(sectionName, thickness, material):
    
    sectionName = sectionName
    thickness = thickness / 1000		# Input value in mm ---> Output m
    material = material
    sectionType = "ElasticMembranePlateSection"
    sectionProperties = sectionName + "_" + sectionType
    return [[sectionProperties, thickness, material]]


plateFiberSection = ElasticMembranePlateSection(sectionName, thickness, material)