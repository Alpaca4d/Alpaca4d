import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp

def removeDuplicates(points, tol):
    uniquePoints = ghcomp.Kangaroo2Component.removeDuplicatePts(points, tol)
    return uniquePoints


def RTreeSeach(RTree, searchPoint, tol):

    #closestPoints = []
    closestIndices = []

    #event handler of type RTreeEventArgs
    def SearchCallback(sender, e):
        #closestPoints.Add(pointList[e.Id])
        closestIndices.Add(e.Id)

    for item in searchPoint:
        RTree.Search(rg.Sphere(item, tol), SearchCallback)
        ind = closestIndices
    
    return ind

def cleanTetrahedron(iMesh):
    iPoints = iMesh.Vertices.ToPoint3dArray()
    
    iPoint = []
    for pt in iPoints:
        iPoint.append(pt)
    
    tets = rg.Mesh()
    
    for pt in iPoint:
        tets.Vertices.Add(pt)
    
    
    tets.Faces.AddFace(0,2,1)
    tets.Faces.AddFace(0,2,3)
    tets.Faces.AddFace(0,3,1)
    tets.Faces.AddFace(1,3,2)
    
    tets.FaceNormals.ComputeFaceNormals()
    #tets.UnifyNormals()
    
    # find the center face and normal
    faceCenter = tets.Faces.GetFaceCenter(0)
    faceNormal = tets.FaceNormals.Item[0]
    
    
    
    polyCurvePt = iPoint[0:3] + [iPoint[0]] 
    faceEdge = rg.Polyline(polyCurvePt).ToNurbsCurve()
    
    
    # find number of intersection to understand if the normal is pointing outside
    line = rg.Line(faceCenter,  faceCenter + (1000 * faceNormal))
    line.Extend(0.001, 0.001)
    result = len( rg.Intersect.Intersection.MeshLine(tets, line)[0] )
    print(result)
    if result > 1:
        faceNormal = -faceNormal
    
    
    orientation = faceEdge.ClosedCurveOrientation(faceNormal)
    
    if (orientation != rg.CurveOrientation.Clockwise):
        print("I am here")
        #change the order if it is anticlockwise
        newTets = rg.Mesh()
    
        newTets.Vertices.Add(iPoint[0])
        newTets.Vertices.Add(iPoint[2])
        newTets.Vertices.Add(iPoint[1])
        newTets.Vertices.Add(iPoint[3])
        
        newTets.Faces.AddFace(0,2,1)
        newTets.Faces.AddFace(0,2,3)
        newTets.Faces.AddFace(0,3,1)
        newTets.Faces.AddFace(1,3,2)
        
        
        newTets.FaceNormals.ComputeFaceNormals()
        newTets.UnifyNormals()
    else:
        newTets = tets
    
    return newTets

def cleanHexahedron(Brick):


    Brick.FaceNormals.ComputeFaceNormals()
    #Brick.UnifyNormals()

    # find the center face and normal
    faceCenter = Brick.Faces.GetFaceCenter(0)
    faceNormal = Brick.FaceNormals.Item[0]


    polyCurvePts = []
    firstFace = []


    for item in Brick.Faces.GetTopologicalVertices(0):
        polyCurvePts.append( Brick.Vertices.Item[item] )
        firstFace.append(item)

    faceEdge = ghcomp.PolyLine(polyCurvePts , True).ToNurbsCurve()



    # find number of intersection to understand if the normal is pointing outside
    line = rg.Line(faceCenter,  faceCenter + (1000 * faceNormal))
    line.Extend(0.001, 0.001)
    result = len( rg.Intersect.Intersection.MeshLine(Brick, line)[0] )



    if result > 1:
        faceNormal = -faceNormal


    orientation = faceEdge.ClosedCurveOrientation(faceNormal)


    secondFace = []
    for item in Brick.Faces.GetTopologicalVertices(0):
        index = Brick.Vertices.GetConnectedVertices(item)
        for i in index:
            if i not in Brick.Faces.GetTopologicalVertices(0):
                secondFace.append(i)


    if (orientation != rg.CurveOrientation.Clockwise):
        firstFace.reverse()
        secondFace.reverse()


    # create new  Brick
    newBrick = rg.Mesh()

    for index in firstFace:
        newBrick.Vertices.Add( Brick.Vertices.Item[index] )
    for index in secondFace:
        newBrick.Vertices.Add( Brick.Vertices.Item[index] )

    newBrick.Faces.AddFace(0,1,2,3)
    newBrick.Faces.AddFace(4,5,6,7)
    newBrick.Faces.AddFace(1,2,6,5)
    newBrick.Faces.AddFace(0,3,7,4)
    newBrick.Faces.AddFace(0,1,5,4)
    newBrick.Faces.AddFace(3,2,6,7)

    newBrick.FaceNormals.ComputeFaceNormals()
    newBrick.UnifyNormals()

    return newBrick


def cleanShellMITC9(iMesh):
    
    newMesh = iMesh.Duplicate()
    polyCrv = newMesh.GetNakedEdges()[0]
    
    vts = polyCrv.ToArray()[:-1]
    
    vt_4 = (vts[0] + vts [1]) / 2.0
    vt_5 = (vts[1] + vts [2]) / 2.0
    vt_6 = (vts[2] + vts [3]) / 2.0
    vt_7 = (vts[3] + vts [0]) / 2.0
    vt_center = newMesh.Faces.GetFaceCenter(0)
    
    
    oMesh = rg.Mesh()
    for pt in vts:
        oMesh.Vertices.Add(pt)
    
    oMesh.Vertices.Add(vt_4)
    oMesh.Vertices.Add(vt_5)
    oMesh.Vertices.Add(vt_6)
    oMesh.Vertices.Add(vt_7)
    oMesh.Vertices.Add(vt_center)
    
    oMesh.Faces.AddFace(0,4,8,7)
    oMesh.Faces.AddFace(4,1,5,8)
    oMesh.Faces.AddFace(8,5,2,6)
    oMesh.Faces.AddFace(7,8,6,3)
    
    return oMesh


