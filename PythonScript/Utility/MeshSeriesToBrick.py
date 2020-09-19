"""Generate a Brick element from a list of mesh .
the faces of the mesh '0' will be connected with the faces of the meshes '1' generating a brick element ( cube ).
Each mesh in the list must have the same number of faces.
    Inputs:
        MeshSeries: quadMesh list with the same number of faces .
    Output:
        Brick: Mesh with 6 faces and 8 nodes.
"""

import Rhino.Geometry as rg
import Grasshopper as gh

def MeshToShell(Mesh):
    
    Mesh.Unweld(0, True)
    mesh = Mesh.ExplodeAtUnweldedEdges()
    #print( len(mesh) )
    newMesh = []
    elementType = []
    for explodedMesh in mesh:
        newMesh.append(explodedMesh)
    return newMesh 

def brick( MeshList ):
    meshExpl = []
    Vertix = []
    elementType = []
    solid = []
    a = rg.Mesh.DuplicateMesh( MeshList[0] ) #.Unweld(0, True)
    a.Unweld(0, True)
    b = a.ExplodeAtUnweldedEdges()
    if len( b ) > 0 :
        for Mesh in MeshList:
            shellWrapper = MeshToShell(Mesh)
            meshExpl.append( shellWrapper )
        for index1 in range(0, len(MeshList)-1):
            for index2 in range(0, len(meshExpl[0])):
                if meshExpl[ index1 ][ index2 ].Vertices.Count == 4:
                    
                    elementType.append("stdBrick")
                    vertix1 = meshExpl[ index1 ][ index2 ].Vertices[0]
                    vertix2 = meshExpl[ index1 ][ index2 ].Vertices[1]
                    vertix3 = meshExpl[ index1 ][ index2 ].Vertices[2]
                    vertix4 = meshExpl[ index1 ][ index2 ].Vertices[3]
                    vertix5 = meshExpl[index1 + 1 ][ index2].Vertices[0]
                    vertix6 = meshExpl[index1 + 1 ][ index2].Vertices[1]
                    vertix7 = meshExpl[index1 + 1 ][ index2].Vertices[2]
                    vertix8 = meshExpl[index1 + 1 ][ index2].Vertices[3]
                    
                    vertix = [ vertix1, vertix2, vertix3, vertix4,
                    vertix5, vertix6, vertix7, vertix8 ]
                    
                    ele = rg.Mesh()
                    
                    ele.Vertices.Add( vertix1 ) # 0 
                    ele.Vertices.Add( vertix2 ) # 1
                    ele.Vertices.Add( vertix3 ) # 2
                    ele.Vertices.Add( vertix4 ) # 3
                    ele.Vertices.Add( vertix5 ) # 4
                    ele.Vertices.Add( vertix6 ) # 5
                    ele.Vertices.Add( vertix7 ) # 6
                    ele.Vertices.Add( vertix8 ) # 7
                    
                    ele.Faces.AddFace(0, 1, 2, 3) # 0
                    ele.Faces.AddFace(4, 5, 6, 7) # 1
                    ele.Faces.AddFace(0, 1, 5, 4) # 2
                    ele.Faces.AddFace(3, 2, 6, 7) # 3
                    ele.Faces.AddFace(1, 5, 6, 2) # 4
                    ele.Faces.AddFace(0, 4, 7, 3) # 5
                solid.append(ele)
                #ele.IsClosed()
                    
    else:
        for index1 in range(0, len(MeshList)-1):
            elementType.append("stdBrick")
            vertix1 = MeshList[ index1 ].Vertices[0]
            vertix2 = MeshList[ index1 ].Vertices[1]
            vertix3 = MeshList[ index1 ].Vertices[2]
            vertix4 = MeshList[ index1 ].Vertices[3]
            vertix5 = MeshList[index1 + 1 ].Vertices[0]
            vertix6 = MeshList[index1 + 1 ].Vertices[1]
            vertix7 = MeshList[index1 + 1 ].Vertices[2]
            vertix8 = MeshList[index1 + 1 ].Vertices[3]
            
            vertix = [ vertix1, vertix2, vertix3, vertix4,
            vertix5, vertix6, vertix7, vertix8 ]
            
            ele = rg.Mesh()
            
            ele.Vertices.Add( vertix1 ) # 0 
            ele.Vertices.Add( vertix2 ) # 1
            ele.Vertices.Add( vertix3 ) # 2
            ele.Vertices.Add( vertix4 ) # 3
            ele.Vertices.Add( vertix5 ) # 4
            ele.Vertices.Add( vertix6 ) # 5
            ele.Vertices.Add( vertix7 ) # 6
            ele.Vertices.Add( vertix8 ) # 7
            
            ele.Faces.AddFace(0, 1, 2, 3) # 0
            ele.Faces.AddFace(4, 5, 6, 7) # 1
            ele.Faces.AddFace(0, 1, 5, 4) # 2
            ele.Faces.AddFace(3, 2, 6, 7) # 3
            ele.Faces.AddFace(1, 5, 6, 2) # 4
            ele.Faces.AddFace(0, 4, 7, 3) # 5
            
            solid.append(ele)
    return solid

checkData = True

if not MeshSeries or len(MeshSeries) == 1 :  #is not None:
    checkData = False
    msg = "input 'MeshSeries' failed to collect data"
    ghenv.Component.AddRuntimeMessage( gh.Kernel.GH_RuntimeMessageLevel.Warning, msg )

if len(MeshSeries) == 1 :
    checkData = False
    msg = "Provide at least 2 meshes"
    ghenv.Component.AddRuntimeMessage( gh.Kernel.GH_RuntimeMessageLevel.Warning, msg )

if checkData != False:
    Brick= brick( MeshSeries )


