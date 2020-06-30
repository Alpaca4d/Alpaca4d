import Rhino.Geometry as rg
import Grasshopper as gh

def Solid( Mesh, Colour, material):
    
    if Mesh.Vertices.Count == 8:
        elementType = "bbarBrick"
    elif Mesh.Vertices.Count == 4:
        elementType = "FourNodeTetrahedron"
    else:
    	msg = "Not a valid Mesh"
    	ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
    newMesh = Mesh
    
    Material = material
    colour = Colour
    return[ [ newMesh , elementType, Material, colour ] ]


checkData = True

if Mesh is None:
    checkData = False
    msg = "input 'Mesh' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if material is None:
    checkData = False
    msg = "input 'CrossSection' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    SolidWrapper = Solid( solid, Colour, material )