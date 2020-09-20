

import Rhino.Geometry as rg

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
            '''
            else :
                elementType.append(["FourNodeTetrahedron"]*3)
                
                if meshExpl[ index1 ][ index2 ].Vertices[0] == meshExpl[index1 + 1 ][ index2].Vertices[0] :
                    vertix1 = meshExpl[ index1 ][ index2 ].Vertices[0]
                    vertix2 = meshExpl[ index1 ][ index2 ].Vertices[1]
                    vertix3 = meshExpl[ index1 ][ index2 ].Vertices[2]
                    vertix4 = meshExpl[index1 + 1 ][ index2].Vertices[1]
                    vertix5 = meshExpl[index1 + 1 ][ index2].Vertices[2]
                    
                    vertixEle1 = [ vertix1, vertix2, vertix3, vertix4 ]
                    vertixEle2 = [ vertix1, vertix2, vertix3, vertix2 ]
                    
                    ele1 = rg.Mesh() # Tetrahedron 1
                    ele2 = rg.Mesh() # Tetrahedron 2
                    
                    ele1.Vertices.Add( vertix1 ) # 0 
                    ele1.Vertices.Add( vertix2 ) # 1
                    ele1.Vertices.Add( vertix3 ) # 2 
                    ele1.Vertices.Add( vertix4 ) # 3 
                    
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    
                    ele2.Vertices.Add( vertix1 ) # 0 
                    ele2.Vertices.Add( vertix2 ) # 1 
                    ele2.Vertices.Add( vertix3 ) # 2 
                    ele2.Vertices.Add( vertix2 ) # 3
    
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    
                    ele1.Faces.AddFace(0, 1, 4 ) # 0
                    ele1.Faces.AddFace(0, 1, 3 ) # 1
                    ele1.Faces.AddFace(0, 4, 3 ) # 2
                    ele1.Faces.AddFace(1, 3, 4 ) # 3
                    
                    ele2.Faces.AddFace(0, 1, 3 ) # 0
                    ele2.Faces.AddFace(0, 1, 2 ) # 1
                    ele2.Faces.AddFace(1, 2, 3 ) # 2
                    ele2.Faces.AddFace(0, 2, 3 ) # 3
                    
                    ele = [ ele1, ele2 ]
                    
                else :
                
                    vertix1 = meshExpl[ index1 ][ index2 ].Vertices[0]
                    vertix2 = meshExpl[ index1 ][ index2 ].Vertices[1]
                    vertix3 = meshExpl[ index1 ][ index2 ].Vertices[2]
                    vertix4 = meshExpl[index1 + 1 ][ index2].Vertices[0]
                    vertix5 = meshExpl[index1 + 1 ][ index2].Vertices[1]
                    vertix6 = meshExpl[index1 + 1 ][ index2].Vertices[2]
                    
                    vertixEle1 = [ vertix1, vertix2, vertix3, vertix6 ]
                    vertixEle2 = [ vertix4, vertix5, vertix6, vertix1 ]
                    vertixEle3 = [ vertix5, vertix6, vertix2, vertix1 ]
                    
                    vertix = [ vertixEle1, vertixEle2, vertixEle3 ]
                    
                    ele1 = rg.Mesh() # Tetrahedron 1
                    ele2 = rg.Mesh() # Tetrahedron 2
                    ele3 = rg.Mesh() # Tetrahedron 3
                    
                    ele1.Vertices.Add( vertix1 ) # 0 
                    ele1.Vertices.Add( vertix2 ) # 1
                    ele1.Vertices.Add( vertix3 ) # 2 
                    ele1.Vertices.Add( vertix6 ) # 3 
                    
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    ele1.VertexColors.Add(color)
                    
                    ele2.Vertices.Add( vertix4 ) # 0 
                    ele2.Vertices.Add( vertix5 ) # 1 
                    ele2.Vertices.Add( vertix6 ) # 2 
                    ele2.Vertices.Add( vertix1 ) # 3
    
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    ele2.VertexColors.Add(color)
                    
                    ele3.Vertices.Add( vertix5 ) # 0 
                    ele3.Vertices.Add( vertix6 ) # 1 
                    ele3.Vertices.Add( vertix2 ) # 2 
                    ele3.Vertices.Add( vertix1 ) # 3
                    
                    ele3.VertexColors.Add(color)
                    ele3.VertexColors.Add(color)
                    ele3.VertexColors.Add(color)
                    ele3.VertexColors.Add(color)
                    
                    ele1.Faces.AddFace(0, 1, 2 ) # 0
                    ele1.Faces.AddFace(0, 3, 1 ) # 1
                    ele1.Faces.AddFace(0, 3, 2 ) # 2
                    ele1.Faces.AddFace(1, 3, 2 ) # 3
                    
                    ele2.Faces.AddFace(0, 1, 2 ) # 0
                    ele2.Faces.AddFace(0, 3, 1 ) # 1
                    ele2.Faces.AddFace(0, 3, 2 ) # 2
                    ele2.Faces.AddFace(1, 3, 2 ) # 3
                    
                    ele3.Faces.AddFace(0, 1, 2 ) # 0
                    ele3.Faces.AddFace(0, 3, 1 ) # 1
                    ele3.Faces.AddFace(0, 3, 2 ) # 2
                    ele3.Faces.AddFace(1, 3, 2 ) # 3
                    
                    ele = [ ele1, ele2, ele3 ]
            
            solid.append(ele)
            Vertix.append( vertix )
            '''
    return solid, elementType

Brick, type = brick( MeshSeries )



