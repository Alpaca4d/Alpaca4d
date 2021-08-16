import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
import Rhino.Display as rd
from scriptcontext import doc


ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import function.DomeFunc as dg 

#---------------------------------------------------------------------------------------#

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
nodeValue = []
displacementValue = []
#ShellOut = openSeesOutputWrapper[4]

pointWrapper = []
dispWrapper = []

for index,item in enumerate(diplacementWrapper):
    nodeValue.append( item[0] )
    displacementValue.append( item[1] )
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    if len(item[1]) == 3:
        dispWrapper.append( [index, rg.Point3d( item[1][0], item[1][1], item[1][2] ) ] )
    elif len(item[1]) == 6:
        dispWrapper.append( [index, [rg.Point3d(item[1][0],item[1][1],item[1][2] ), rg.Point3d(item[1][3],item[1][4],item[1][5]) ] ] )

## Dict. for point ##
pointWrapperDict = dict( pointWrapper )
pointDispWrapperDict = dict( dispWrapper )
####

## FOR scala automatica ##
## nodeValue è la lista delle cordinate
rowX = [row[0] for row in nodeValue ]
rowY = [row[1] for row in nodeValue ]
rowZ = [row[2] for row in nodeValue ]

scaleMax = max( max(rowX), max(rowY), max(rowZ) )
scaleMin = min( min(rowX), min(rowY), min(rowZ) )
coordMax = max( mt.fabs(scaleMin),mt.fabs(scaleMax)) - mt.fabs(scaleMin)

## displacementValue è la lista degli spostamenti

rowDefX = [row[0] for row in displacementValue ]
rowDefY = [row[1] for row in displacementValue ]
rowDefZ = [row[2] for row in displacementValue ]

defMax = max( max(rowDefX), max(rowDefY), max(rowDefZ) )
defMin = min( min(rowDefX), min(rowDefY), min(rowDefZ) )
DefMax = max( mt.fabs(defMax),mt.fabs(defMin))

if scale == None:
    scaleDef = dg.scaleAutomatic( coordMax , DefMax )

else :
    scaleDef = scale

## Funzione cerchio ##
def AddCircleFromCenter( plane, radius):
    t = dg.linspace( 0 , 2*mt.pi, 12 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle
    
def defShellQuad( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][2]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")[0]
    rotate1 = nodeDisp.get( index1 -1 , "never")[1]
    
    trasl2 = nodeDisp.get( index2 -1 , "never")[0]
    rotate2 = nodeDisp.get( index2 -1 , "never")[1]
    
    trasl3 = nodeDisp.get( index3 -1 , "never")[0]
    rotate3 = nodeDisp.get( index3 -1 , "never")[1]
    
    trasl4 = nodeDisp.get( index4 -1 , "never")[0]
    rotate4 = nodeDisp.get( index4 -1 , "never")[1]
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = ghcomp.Move( node.get( index1 -1 , "never"), scaleDef*trasl1 )[0]
    pointDef2 = ghcomp.Move( node.get( index2 -1 , "never"), scaleDef*trasl2 )[0]
    pointDef3 = ghcomp.Move( node.get( index3 -1 , "never"), scaleDef*trasl3 )[0]
    pointDef4 = ghcomp.Move( node.get( index4 -1 , "never"), scaleDef*trasl4 )[0]
    
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    
    
    shellDefModel.Faces.AddFace(0, 1, 2, 3)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4], [rotate1, rotate2, rotate3, rotate4]]

def defShellTriangle( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")[0]
    rotate1 = nodeDisp.get( index1 -1 , "never")[1]
    
    trasl2 = nodeDisp.get( index2 -1 , "never")[0]
    rotate2 = nodeDisp.get( index2 -1 , "never")[1]
    
    trasl3 = nodeDisp.get( index3 -1 , "never")[0]
    rotate3 = nodeDisp.get( index3 -1 , "never")[1]
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = ghcomp.Move( node.get( index1 -1 , "never"), scaleDef*trasl1 )[0]
    pointDef2 = ghcomp.Move( node.get( index2 -1 , "never"), scaleDef*trasl2 )[0]
    pointDef3 = ghcomp.Move( node.get( index3 -1 , "never"), scaleDef*trasl3 )[0]
    
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    
    shellDefModel.Faces.AddFace(0, 1, 2)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    return  [shellDefModel,[trasl1, trasl2, trasl3], [rotate1, rotate2, rotate3]]
    
def defSolid( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    index5 = eleNodeTag[4]
    index6 = eleNodeTag[5]
    index7 = eleNodeTag[6]
    index8 = eleNodeTag[7]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    trasl5 = nodeDisp.get( index5 -1 , "never")
    trasl6 = nodeDisp.get( index6 -1 , "never")
    trasl7 = nodeDisp.get( index7 -1 , "never")
    trasl8 = nodeDisp.get( index8 -1 , "never")
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = ghcomp.Move( node.get( index1 -1 , "never"), scaleDef*trasl1 )[0]
    pointDef2 = ghcomp.Move( node.get( index2 -1 , "never"), scaleDef*trasl2 )[0]
    pointDef3 = ghcomp.Move( node.get( index3 -1 , "never"), scaleDef*trasl3 )[0]
    pointDef4 = ghcomp.Move( node.get( index4 -1 , "never"), scaleDef*trasl4 )[0]
    pointDef5 = ghcomp.Move( node.get( index5 -1 , "never"), scaleDef*trasl5 )[0]
    pointDef6 = ghcomp.Move( node.get( index6 -1 , "never"), scaleDef*trasl6 )[0]
    pointDef7 = ghcomp.Move( node.get( index7 -1 , "never"), scaleDef*trasl7 )[0]
    pointDef8 = ghcomp.Move( node.get( index8 -1 , "never"), scaleDef*trasl8 )[0]
    #print( type(pointDef1) ) 
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    shellDefModel.Vertices.Add( pointDef5 ) #4
    shellDefModel.Vertices.Add( pointDef6 ) #5
    shellDefModel.Vertices.Add( pointDef7 ) #6
    shellDefModel.Vertices.Add( pointDef8 ) #7

    shellDefModel.Faces.AddFace(0, 1, 2, 3)
    shellDefModel.Faces.AddFace(4, 5, 6, 7)
    shellDefModel.Faces.AddFace(0, 1, 5, 4)
    shellDefModel.Faces.AddFace(1, 2, 6, 5)
    shellDefModel.Faces.AddFace(2, 3, 7, 6)
    shellDefModel.Faces.AddFace(3, 0, 4, 7)
    
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    return  [shellDefModel,[trasl1, trasl2, trasl3,trasl4, trasl5, trasl6, trasl7, trasl8 ]]

def defTetraSolid( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = ghcomp.Move( node.get( index1 -1 , "never"), scaleDef*trasl1 )[0]
    pointDef2 = ghcomp.Move( node.get( index2 -1 , "never"), scaleDef*trasl2 )[0]
    pointDef3 = ghcomp.Move( node.get( index3 -1 , "never"), scaleDef*trasl3 )[0]
    pointDef4 = ghcomp.Move( node.get( index4 -1 , "never"), scaleDef*trasl4 )[0]
    
    #print( type(pointDef1) )
    
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    
    
    shellDefModel.Faces.AddFace( 0, 1, 2 )
    shellDefModel.Faces.AddFace( 0, 1, 3 )
    shellDefModel.Faces.AddFace( 1, 2, 3 )
    shellDefModel.Faces.AddFace( 0, 2, 3 )
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    
    return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4]]
## node e nodeDisp son dictionary ##
def defValueTimoshenkoBeam( ele, node, nodeDisp ):
#------------------- WORLD PLANE ----------------------#
    worldPlane = rg.Plane.WorldXY
# plane XY 
#------------------------------------------------------#

#------------ Propriety TimoshenkoBeam  ----------------#

    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    
    E = propSection[1]
    G = propSection[2]
    A = propSection[3]
    Avz = propSection[4]
    Avy = propSection[5]
    Jxx = propSection[6]
    Iy = propSection[7]
    Iz = propSection[8]
    
#------ traslation and rotation index start & end ------- #
    traslStart = nodeDisp.get( indexStart -1 , "never")[0]
    rotateStart = nodeDisp.get( indexStart -1 , "never")[1]
    
    traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
    rotateEnd = nodeDisp.get( indexEnd -1 , "never")[1]
    
## ----------------CHANGE BASIS global to local ------------##
#---------------------------------------------------------#
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    line = rg.LineCurve( pointStart, pointEnd )

# ---------------------------versor ---------------------------#

    axis3 = pointEnd - pointStart
    axis3.Unitize()
    axis1 =  rg.Vector3d( propSection[9][0], propSection[9][1], propSection[9][2]  )
    axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
    versor = [ axis1, axis2, axis3 ] 
    
#------------- WORLD PLANE on point start of line ---------------#
    WorldPlane = ghcomp.Move(worldPlane, pointStart)[0]
#----------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2)
    ## NODE START ###
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    
    localTraslStart = rg.Point3d( traslStart )
    #localTraslStart = traslStart
    localTraslStart.Transform(xform)
    
    uI1 = localTraslStart[0] # spostamento in direzione dell'asse rosso 
    uI2 = localTraslStart[1] # spostamento in direzione dell'asse verde
    uI3 = localTraslStart[2] # spostamento linea d'asse
    #print(uI1,uI2,uI3)
    
    localRotStart = rg.Point3d(rotateStart)
    #localRotStart = rotateStart
    localRotStart.Transform(xform)
    
    rI1 = localRotStart[0] # spostamento in direzione dell'asse rosso 
    rI2 = localRotStart[1] # spostamento in direzione dell'asse verde
    rI3 = localRotStart[2] # spostamento linea d'asse
    #print(rI1,rI2,rI3)
    
    ## NODE END ##
    
    localTraslEnd = rg.Point3d(traslEnd)
    #localTraslEnd = traslEnd
    localTraslEnd.Transform(xform)
    
    uJ1 = localTraslEnd[0] # spostamento in direzione dell'asse rosso 
    uJ2 = localTraslEnd[1] # spostamento in direzione dell'asse verde
    uJ3 = localTraslEnd[2] # spostamento linea d'asse
    #print(uJ1,uJ2,uJ3)
    
    localRotEnd = rg.Point3d(rotateEnd)
    #localRotEnd = rotateEnd
    localRotEnd.Transform(xform)
    
    rJ1 = localRotEnd[0] # spostamento in direzione dell'asse rosso 
    rJ2 = localRotEnd[1] # spostamento in direzione dell'asse verde
    rJ3 = localRotEnd[2] # spostamento linea d'asse

## ------------------- displacement value -------------------------##
    Length = ghcomp.Length(line)
    divideDistance = 0.5
    DivCurve = ghcomp.DivideDistance(line,divideDistance)
    PointsDivLength = DivCurve[0]
    s = dg.linspace(0,Length, len(PointsDivLength))
    AlphaY = dg.alphat( E, G, Iy, Avz )
    AlphaZ = dg.alphat( E, G, Iz, Avy )
    
    localTransVector = []
    localRotVector = []
    globalTransVector = []
    globalRotVector = []
    
    #----------------------- local to global-------------------------#
    p2p = rg.Transform.PlaneToPlane(  WorldPlane, localPlane )
    xform2 = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    p2pI = rg.Transform.TryGetInverse( p2p )
    #----------------------------------------------------------------#
    for index, x in enumerate(s):
        
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = dg.spostu(x, Length, uI3, uJ3)
        u3Vector = u3*axis3
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
        v1 =  dg.spostv(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        v1Vector = v1*axis1 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
        v2 =  dg.spostw(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        v2Vector = v2*axis2 
        
        ## RISULTANTE SPOSTAMENTI ##
        transResult = v1Vector + v2Vector + u3Vector
        localTransVector.append(transResult)
        
        r2x =  dg.thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        r1x =  dg.psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        r3x = dg.phix(x, Length, rI3, rJ3)
        
        rotResult = r1x*axis1 + r2x*axis2 + r3x*axis3
        localRotVector.append( rotResult )

        #------------- WORLD PLANE on point start of line ---------------#
        #WorldPlane2 = ghcomp.Move(worldPlane, transResult)[0]
        #localPlane2 = ghcomp.Move(localPlane, transResult)[0]
        #----------------------------------------------------------------#
        #----------------------- local to global-------------------------#
        #xform2 = rg.Transform.ChangeBasis(  WorldPlane, localPlane2 )
        #----------------------------------------------------------------# 
        globalRot = rg.Point3d( rotResult )
        globalRot.Transform(p2p) 
        globalRot.Transform(xform2) 
        #globalRot.Transform(p2pI) 
        globalRotVector.append( globalRot ) 
        globalTrasl = rg.Point3d( transResult ) 
        globalTrasl.Transform(p2p) 
        globalTrasl.Transform(xform2) 
        #globalTrasl.Transform(p2pI) 
        globalTransVector.append( globalTrasl )
    return  [  localTransVector, localRotVector , versor, PointsDivLength, globalTransVector, globalRotVector ] 

## node e nodeDisp son dictionary ##
def defTruss( ele, node, nodeDisp, scale ):
    
    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    traslStart = pointDispWrapperDict.get( indexStart -1 , "never")
    traslEnd = pointDispWrapperDict.get( indexEnd -1 , "never")
    pointStart = pointWrapperDict.get( indexStart -1 , "never")
    pointEnd = pointWrapperDict.get( indexEnd -1 , "never")
    line = rg.LineCurve( ghcomp.Move(pointStart, scale*traslStart)[0], ghcomp.Move( pointEnd, scale*traslEnd )[0] )

    axis3 = pointEnd - pointStart
    axis3.Unitize()
    axis1 =  rg.Vector3d( propSection[9][0], propSection[9][1], propSection[9][2]  )
    axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
    versor = [ axis1, axis2, axis3 ] 
    
    globalTransVector = [ traslStart, traslEnd ]
    PointsDivLength = [ pointStart, pointEnd ]
    
    return  [ line, versor, PointsDivLength, globalTransVector ] 
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


modelCurve = []
ShellDefModel = []
ExtrudedView = rg.Mesh()

traslTimoshenkoBeamValue = []
rotTimoshenkoBeamValue = []

defSectionPolyline = []

traslTrussValue = []

traslShellValue = []
rotShellValue = []
ExtrudedShell = []

SolidDefModel = []
traslSolidValue = []

PointCurveDef = []

for ele in EleOut :
    eleType = ele[2][0]
    nNode = len( ele[1] )
    
    if eleType == 'ElasticTimoshenkoBeam' :
        
        dimSection = ele[2][10]
        color = ele[2][12]
        valueTBeam = defValueTimoshenkoBeam( ele, pointWrapperDict, pointDispWrapperDict )
        localTrans = valueTBeam[0]
        localRot = valueTBeam[1]
        globalTrans = valueTBeam[4]
        globalRot = valueTBeam[5]
        PointsDivLength = valueTBeam[3]
        axis1 = valueTBeam[2][0]
        axis2 = valueTBeam[2][1]
        axis3 = valueTBeam[2][2]
        transPoint = []
        traslTimoshenkoBeamValue.append( globalTrans ) 
        rotTimoshenkoBeamValue.append( globalRot )
        defSection = []
        sectionPolyline = []
        print( localTrans[-1] )
        print( globalTrans[-1] )
        
        for beamPoint, vectorMove, vectoreRotate in zip( PointsDivLength, localTrans, localRot ):
            MovDefpoint = ghcomp.Move( beamPoint, scaleDef*vectorMove )[0]
            transPoint.append( MovDefpoint )
            
            ## Parametri per vista estrusa modello deformato ##
            sectionPlane = rg.Plane( MovDefpoint, axis1, axis2 )
            centerRotatation = MovDefpoint
            r1 = vectoreRotate[0]
            r2 = vectoreRotate[1]
            r3 = vectoreRotate[2]
            sectionPlane.Rotate( scaleDef*r1, axis1, centerRotatation )
            sectionPlane.Rotate( scaleDef*r2, axis2, centerRotatation )
            sectionPlane.Rotate( scaleDef*r3, axis3, centerRotatation )
            
            if dimSection[0] == 'rectangular' :
                width, height = dimSection[1], dimSection[2]
                section = dg.AddRectangleFromCenter( sectionPlane, width, height )
                
            if dimSection[0] == 'circular' :
                radius  = dimSection[2]
                section = AddCircleFromCenter( sectionPlane, radius )
            
            defSection.append( section )
            widthCurve, heightCurve = 0.05, 0.05
            sectionPoly = dg.AddRectangleFromCenter( sectionPlane, widthCurve, heightCurve )
            sectionPolyline.append( sectionPoly )
            
        defSectionPolyline.append( sectionPolyline )
        #defpolyline = rg.PolylineCurve( transPoint )
        #modelCurve.append( defpolyline )
        # estrusione della beam #
        meshdef = meshLoft3( defSection,  color )
        ExtrudedView.Append( meshdef )
        #doc.Objects.AddMesh( meshdef )
        
    elif eleType == 'Truss' :
        dimSection = ele[2][10]
        color = ele[2][12]
        #print( color )
        valueTruss = defTruss( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
        modelCurve.append( valueTruss[0] )
        PointsDivLength = valueTruss[3]
        axis1 = valueTruss[1][0]
        axis2 = valueTruss[1][1]
        axis3 = valueTruss[1][2]
        PointsDivLength = valueTruss[2]
        globalTrans = valueTruss[3]
        traslTrussValue.append( globalTrans ) 
        defSection = []
        sectionPolyline = []
        
        for beamPoint, vectorMove in zip( PointsDivLength, globalTrans):
            MovDefpoint = ghcomp.Move( beamPoint, scaleDef*vectorMove )[0]
            ## Parametri per vista estrusa modello deformato ##
            sectionPlane = rg.Plane( MovDefpoint, axis1, axis2 )
            
            if dimSection[0] == 'rectangular' :
                width, height = dimSection[1], dimSection[2]
                section = dg.AddRectangleFromCenter( sectionPlane, width, height )
                
            if dimSection[0] == 'circular' :
                radius  = dimSection[2]
                section = AddCircleFromCenter( sectionPlane, radius )

            defSection.append( section )
            
            # For polyline
            widthCurve, heightCurve = 0.05, 0.05
            sectionPoly = dg.AddRectangleFromCenter( sectionPlane, widthCurve, heightCurve )
            sectionPolyline.append( sectionPoly )
            
        #defSectionPolyline.append( sectionPolyline )
        # estrusione della truss #
        
        meshdef = meshLoft3( defSection,  color )
        ExtrudedView.Append( meshdef )
        doc.Objects.AddMesh( meshdef )

    elif nNode == 4 and eleType != 'FourNodeTetrahedron':
        shellDefModel = defShellQuad( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
        ShellDefModel.append( shellDefModel[0] )
        thick = ele[2][1]
        traslShellValue.append( shellDefModel[1] )
        rotShellValue.append( shellDefModel[2] )
        vt = shellDefModel[0].Vertices
        shellDefModel[0].FaceNormals.ComputeFaceNormals()
        fid,MPt = shellDefModel[0].ClosestPoint(vt[0],0.01)
        normalFace = shellDefModel[0].FaceNormals[fid]
        vectormoltiplicate = rg.Vector3f.Multiply( -normalFace, thick/2 ) 
        moveShell = ghcomp.Move( shellDefModel[0], vectormoltiplicate  )[0] 
        extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
        ExtrudedView.Append( extrudeShell )
        doc.Objects.AddMesh( extrudeShell)
        
    elif nNode == 3:
        #print( nNode )
        shellDefModel = dg.defShellTriangle( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
        ShellDefModel.append( shellDefModel[0] )
        traslShellValue.append( shellDefModel[1] )
        rotShellValue.append( shellDefModel[2] )
        
    elif nNode == 8:
        solidDefModel = defSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef)
        SolidDefModel.append( solidDefModel[0] )
        doc.Objects.AddMesh( solidDefModel[0] )
        traslSolidValue.append( solidDefModel[1] )
        ExtrudedView.Append( solidDefModel[0] )
        
    elif  eleType == 'FourNodeTetrahedron' :
        #print(ele)
        solidDefModel = defTetraSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
        SolidDefModel.append( solidDefModel[0] )
        traslSolidValue.append( solidDefModel[1] )
        ExtrudedView.append( solidDefModel[0] )

# Max Beam #
maxTraslX = []
maxTraslY = []
maxTraslZ = []
minTraslX = []
minTraslY = []
minTraslZ = []
for valuetrasl in traslTimoshenkoBeamValue:
    rowMaxX = max([row[0] for row in valuetrasl ])
    rowMaxY = max([row[1] for row in valuetrasl ])
    rowMaxZ = max([row[2] for row in valuetrasl ])
    
    rowMinX = min([row[0] for row in valuetrasl ])
    rowMinY = min([row[1] for row in valuetrasl ])
    rowMinZ = min([row[2] for row in valuetrasl ])
    
    maxTraslX.append( rowMaxX )
    maxTraslY.append( rowMaxY )
    maxTraslZ.append( rowMaxZ )
    minTraslX.append( rowMinX )
    minTraslY.append( rowMinX )
    minTraslZ.append( rowMinX )


#              txMax          tyMax         tzMax
tMax = [ max( max(rowDefX),max(maxTraslX)  ), max( max(rowDefY), max(maxTraslY) ), max( max(rowDefZ), max(maxTraslZ) ) ]
#              txMin          tyMin         tzMin
tMin = [ min( min(rowDefX), min(minTraslX) ), min( min(rowDefY), min(minTraslY) ), min( min(rowDefZ), min(minTraslZ) ) ]

if direction == 0:
    i = 0
elif direction == 1:
    i = 1
elif direction == 2:
    i = 2

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
    domain = dg.linspace( valueMin, valueMax, n)
    
    for i in range(1,n):
        if  domain[i-1] <= value <= domain[i]:
            return listcolo[ i-1 ]
        elif  valueMax <= value <= valueMax + 0.001 :
            return listcolo[ -1 ]
        elif  valueMin - 0.01 <= value <= valueMin  :
            return listcolo[ 0 ]

## Mesh from close section eith gradient color ##
def meshLoft4( point, value, valueMax, valueMin ):
    meshEle = rg.Mesh()
    for i in range(0,len(point)):
        color = gradientJet( value[i], valueMax, valueMin )
        for j in range(0, len(point[0])):
            vertix = point[i][j]
            meshEle.Vertices.Add( vertix ) 
            meshEle.VertexColors.Add( color[0],color[1],color[2] );
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
    return meshEle


modelDisp = rg.Mesh()

for curve,value in zip(defSectionPolyline,traslTimoshenkoBeamValue):
    row = [row[i] for row in value ]
    beamPolylineMesh = meshLoft4( curve, row, tMax[i], tMin[i] )
    modelDisp.Append( beamPolylineMesh )

for shellEle, value in zip(ShellDefModel,traslShellValue) :
    shellColor = shellEle.DuplicateMesh()
    shellColor.VertexColors.Clear()
    for j in range(0,shellEle.Vertices.Count):
        jetColor = gradientJet(value[j][i], tMax[i], tMin[i])
        shellColor.VertexColors.Add( jetColor[0],jetColor[1],jetColor[2] )
    modelDisp.Append( shellColor)
#dup.VertexColors.CreateMonotoneMesh(Color.Red)
#doc.Objects.AddMesh(dup)
for solidEle, value in zip(SolidDefModel,traslSolidValue) :
    solidColor = solidEle.DuplicateMesh()
    solidColor.VertexColors.Clear()
    for j in range(0,solidEle.Vertices.Count):
        jetColor = gradientJet(value[j][i], tMax[i], tMin[i])
        solidColor.VertexColors.Add( jetColor[0],jetColor[1],jetColor[2] )
    modelDisp.Append( solidColor)
        #rg.Collections.MeshVertexColorList.SetColor( solidEle,j, color[0], color[1], color[2] )



ModelDisp = modelDisp
#ModelDispExstr = th.list_to_tree([ ExtrudedBeamView ,ExtrudedShell, SolidDefModel ])
ModelDispExstr = ExtrudedView

