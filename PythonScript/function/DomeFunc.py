import math as mt

def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]

## Funzione rettangolo ##
def AddRectangleFromCenter(plane, width, height):
    a = plane.PointAt(-width * 0.5, -height * 0.5 )
    b = plane.PointAt(-width * 0.5,  height * 0.5 )
    c = plane.PointAt( width * 0.5,  height * 0.5 )
    d = plane.PointAt( width * 0.5,  -height * 0.5 )
    #rectangle = rg.PolylineCurve( [a, b, c, d, a] )
    rectangle  = [a, b, c, d] 
    return rectangle

## Funzione cerchio ##
def AddCircleFromCenter( plane, radius):
    t = linspace( 0 , 2*mt.pi, 20 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle

def gradientJet(value, valueMax, valueMin):

    listcolo = [[0, 0, 102 ],
                [0, 0, 255],
                [0, 64, 255],
                [0, 128, 255],
                [0, 191, 255],
                [0, 255, 255],
                [0, 255, 191],
                [0, 255, 128],
                [0, 255, 64],
                [0, 255, 0],
                [64, 255, 0],
                [128, 255, 0],
                [191, 255, 0],
                [255, 255, 0],
                [255, 191, 0],
                [255, 128, 0],
                [255, 64, 0],
                [255, 0, 0],
                [230, 0, 0],
                [204, 0, 0]]

    #domain = linspace( valueMin,  valueMax, len( listcolo ) )
    n = len( listcolo )
    diff = (float(valueMax) - valueMin)/( n - 1 )
    domain = [diff * i + valueMin  for i in range(n)]
    #print(domain)
    for i in range(1,n):
        if  domain[i-1] <= value <= domain[i]:
            return listcolo[ i-1 ]
        elif  valueMax <= value <= valueMax + 0.0001 :
            return listcolo[ -1 ]
        elif  valueMin -0.0001 <= value <= valueMin :
            return listcolo[ 0 ]


def scaleAutomatic( Num , Den ):
    if Den < 0.1 :
        return Num
    else :
        return Num*1/Den

## -------------FUNZIONI DI FORMA PER TRAVE DI TYMOSHENKO------------------ ##

def alphat( E, G, I, At ):
    return (E*I)/(G*At)

## Spostamenti e rotazioni ##
def spostu( x, L, uI, uJ ):
    return -(-L*uI + uI*x - uJ*x)/L
    
def spostv( x, L, vI, vJ, thetaI, thetaJ, alphay ):
    return (L**3*thetaI*x + L**3*vI - 2*L**2*thetaI*x**2 - L**2*thetaJ*x**2 + 6*L*alphay*thetaI*x - 6*L*alphay*thetaJ*x + 12*L*alphay*vI + L*thetaI*x**3 + L*thetaJ*x**3 - 3*L*vI*x**2 + 3*L*vJ*x**2 - 6*alphay*thetaI*x**2 + 6*alphay*thetaJ*x**2 - 12*alphay*vI*x + 12*alphay*vJ*x + 2*vI*x**3 - 2*vJ*x**3)/(L*(L**2 + 12*alphay))
    
def spostw( x, L, wI, wJ, psiI, psiJ, alphaz ):
    return -(L**3*psiI*x - L**3*wI - 2*L**2*psiI*x**2 - L**2*psiJ*x**2 - 6*L*alphaz*psiI*x + 6*L*alphaz*psiJ*x + 12*L*alphaz*wI + L*psiI*x**3 + L*psiJ*x**3 + 3*L*wI*x**2 - 3*L*wJ*x**2 + 6*alphaz*psiI*x**2 - 6*alphaz*psiJ*x**2 - 12*alphaz*wI*x + 12*alphaz*wJ*x - 2*wI*x**3 + 2*wJ*x**3)/(L*(L**2 - 12*alphaz))
    
def thetaz(x, L, vI, vJ, thetaI, thetaJ, alphay): 
    return (L**3*thetaI - 4*L**2*thetaI*x - 2*L**2*thetaJ*x + 12*L*alphay*thetaI + 3*L*thetaI*x**2 + 3*L*thetaJ*x**2 - 6*L*vI*x + 6*L*vJ*x - 12*alphay*thetaI*x + 12*alphay*thetaJ*x + 6*vI*x**2 - 6*vJ*x**2)/(L*(L**2 + 12*alphay))
    
def phix(x, L, phiI, phiJ):
    return -(-L*phiI + phiI*x - phiJ*x)/L

def psiy(x, L, wI, wJ, psiI, psiJ, alphaz): 
    return (L**3*psiI - 4*L**2*psiI*x - 2*L**2*psiJ*x - 12*L*alphaz*psiI + 3*L*psiI*x**2 + 3*L*psiJ*x**2 + 6*L*wI*x - 6*L*wJ*x + 12*alphaz*psiI*x - 12*alphaz*psiJ*x - 6*wI*x**2 + 6*wJ*x**2)/(L*(L**2 - 12*alphaz))
    
def gammay( L, vI, vJ, thetaI, thetaJ, alphay): 

    return (L*thetaI + L*thetaJ + 2*vI - 2*vJ)/(L*(L**2 + 12*alphay))
    
def gammaz( L, wI, wJ, psiI, psiJ, alphaz):

    return -(L*psiI + L*psiJ - 2*wI + 2*wJ)/(L*(L**2 - 12*alphaz))

##------------------------------------------------------------------------- --##

## Mesh from close section eith gradient color ##
def meshLoft3( point, color ):
    meshEle = rg.Mesh()
    for i in range(0,len(point)):
        for j in range(0, len(point[0])):
            vertix = point[i][j]
            meshEle.Vertices.Add( vertix ) 
            #meshEle.VertexColors.Add( color[0],color[1],color[2] );
    k = len(point[0])
    for i in range(0,len(point)-1):
        for j in range(0, len(point[0])):
            if j < k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = index2 + 1
                index4 = index1 + 1
            elif j == k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = (i+1)*k
                index4 = i*k
            meshEle.Faces.AddFace(index1, index2, index3, index4)
            #rs.ObjectColor(scyl,(255,0,0))
    colour = rs.CreateColor( color[0], color[1], color[2] )
    meshEle.VertexColors.CreateMonotoneMesh( colour )
    return meshEle

def Beam( ele, node):
    TagEle = ele[1]
    indexStart = ele[2][0]
    indexEnd = ele[2][1]
    color = ele[16]
    dimSection = ele[14]
    pointStart = node.get( indexStart  , "never")
    pointEnd = node.get( indexEnd  , "never")
    line = rg.LineCurve( pointStart, pointEnd )
    axis3 = pointEnd - pointStart
    axis3.Unitize()
    axis1 =  rg.Vector3d( ele[13][0], ele[13][1], ele[13][2]  )
    axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
    versor = [ axis1, axis2, axis3 ] 
    
    planeStart = rg.Plane(pointStart, axis1, axis2)
    planeEnd = rg.Plane(pointEnd, axis1, axis2)
    plane = [ planeStart, planeEnd ]
    
    sectionForm = []
    sectionPolyline = []
    for sectionPlane in plane:
        
        if dimSection[0] == 'rectangular' :
            width, height = dimSection[1], dimSection[2]
            section = dg.AddRectangleFromCenter( sectionPlane, width, height )
            
        if dimSection[0] == 'circular' :
            radius  = dimSection[2]
            section = AddCircleFromCenter( sectionPlane, radius )
            
        sectionForm.append( section )
        
        
    meshExtr = meshLoft3( sectionForm,  color )
    colour = rs.CreateColor( color[0], color[1], color[2] )
    return [ line, meshExtr, colour ]


def TetraSolid( ele, node ):
    
    eleTag = ele[1]
    eleNodeTag = ele[2]
    color = ele[5]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    ## CREO IL MODELLO DEFORMATO  ##
    point1 =  node.get( index1 -1 , "never")
    point2 =  node.get( index2 -1 , "never")
    point3 =  node.get( index3 -1 , "never")
    point4 =  node.get( index4 -1 , "never")
    
    #print( type(pointDef1) )
    
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( point1 ) #0
    shellDefModel.Vertices.Add( point2 ) #1
    shellDefModel.Vertices.Add( point3 ) #2
    shellDefModel.Vertices.Add( point4 ) #3
    
    
    shellDefModel.Faces.AddFace( 0, 1, 2 )
    shellDefModel.Faces.AddFace( 0, 1, 3 )
    shellDefModel.Faces.AddFace( 1, 2, 3 )
    shellDefModel.Faces.AddFace( 0, 2, 3 )
    colour = rs.CreateColor( color[0], color[1], color[2], 0 )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    
    return  shellDefModel

def ShellQuad( ele, node):
    
    eleTag = ele[1]
    eleNodeTag = ele[2]
    color = ele[5]
    thick = ele[4]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    ## CREO IL MODELLO  ##
    point1 = node.get( index1 -1 , "never")
    point2 = node.get( index2 -1 , "never")
    point3 = node.get( index3 -1 , "never")
    point4 =  node.get( index4 -1 , "never")
    
    shellModel = rg.Mesh()
    shellModel.Vertices.Add( point1 ) #0
    shellModel.Vertices.Add( point2 ) #1
    shellModel.Vertices.Add( point3 ) #2
    shellModel.Vertices.Add( point4 ) #3
    
    
    shellModel.Faces.AddFace(0, 1, 2, 3)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellModel.VertexColors.CreateMonotoneMesh( colour )

    vt = shellModel.Vertices
    shellModel.FaceNormals.ComputeFaceNormals()
    fid,MPt = shellModel.ClosestPoint(vt[0],0.01)
    normalFace = shellModel.FaceNormals[fid]
    vectormoltiplicate = rg.Vector3f.Multiply( -normalFace, thick/2 ) 
    moveShell = ghcomp.Move( shellModel, vectormoltiplicate  )[0] 
    extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
    
    return  [ shellModel, extrudeShell ] 

def ShellTriangle( ele, node ):
    
    eleTag = ele[1]
    eleNodeTag = ele[2]
    color = ele[5]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    
    
    ## CREO IL MODELLO DEFORMATO  ##
    point1 =  node.get( index1 -1 , "never")
    point2 =  node.get( index2 -1 , "never")
    point3 =  node.get( index3 -1 , "never")
    
    shellModel = rg.Mesh()
    shellModel.Vertices.Add( point1 ) #0
    shellModel.Vertices.Add( point2 ) #1
    shellModel.Vertices.Add( point3 ) #2
    
    shellModel.Faces.AddFace(0, 1, 2)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellModel.VertexColors.CreateMonotoneMesh( colour )
    
    vt = shellModel.Vertices
    shellModel.FaceNormals.ComputeFaceNormals()
    fid,MPt = shellModel.ClosestPoint(vt[0],0.01)
    normalFace = shellModel.FaceNormals[fid]
    vectormoltiplicate = rg.Vector3f.Multiply( -normalFace, thick/2 ) 
    moveShell = ghcomp.Move( shellModel, vectormoltiplicate  )[0] 
    extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
    
    return  [ shellModel, extrudeShell ]
    
def Solid( ele, node ):
    
    eleTag = ele[1]
    eleNodeTag = ele[2]
    color = ele[5]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    index5 = eleNodeTag[4]
    index6 = eleNodeTag[5]
    index7 = eleNodeTag[6]
    index8 = eleNodeTag[7]
    
    ## CREO IL MODELLO DEFORMATO  ##
    point1 =  node.get( index1 -1 , "never")
    point2 =  node.get( index2 -1 , "never")
    point3 =  node.get( index3 -1 , "never")
    point4 =  node.get( index4 -1 , "never")
    point5 =  node.get( index5 -1 , "never")
    point6 =  node.get( index6 -1 , "never")
    point7 =  node.get( index7 -1 , "never")
    point8 =  node.get( index8 -1 , "never")
    #print( type(pointDef1) ) 
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( point1 ) #0
    shellDefModel.Vertices.Add( point2 ) #1
    shellDefModel.Vertices.Add( point3 ) #2
    shellDefModel.Vertices.Add( point4 ) #3
    shellDefModel.Vertices.Add( point5 ) #4
    shellDefModel.Vertices.Add( point6 ) #5
    shellDefModel.Vertices.Add( point7 ) #6
    shellDefModel.Vertices.Add( point8 ) #7

    shellDefModel.Faces.AddFace(0, 1, 2, 3)
    shellDefModel.Faces.AddFace(4, 5, 6, 7)
    shellDefModel.Faces.AddFace(0, 1, 5, 4)
    shellDefModel.Faces.AddFace(1, 2, 6, 5)
    shellDefModel.Faces.AddFace(2, 3, 7, 6)
    shellDefModel.Faces.AddFace(3, 0, 4, 7)
    
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    return  shellDefModel
## ------------Disegno dei vincoli-------------------------------------##

def AddBoxFromCenter(plane, width, height):
    a = plane.PointAt(-width * 0.5, -width * 0.5 )
    b = plane.PointAt(-width * 0.5,  width * 0.5 )
    c = plane.PointAt( width * 0.5,  width * 0.5 )
    d = plane.PointAt( width * 0.5,  -width * 0.5 )
    rectangle1 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    box = rg.Brep.CreateOffsetBrep( rectangle1, height, True, True, 0.01 )
    return box
    
def AddForm1Center(plane, width, height):
    surf = rg.Brep()
    a = plane.PointAt(-width * 0.25, -width * 0.25 )
    b = plane.PointAt(-width * 0.25,  width * 0.25 )
    c = plane.PointAt( width * 0.25,  width * 0.25 )
    d = plane.PointAt( width * 0.25,  -width * 0.25 )
    rectangle1 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    rectangleCurve1 = rg.PolylineCurve( [ a, b, c, d, a] )
    e = plane.PointAt(-width * 0.5, -width * 0.5 )
    f = plane.PointAt(-width * 0.5,  width * 0.5 )
    g = plane.PointAt( width * 0.5,  width * 0.5 )
    h = plane.PointAt( width * 0.5,  -width * 0.5 )
    rectangle2 = rg.Brep.CreateFromCornerPoints( e, f, g, h, 0.01)
    rectangleCurve2 = rg.PolylineCurve( [ e, f, g, h, e] )
    vectorMove = rg.Vector3d( 0, 0, -height )
    trasl = rg.Transform.Translation( vectorMove )
    rectangle2.Transform( trasl )
    rectangleCurve2.Transform( trasl )
    surf.Append( rectangle1 )
    surf.Append( rectangle2 )
    pyramidTrunk = rg.Brep.CreateFromLoft( [ rectangleCurve1, rectangleCurve2 ], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False )
    for pyramid in pyramidTrunk:
        surf.Append( pyramid )
    return  surf 

def AddForm2Center(plane, width, height):
    surf = rg.Brep()
    a = plane.PointAt(-width * 0.5, -width * 0.25 )
    b = plane.PointAt(-width * 0.5,  width * 0.25 )
    c = plane.PointAt( width * 0.5,  width * 0.25 )
    d = plane.PointAt( width * 0.5,  -width * 0.25 )
    rectangle1 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    rectangleCurve1 = rg.PolylineCurve( [ a, b, c, d, a] )
    e = plane.PointAt(-width * 0.5, -width * 0.5 )
    f = plane.PointAt(-width * 0.5,  width * 0.5 )
    g = plane.PointAt( width * 0.5,  width * 0.5 )
    h = plane.PointAt( width * 0.5,  -width * 0.5 )
    rectangle2 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    rectangleCurve2 = rg.PolylineCurve( [ e, f, g, h, e] )
    vectorMove = rg.Vector3d( 0, 0, -height )
    trasl = rg.Transform.Translation( vectorMove )
    rectangle2.Transform( trasl )
    rectangleCurve2.Transform( trasl )
    surf.Append( rectangle1 )
    surf.Append( rectangle2 )
    pyramidTrunk = rg.Brep.CreateFromLoft( [ rectangleCurve1, rectangleCurve2 ], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False )
    for pyramid in pyramidTrunk:
        surf.Append( pyramid )
    return  surf 

def AddForm3Center(plane, width, height):
    surf = rg.Brep()
    a = plane.PointAt(-width * 0.25, -width * 0.5 )
    b = plane.PointAt(-width * 0.25,  width * 0.5 )
    c = plane.PointAt( width * 0.25,  width * 0.5 )
    d = plane.PointAt( width * 0.25,  -width * 0.5 )
    rectangle1 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    rectangleCurve1 = rg.PolylineCurve( [ a, b, c, d, a] )
    e = plane.PointAt(-width * 0.5, -width * 0.5 )
    f = plane.PointAt(-width * 0.5,  width * 0.5 )
    g = plane.PointAt( width * 0.5,  width * 0.5 )
    h = plane.PointAt( width * 0.5,  -width * 0.5 )
    rectangle2 = rg.Brep.CreateFromCornerPoints( a, b, c, d, 0.01)
    rectangleCurve2 = rg.PolylineCurve( [ e, f, g, h, e] )
    vectorMove = rg.Vector3d( 0, 0, -height )
    trasl = rg.Transform.Translation( vectorMove )
    rectangle2.Transform( trasl )
    rectangleCurve2.Transform( trasl )
    surf.Append( rectangle1 )
    surf.Append( rectangle2 )
    pyramidTrunk = rg.Brep.CreateFromLoft( [ rectangleCurve1, rectangleCurve2 ], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Straight, False )
    for pyramid in pyramidTrunk:
        surf.Append( pyramid )
    return  surf