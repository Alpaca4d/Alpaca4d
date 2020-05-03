import Rhino.Geometry as rg

def Solid( Mesh, Colour, material):
    
    if Mesh.Vertices.Count == 8:
        elementType = "bbarBrick"
    else:
        elementType = "FourNodeTetrahedron"
    newMesh = Mesh
    
    Material = material
    colour = Colour
    return[ [ newMesh , elementType, Material, colour ] ]

SolidWrapper = Solid( solid, Colour, material )
