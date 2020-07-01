"""Generate a Brick Element
    Inputs:
        Brick: Closed Mesh representing the structural element.
        Colour: Colour of the element.
        nDMaterial: Material element.
    Output:
       solidWrapper: Solid with properties.
       """


import Rhino.Geometry as rg
import Grasshopper as gh

def Solid( Brick, Colour, nDMaterial):
    
    if Brick.Vertices.Count == 8:
        elementType = "bbarBrick"
    elif Brick.Vertices.Count == 4:
        elementType = "FourNodeTetrahedron"
    else:
    	msg = "Not a valid Mesh"
    	ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
    newMesh = Brick
    
    Material = nDMaterial
    colour = Colour
    return[ [ newMesh , elementType, Material, colour ] ]


checkData = True

if Brick is None:
    checkData = False
    msg = "input 'Brick' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if nDMaterial is None:
    checkData = False
    msg = "input 'nDMaterial' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    solidWrapper = Solid( Brick, Colour, nDMaterial )