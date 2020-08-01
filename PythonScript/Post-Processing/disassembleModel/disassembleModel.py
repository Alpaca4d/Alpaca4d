"""Generate Model view 
    Inputs:
        AlpacaModel: Output of Assemble Model.
    Output:
       ModelView : analitic element ( beam, shell, brick ... ).
       ModelViewExtruded : extruded model .
       Points : points of model .
       Support : info support .
       Load : info Load .
       Material : info Material.
       Section : info Section.
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
import rhinoscriptsyntax as rs
import sys


#---------------------------------------------------------------------------------------#
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
    t = linspace( 0 , 1.80*mt.pi, 20 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle

def AddIFromCenter(plane, Bsup, tsup, Binf, tinf, H, ta, yg):
    #-------------------1---------2 #
    '''
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
    '''
    p1 = plane.PointAt( -(yg - tinf), ta/2 )
    p2 = plane.PointAt( -(yg - tinf), Binf/2 )
    p3 = plane.PointAt( -yg, Binf/2 )
    p4 = plane.PointAt( -yg, -Binf/2 )
    p5 = plane.PointAt( -(yg - tinf), -Binf/2 ) 
    p6 = plane.PointAt( -(yg - tinf), -ta/2 )
    p7 = plane.PointAt( (H - yg - tsup), -ta/2)
    p8 = plane.PointAt( (H - yg - tsup), -Bsup/2 )
    p9 = plane.PointAt( (H - yg ), -Bsup/2 )
    p10 = plane.PointAt( (H - yg ), Bsup/2 )
    p11 = plane.PointAt( (H - yg - tsup), Bsup/2 )
    p12 = plane.PointAt( (H - yg - tsup), ta/2 )

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
    thick = ele[4]
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
    axis1 =  rg.Vector3d( ele[13][0][0], ele[13][0][1], ele[13][0][2]  )
    axis2 =  rg.Vector3d( ele[13][1][0], ele[13][1][1], ele[13][1][2]  )
    axis3 =  rg.Vector3d( ele[13][2][0], ele[13][2][1], ele[13][2][2]  )
    versor = [ axis1, axis2, axis3 ] 
    
    planeStart = rg.Plane(pointStart, axis1, axis2)
    planeEnd = rg.Plane(pointEnd, axis1, axis2)
    plane = [ planeStart, planeEnd ]
    
    sectionForm = []
    sectionPolyline = []
    for sectionPlane in plane:
        
        if dimSection[0] == 'rectangular' :
            width, height = dimSection[1], dimSection[2]
            section = AddRectangleFromCenter( sectionPlane, width, height )
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
        elif dimSection[0] == 'rectangularHollow' :
            width, height, thickness = dimSection[1], dimSection[2], dimSection[3]
            section1 = AddRectangleFromCenter( sectionPlane, width, height )
            section2 = AddRectangleFromCenter( sectionPlane, width - (2*thickness), height - (2*thickness) )
            sectionForm.append( [ section1, section2 ] )
        elif dimSection[0] == 'Generic' :
            radius  = dimSection[1]
            section = AddCircleFromCenter( sectionPlane, radius )
            sectionForm.append( section )
        #print(sectionForm)

    colour = rs.CreateColor( color[0], color[1], color[2] )

    if dimSection[0] == 'circular' :
        sectionForm1 = [row[0] for row in sectionForm ]
        sectionForm2 = [row[1] for row in sectionForm ]
        meshExtr = meshLoft3( sectionForm1,  color )
        meshExtr.Append( meshLoft3( sectionForm2,  color ) )
        sectionStartEnd = [ [sectionForm1[0], sectionForm2[0]], [sectionForm1[-1], sectionForm2[-1]]  ]
        for iSection in sectionStartEnd :
            iMesh = rg.Mesh()
            for iPoint, jPoint in zip(iSection[0],iSection[1])  :
                iMesh.Vertices.Add( iPoint )
                iMesh.Vertices.Add( jPoint )
            for i in range(0,len(iSection[0]) - 1): # sistemare
                index1 = i*2 # 0
                index2 = index1 + 1 #1
                index3 = index1 + 3 #2
                index4 = index1 + 2 #3
                iMesh.Faces.AddFace(index1, index2, index3, index4)
            iMesh.Faces.AddFace(index4, index3, 1, 0)
            iMesh.VertexColors.CreateMonotoneMesh( colour )
            meshExtr.Append( iMesh )
            #meshExtr.IsClosed()
    elif  dimSection[0] == 'rectangular' : 
        meshExtr = meshLoft3( sectionForm,  color )
        sectionStartEnd = [ sectionForm[0], sectionForm[-1] ]
        for iSection in sectionStartEnd :
            iMesh = rg.Mesh()
            for iPoint in iSection :
                 iMesh.Vertices.Add( iPoint )
            iMesh.Faces.AddFace(0, 1, 2, 3)
            iMesh.VertexColors.CreateMonotoneMesh( colour )
            meshExtr.Append( iMesh )
    elif  dimSection[0] == 'doubleT' : 
        meshExtr = meshLoft3( sectionForm,  color )
        sectionStartEnd = [ sectionForm[0], sectionForm[-1] ]
        for iSection in sectionStartEnd :
            iMesh = rg.Mesh()
            for iPoint in iSection :
                 iMesh.Vertices.Add( iPoint )
            iMesh.Faces.AddFace( 0, 1, 2 )
            iMesh.Faces.AddFace(2, 3, 5, 0 )
            iMesh.Faces.AddFace( 3, 4, 5 )
            iMesh.Faces.AddFace( 5, 6, 11, 0 )
            iMesh.Faces.AddFace( 6, 7, 8 )
            iMesh.Faces.AddFace( 8, 9, 11, 6 )
            iMesh.Faces.AddFace( 9, 10, 11 )
            #iMesh.Faces.AddFace(3, 2, 1, 4)
            #iMesh.Faces.AddFace( 5, 6, 11, 0 )
            #iMesh.Faces.AddFace(7, 8, 9, 10)
            iMesh.VertexColors.CreateMonotoneMesh( colour )
            meshExtr.Append( iMesh ) 
    elif  dimSection[0] == 'rectangularHollow' : 
        sectionForm1 = [row[0] for row in sectionForm ]
        sectionForm2 = [row[1] for row in sectionForm ]
        meshExtr = meshLoft3( sectionForm1,  color )
        meshExtr.Append( meshLoft3( sectionForm2,  color ) )
        sectionStartEnd = [ [sectionForm1[0], sectionForm2[0]], [sectionForm1[-1], sectionForm2[-1]]  ]
        for iSection in sectionStartEnd :
            iMesh = rg.Mesh()
            for iPoint, jPoint in zip(iSection[0],iSection[1])  :
                iMesh.Vertices.Add( iPoint )
                iMesh.Vertices.Add( jPoint )
            iMesh.Faces.AddFace(0, 1, 3, 2)
            iMesh.Faces.AddFace(2, 3, 5, 4)
            iMesh.Faces.AddFace(4, 5, 7, 6)
            iMesh.Faces.AddFace(6, 7, 1, 0)
            iMesh.VertexColors.CreateMonotoneMesh( colour )
            meshExtr.Append( iMesh )
            #meshExtr.IsClosed()

    elif dimSection[0] == 'Generic' :
        meshExtr = meshLoft3( sectionForm,  color )

    return [ line, meshExtr, colour ]

## Mesh from close section eith gradient color ##
def meshLoft3( point, color ):
    #print( point )
    meshEle = rg.Mesh()
    pointSection1 = point
    for i in range(0,len(pointSection1)):
        for j in range(0, len(pointSection1[0])):
            vertix = pointSection1[i][j]
            #print( type(vertix) )
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
    #meshdElement.IsClosed(True)
    
    return meshElement
# ------------------------------------------------------------------------------- #
def diassembleModel(AlpacaModel ):

    nodeWrapper = AlpacaModel[0]
    GeomTransf = AlpacaModel[1]
    openSeesBeam = AlpacaModel[2]
    openSeesSupport = AlpacaModel[3]
    openSeesNodeLoad = AlpacaModel[4]
    openSeesMatTag = AlpacaModel[7]
    openSeesShell = AlpacaModel[8]
    openSeesSecTag = AlpacaModel[9]
    openSeesSolid = AlpacaModel[10]

    pointWrapper = []
    for item in nodeWrapper:
        point = rg.Point3d(item[1],item[2],item[3])
        pointWrapper.append( [item[0], point ] )
    ## Dict. for point ##
    pointWrapperDict = dict( pointWrapper )
    ####
    Points = [row[1] for row in pointWrapper ]

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
    for item in openSeesNodeLoad:
        loadWrapper = "{3}; Pos=[{4}]; F={1}; M={2}".format(item[0],item[1][:3],item[1][3:], item[2], pointWrapperDict.get(item[0]))
        forceDisplay.append(loadWrapper)
    Load = forceDisplay



    Support = []

    for support in openSeesSupport :
        index = support[0]
        pos = pointWrapperDict.get(index)
        supportType = support[1:]
        supportTypeTemp = []
        for number in supportType:
            if number == 1:
                dof = True
            else:
                dof = False
            supportTypeTemp.append(dof)
        supportWrapper = "Support; Pos=[{0}]; DOF={1}".format(pos,supportTypeTemp)
        Support.append( supportWrapper )


    Material = []

    for item in openSeesMatTag:
        Grade= item[0].split("_")[0]
        dimensionType = item[0].split("_")[1]
        typeMat = item[0].split("_")[2]
        E = item[1][1][0]
        G = item[1][1][1]
        v = item[1][1][2]
        gamma = item[1][1][3]
        fy = item[1][1][4]
        Material.append( "grade={}; type={}; E={}; G={}; v={}; gamma={}; fy={}".format(Grade,typeMat,E,G,v,gamma,fy))


    Section = []

    for item in openSeesSecTag:
        name = item[0].split("_")[0]
        typeSec = item[0].split("_")[1]
        Section.append("name={}; type={}".format(name, typeSec))

    return ModelView, ModelViewExtruded, Points, Support, Load, Material, Section

checkData = True

if not AlpacaModel:
    checkData = False
    msg = "input 'AlpacaModel' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    ModelView, ModelViewExtruded, Points, Support, Load, Material, Section = diassembleModel( AlpacaModel )