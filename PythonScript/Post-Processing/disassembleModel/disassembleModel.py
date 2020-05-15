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
Points = [row[1] for row in pointWrapper ]

## Funzione cerchio ##
def AddCircleFromCenter( plane, radius):
    t = dg.linspace( 0 , 2*mt.pi, 20 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle

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
            
        if dimSection[0] == 'circular' :
            radius  = dimSection[2]
            section = AddCircleFromCenter( sectionPlane, radius )
            
        sectionForm.append( section )
        
        
    meshExtr = meshLoft3( sectionForm,  color )
    colour = rs.CreateColor( color[0], color[1], color[2] )
    return [ line, meshExtr, colour ]

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


model = []
extrudedModel = []

for ele in openSeesBeam :
    eleTag = ele[1]
    beamModel = Beam( ele, pointWrapperDict )
    model.append([ eleTag, beamModel[0] ])
    extrudedModel.append([ eleTag, beamModel[1] ])

for ele in openSeesShell :
    nNode = len( ele[2] )
    eleTag =  ele[1] 
    if nNode == 4 :
        shellModel = ShellQuad( ele, pointWrapperDict )
        model.append([ eleTag,shellModel[0] ])
        extrudedModel.append([ eleTag,shellModel[1] ])
    elif nNode == 3:
        shellModel = ShellTriangle( ele, pointWrapperDict )
        model.append([ eleTag,shellModel[0] ])
        extrudedModel.append([ eleTag,shellModel[1] ])

for ele in openSeesSolid :
    nNode = len( ele[2] )
    eleTag =  ele[1]
    eleType = ele[0] 
    if nNode == 8:
        solidModel = Solid( ele, pointWrapperDict )
        model.append([ eleTag, solidModel ])
        extrudedModel.append([ eleTag, solidModel ])
    elif  eleType == 'FourNodeTetrahedron' :
        #print(ele)
        solidModel = TetraSolid( ele, pointWrapperDict )
        model.append([ eleTag, solidModel ])
        extrudedModel.append([ eleTag, solidModel ])

modelDict = dict( model )
modelExstrudedDict = dict( extrudedModel )
ModelView = []
ModelViewExtruded = []
for i in range(0,len(modelDict)):
    ModelView.append( modelDict.get( i  , "never" ))
    ModelViewExtruded.append( modelExstrudedDict.get( i , "never" ))

#--------------------------------------------------------------#



forceDisplay = []
for force in openSeesNodeLoad :
    forceVector =  rg.Vector3d( force[1][0], force[1][1] , force[1][2]  )
    forceDisplay.append(  forceVector  )
Load = forceDisplay

Support = []
for support in openSeesSupport :
    index = support[0]
    pos = pointWrapperDict.get( index  , "never")
    Support.append( pos )