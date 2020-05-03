import Rhino.Geometry as rg

def MeshToShell(Mesh, Colour, CrossSection):
    
    Mesh.Unweld(0, True)
    
    elementType = []
    if Mesh.Vertices.Count == 4:
        elementType = "ShellDKGQ"
    else:
        elementType = "ShellDKGT"
    newMesh = Mesh
    
    CrossSection = CrossSection
    colour = Colour
    return[ [ newMesh , elementType, CrossSection, colour] ]

shellWrapper = MeshToShell(Mesh, Colour, CrossSection)

