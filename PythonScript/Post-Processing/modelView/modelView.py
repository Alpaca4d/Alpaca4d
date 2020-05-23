import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import rhinoscriptsyntax as rs
#import Grasshopper
#import System as sy #DV
import sys

'''
ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
'''
folderName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(folderName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 

#---------------------------------------------------------------------------------------#

nodeWrapper = openSeesModel[0]
GeomTransf = openSeesModel[1]
openSeesBeam = openSeesModel[2]
openSeesSupport = openSeesModel[3]
openSeesNodeLoad = openSeesModel[4]
openSeesShell = openSeesModel[8]
openSeesSolid = openSeesModel[10]

pointWrapper = []
for item in nodeWrapper:
    point = rg.Point3d(item[1],item[2],item[3])
    pointWrapper.append( [item[0], point ] )
## Dict. for point ##
pointWrapperDict = dict( pointWrapper )
####

if nodeTag == True:
    posTag = [row[1] for row in pointWrapper ]
    nodeTag = [row[0] for row in pointWrapper ]
    tagNode = th.list_to_tree( [ posTag, nodeTag ]  )

## Funzione cerchio ##
def AddCircleFromCenter( plane, radius):
    t = dg.linspace( 0 , 2*mt.pi, 15 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle

def AddIFromCenter(plane, Bsup, tsup, Binf, tinf, H, ta, yg):
    p1 = plane.PointAt(ta/2, -(yg - tinf) )
    p2 = plane.PointAt( Binf/2,  -(yg - tinf) )
    p3 = plane.PointAt( Binf/2,  -yg )
    p4 = plane.PointAt( -Binf/2,  -yg )
    p5 = plane.PointAt( -Binf/2, -(yg - tinf) ) 
    p6 = plane.PointAt( -ta/2,  -(yg - tinf) )
    p7 = plane.PointAt( -ta/2,  (H - yg - tsup))
    p8 = plane.PointAt( -Bsup/2,  (H - yg - tsup) )
    p9 = plane.PointAt( -Bsup/2,  (H - yg ) )
    p10 = plane.PointAt( Bsup/2,  (H - yg ) )
    p11 = plane.PointAt( Bsup/2,  (H - yg - tsup) )
    p12 = plane.PointAt( ta/2,  (H - yg - tsup) )
    wirframe  = [ p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 ] 
    return wirframe

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
    vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
    trasl = rg.Transform.Translation( vectormoltiplicate )
    moveShell = rg.Mesh.DuplicateMesh(shellModel)
    moveShell.Transform( trasl )
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
    vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 ) 
    trasl = rg.Transform.Translation( vectormoltiplicate )
    moveShell = rg.Mesh.DuplicateMesh(shellModel)
    moveShell.Transform( trasl )
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
## node e nodeDisp son dictionary ##
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
            sectionForm.append( section )
        elif dimSection[0] == 'circular' :
            radius1  = dimSection[1]/2
            radius2  = dimSection[1]/2 - dimSection[2]
            section1 = AddCircleFromCenter( sectionPlane, radius1 )
            section2 = AddCircleFromCenter( sectionPlane, radius2 )
            sectionForm.append( [ section1, section2 ] )
        elif dimSection[0] == 'doubleT' :
            Bsup = dimSection[1]
            tsup = dimSection[2]
            Binf = dimSection[3]
            tinf = dimSection[4]
            H =  dimSection[5]
            ta =  dimSection[6]
            yg =  dimSection[7]
            section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
            sectionForm.append( section )
        elif dimSection[0] == 'Generic' :
            radius  = dimSection[1]
            section = AddCircleFromCenter( sectionPlane, radius )
            sectionForm.append( section )
            
        
        
    meshExtr = meshLoft3( sectionForm,  color )
    colour = rs.CreateColor( color[0], color[1], color[2] )
    return [ line, meshExtr, colour ]

## Mesh from close section eith gradient color ##
def meshLoft3( point, color ):
    meshElement = rg.Mesh()
    if len(point[0]) < 11 : # perchè in questo caso piùsezioni
        nLength =  len(point[0]) 
        for item in range( nLength ):
            meshEle = rg.Mesh()
            pointSection1 = [row[item] for row in point ]
            for i in range(0,len(pointSection1)):
                for j in range(0, len(pointSection1[0])):
                    vertix = pointSection1[i][j]
                    meshEle.Vertices.Add( vertix ) 
                    #meshEle.VertexColors.Add( color[0],color[1],color[2] );
            k = len(pointSection1[0])
            for i in range(0,len(pointSection1)-1):
                for j in range(0, len(pointSection1[0])):
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
            meshElement.Append( meshEle )
    else :
        meshEle = rg.Mesh()
        pointSection1 = point
        for i in range(0,len(pointSection1)):
            for j in range(0, len(pointSection1[0])):
                vertix = pointSection1[i][j]
                print( type(vertix) )
                meshEle.Vertices.Add( vertix ) 
                #meshEle.VertexColors.Add( color[0],color[1],color[2] );
        k = len(pointSection1[0])
        for i in range(0,len(pointSection1)-1):
            for j in range(0, len(pointSection1[0])):
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
        meshElement = meshEle
    
    return meshElement


model = []
extrudedModel = []

line = []
colorLine = []

eleTag = []
posEleTag = []
for ele in openSeesBeam :
    eleTag.append(ele[1])
    beamModel = Beam( ele, pointWrapperDict )
    line.append( beamModel[0] )
    posEleTag.append( beamModel[0].PointAtNormalizedLength(0.5) )
    model.append( beamModel[0] )
    colorLine.append( beamModel[2] )
    extrudedModel.append( beamModel[1] )


for ele in openSeesShell :
    nNode = len( ele[2] )
    eleTag.append( ele[1] )
    if nNode == 4 :
        shellModel = ShellQuad( ele, pointWrapperDict )
        model.append( shellModel[0] )
        extrudedModel.append( shellModel[1] )
        calcPropSection = rg.AreaMassProperties.Compute( shellModel[0], False, True, False, False )
        centroid = calcPropSection.Centroid
        posEleTag.append( centroid )
    elif nNode == 3:
        #print( nNode )
        shellModel = ShellTriangle( ele, pointWrapperDict )
        model.append( shellModel[0] )
        extrudedModel.append( shellModel[1] )
        calcPropSection = rg.AreaMassProperties.Compute( shellModel[0], False, True, False, False )
        centroid = calcPropSection.Centroid
        posEleTag.append( centroid )


for ele in openSeesSolid :
    nNode = len( ele[2] )
    eleTag.append( ele[1] )
    eleType = ele[0] 
    if nNode == 8:
        solidModel = Solid( ele, pointWrapperDict )
        model.append( solidModel )
        extrudedModel.append( solidModel )
        calcPropSection = rg.AreaMassProperties.Compute( solidModel, False, True, False, False )
        centroid = calcPropSection.Centroid
        posEleTag.append( centroid )
    elif  eleType == 'FourNodeTetrahedron' :
        #print(ele)
        solidModel = TetraSolid( ele, pointWrapperDict )
        model.append( solidModel )
        extrudedModel.append( solidModel )
        calcPropSection = rg.AreaMassProperties.Compute( solidModel, False, True, False, False )
        centroid = calcPropSection.Centroid
        posEleTag.append( centroid )


if elementTag == True:
    tagEle = th.list_to_tree( [ posEleTag, eleTag ]  )

if modelExstrud == True:
    modelView = extrudedModel
else:
    modelView = model
    lineModel = th.list_to_tree( [ line, colorLine ]  )

#------------------ Local Axis ----------------------#
midPoint = []
v3Display = []
v2Display = []
v1Display = []
eleTag = []
if LocalAxes == True:
    for ele in openSeesBeam :
        indexStart = ele[2][0]
        indexEnd = ele[2][1]
        propSection = ele[13]
        ## creo la linea ##
        line = rg.LineCurve( pointWrapperDict.get( indexStart  , "never"), pointWrapperDict.get( indexEnd  , "never"))
        MidPoint =  line.PointAtNormalizedLength(0.5)
        ## creo i versori  ##
        axis3 = pointWrapperDict.get( indexEnd  , "never") - pointWrapperDict.get( indexStart  , "never")
        axis3.Unitize()
        axis1 =  rg.Vector3d( propSection[0], propSection[1], propSection[2]  )
        axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
        midPoint.append( MidPoint )
        v3Display.append( axis3*0.5 )
        v2Display.append( axis2*0.5  )
        v1Display.append( axis1*0.5  )
localAxis = th.list_to_tree( [ midPoint, v1Display, v2Display, v3Display ] )

#--------------------------------------------------------------#


forceMax = []
for force in openSeesNodeLoad :
    forceVector =  rg.Vector3d( force[1][0], force[1][1] , force[1][2]  )
    fmax = max( forceVector.X, forceVector.Y, forceVector.Z )
    fmin = min( forceVector.X, forceVector.Y, forceVector.Z )
    forceMax.append( max( [ fmax, mt.fabs(fmin) ] ) )
forceMax = max( forceMax )

#scale = forceMax*0.1/coordMax 
scale = 1/forceMax 

forceDisplay = []
ancorPoint = []
if Load == True:
    for force in openSeesNodeLoad :
        index = force[0]
        pos = pointWrapperDict.get( index  , "never") 
        forceVector =  rg.Vector3d( force[1][0], force[1][1] , force[1][2]  )
        ancorPoint.append( pos )
        forceDisplay.append(  forceVector*scale  )
forceDisplay = th.list_to_tree( [ ancorPoint, forceDisplay ] )



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

a = []
if Support == True:
    for support in openSeesSupport :
        index = support[0]
        pos = pointWrapperDict.get( index  , "never")
        center_point = rg.Point3d( pos )
        
        if support[1] == 1 and support[2] == 0 and support[3] == 1 and support[4] == 1 and support[5] == 1 and support[6] == 1 : # carrello lungo y
            supp = rg.Brep()
            plane = rg.Plane.WorldYZ
            radius = 0.15
            length = radius*3.50
            vector = rg.Vector3d( -length/2, 0 , -2.5*radius ) 
            vectorTrasl = rg.Point3d.Add( center_point, vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
            plane.Transform( trasl )
            circle = rg.Circle(plane, radius/2)
            brepCylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )
            cylinder1 = rg.Brep.DuplicateBrep(brepCylinder)
            traslc1 = rg.Transform.Translation( 0, -length/4, 0 )
            cylinder1.Transform( traslc1 )
            cylinder2 = rg.Brep.DuplicateBrep(brepCylinder)
            supp.Append( cylinder1 )
            traslc2 = rg.Transform.Translation( 0, length/4, 0 )
            cylinder2.Transform( traslc2 )
            supp.Append( cylinder2 )
            plane2 = rg.Plane.WorldXY
            vector2 = rg.Vector3d( 0, 0 , 0 ) 
            vectorTrasl2 = rg.Point3d.Add( center_point, vector2 )
            trasl2 = rg.Transform.Translation( vectorTrasl2.X, vectorTrasl2.Y, vectorTrasl2.Z ) 
            plane2.Transform( trasl2 )
            supp.Append( AddForm2Center(plane2, length, radius*2) )
            a.append( supp )
        if support[1] == 0 and support[2] == 1 and support[3] == 1 and support[4] == 1 and support[5] == 1 and support[6] == 1 : # carrello lungo x
            supp = rg.Brep()
            plane = rg.Plane.WorldZX
            radius = 0.15
            length = radius*3.50
            vector = rg.Vector3d( 0, -length/2 , -2.5*radius ) 
            vectorTrasl = rg.Point3d.Add( center_point, vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
            plane.Transform( trasl )
            circle = rg.Circle(plane, radius/2)
            brepCylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True ) 
            cylinder1 = rg.Brep.DuplicateBrep(brepCylinder)
            traslc1 = rg.Transform.Translation( -length/4, 0, 0 )
            cylinder1.Transform( traslc1 )
            cylinder2 = rg.Brep.DuplicateBrep(brepCylinder)
            supp.Append( cylinder1 )
            traslc2 = rg.Transform.Translation( length/4, 0, 0 )
            cylinder2.Transform( traslc2 )
            supp.Append( cylinder2 )
            plane2 = rg.Plane.WorldXY
            vector2 = rg.Vector3d( 0, 0 , 0 )
            vectorTrasl2 = rg.Point3d.Add( center_point, vector2 )
            trasl2 = rg.Transform.Translation( vectorTrasl2.X, vectorTrasl2.Y, vectorTrasl2.Z ) 
            plane2.Transform( trasl2 )
            supp.Append( AddForm3Center(plane2, length, radius*2) )
            a.append( supp )
        if support[1] == 1 and support[2] == 1 and support[3] == 1 and support[4] == 0 and support[5] == 1  : # cerniera lungo x
            supp = rg.Brep()
            plane = rg.Plane.WorldZX
            radius = 0.15
            length = radius*3.50
            vector = rg.Vector3d( 0, -length/2 , -radius ) 
            vectorTrasl = rg.Point3d.Add( center_point, vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
            plane.Transform( trasl )
            circle = rg.Circle(plane, radius)
            supp.Append( rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True ) )
            plane2 = rg.Plane.WorldXY
            vector2 = rg.Vector3d( 0, 0 , -1.70*radius )
            vectorTrasl2 = rg.Point3d.Add( center_point, vector2 )
            trasl2 = rg.Transform.Translation( vectorTrasl2.X, vectorTrasl2.Y, vectorTrasl2.Z ) 
            plane2.Transform( trasl2 )
            supp.Append( AddForm3Center(plane2, length, radius*2) )
            a.append( supp )
        if support[1] == 1 and support[2] == 1 and support[3] == 1 and support[4] == 1 and support[5] == 0  : # cerniera lungo y
            supp = rg.Brep()
            plane = rg.Plane.WorldYZ
            radius = 0.15
            length = radius*3.50
            vector = rg.Vector3d( -length/2, 0 , -radius )
            vectorTrasl = rg.Point3d.Add( center_point, vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
            plane.Transform( trasl )
            circle = rg.Circle(plane, radius)
            supp.Append( rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True ) )
            plane2 = rg.Plane.WorldXY
            vector2 = rg.Vector3d( 0, 0 , -1.70*radius )
            vectorTrasl2 = rg.Point3d.Add( center_point, vector2 )
            trasl2 = rg.Transform.Translation( vectorTrasl2.X, vectorTrasl2.Y, vectorTrasl2.Z ) 
            plane2.Transform( trasl2 )
            supp.Append( AddForm2Center(plane2, length, radius*2) )
            a.append( supp )
        if support[1] == 1 and support[2] == 1 and support[3] == 1 and support[4] == 0 and support[5] == 0   : # cerniera sferica
            radius = 0.15
            length = radius*3.50
            vector = rg.Vector3d( 0, 0 , -radius ) 
            center =  rg.Point3d.Add( center_point, vector )
            supp = rg.Brep()
            # sfera
            supp.Append( rg.Brep.CreateFromSphere(rg.Sphere( center, radius)))
            plane = rg.Plane.WorldXY
            vectorTrasl = rg.Point3d.Add( center_point, 1.70*vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z  )
            plane.Transform( trasl )
            # tronco di piramide
            supp.Append( AddForm1Center(plane, length, radius*2) )
            a.append( supp )
        if support[1] == 1 and support[2] == 1 and support[3] == 1 and support[4] == 1 and support[5] == 1  and support[6] == 1 : # incastro
            supp = rg.Brep()
            plane = rg.Plane.WorldXY
            length = 0.5
            h = length/3
            vector = rg.Vector3d( 0, 0 , 0 )
            vectorTrasl = rg.Point3d.Add( center_point, vector )
            trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z  )
            plane2 = rg.Plane.Clone( plane )
            plane2.Transform( trasl )
            supp = AddBoxFromCenter(plane2, length, h) 
            a.append( supp )
support = th.list_to_tree( a )


 
