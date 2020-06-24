import Rhino.Geometry as rg
import Grasshopper as gh

def MeshToShell(Mesh, Colour, CrossSection):
    
    Mesh.Unweld(0, True)
    
    elementType = []
    if Mesh.Vertices.Count == 4:
        elementType = "ShellMITC4"
    else:
        elementType = "ShellDKGT"
    newMesh = Mesh
    
    CrossSection = CrossSection
    colour = Colour
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
    shellWrapper = MeshToShell(Mesh, Colour, CrossSection)





