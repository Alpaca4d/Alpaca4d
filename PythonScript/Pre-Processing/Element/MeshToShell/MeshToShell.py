"""Generate a Shell MITC4 element
    Inputs:
        Mesh: QuadMesh representing the structural element.
        CrossSection: Cross section of the mesh.
        Colour: Colour of the element.
    Output:
       shellWrapper: Shell with properties.
       """


import Rhino.Geometry as rg
import Grasshopper as gh
from System.Drawing import Color 

def MeshToShell(Mesh, Colour, CrossSection):
    
    Mesh.Unweld(0, True)
    
    elementType = []
    if Mesh.Vertices.Count == 4:
        elementType = "ShellMITC4"
        if Colour is None:
            colour = Color.FromArgb(49, 159, 255)
        else:
            colour = Colour
    else:
        elementType = "shellDKGT"
        if Colour is None:
            colour = Color.FromArgb(49, 159, 255)
        else:
            colour = Colour
    newMesh = Mesh
    
    CrossSection = CrossSection
    return[ [ newMesh , elementType, CrossSection, colour] ]

checkData = True

if Mesh is None:
    checkData = False
    msg = "input 'Mesh' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if CrossSection is None:
    checkData = False
    msg = "input 'CrossSection' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    Mesh.Unweld(0, True)
    explodedMesh = Mesh.ExplodeAtUnweldedEdges()
    shellWrapper = []
    if explodedMesh.Length > 0:
        for mesh in explodedMesh:
            shellWrapper.append(MeshToShell(mesh, Colour, CrossSection))
    elif explodedMesh.Length == 0:
            shellWrapper.append(MeshToShell(Mesh, Colour, CrossSection))