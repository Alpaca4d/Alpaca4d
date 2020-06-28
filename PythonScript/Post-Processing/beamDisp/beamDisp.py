"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        numberResults : number of discretizations for beam.
    Output:
       tagElement : number of the tag of Beam or Truss element .
       localTrans : Displacements related to the local system ( 1- red, 2-green, 3-blue).
       localRot : Rotation related to the local system ( 1- red, 2-green, 3-blue).
       globalTrans : Displacements related to the global system ( XYZ ).
       globalRot : Rotation related to the global system ( XYZ ).
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import ghpythonlib.components as ghcomp
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

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
fileName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 
#---------------------------------------------------------------------------------------#

## node e nodeDisp son dictionary ##
def defValueTimoshenkoBeamValue( ele, node, nodeDisp, numberResults ):
    #---------------- WORLD PLANE ----------------------#
    WorldPlane = rg.Plane.WorldXY
    #--------- Propriety TimoshenkoBeam  ----------------#
    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    color = propSection[12]
    E = propSection[1]
    G = propSection[2]
    A = propSection[3]
    Avz = propSection[4]
    Avy = propSection[5]
    Jxx = propSection[6]
    Iy = propSection[7]
    Iz = propSection[8]
    #---- traslation and rotation index start & end ------- #
    traslStart = nodeDisp.get( indexStart -1 , "never")[0]
    rotateStart = nodeDisp.get( indexStart -1 , "never")[1]
    traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
    rotateEnd = nodeDisp.get( indexEnd -1 , "never")[1]
    ##-------------------------------------------- ------------##
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    line = rg.LineCurve( pointStart, pointEnd )
    #-------------------------versor ---------------------------#
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    versor = [ axis1, axis2, axis3 ] 
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localTraslStart = rg.Point3d( traslStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ traslStart, rotateStart, traslEnd, rotateEnd ] )
    #print( vectorTrasform[0] )
    localTraslStart = vectorTrasform[0]
    uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
    uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
    uI3 = localTraslStart.Z # spostamento linea d'asse
    localRotStart = vectorTrasform[1]
    rI1 = localRotStart.X # 
    rI2 = localRotStart.Y # 
    rI3 = localRotStart.Z # 
    localTraslEnd = vectorTrasform[2]
    uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
    uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
    uJ3 = localTraslEnd.Z # spostamento linea d'asse
    localRotEnd = vectorTrasform[3]
    rJ1 = localRotEnd[0] #  
    rJ2 = localRotEnd[1]  # 
    rJ3 = localRotEnd[2]  # 
    ##------------------ displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    DivCurve = dg.linspace( 0, Length, numberResults )
    if DivCurve == None:
        DivCurve = [ 0, Length]
        
    #s = dg.linspace(0,Length, len(PointsDivLength))
    AlphaY = dg.alphat( E, G, Iy, Avz )
    AlphaZ = dg.alphat( E, G, Iz, Avy )
    
    globalTransVector = []
    globalRotVector = []
    localTransVector = []
    localRotVector = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
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
        localTransVector.append( transResult )

        r2x =  dg.thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        r1x =  dg.psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        r3x = dg.phix(x, Length, rI3, rJ3)
        
        rotResult = r1x*axis1 + r2x*axis2 + r3x*axis3
        localRotVector.append( rotResult )
         
        globalRot = rg.Point3d( rotResult ) 
        globalRot.Transform(xform2[1]) 
        globalRot.Transform(xform)
        globalRotVector.append( rg.Vector3d( globalRot ) ) 
        globalTrasl = rg.Point3d( transResult ) 
        globalTrasl.Transform(xform2[1]) 
        globalTrasl.Transform(xform)
        globalTransVector.append( rg.Vector3d( globalTrasl ) )
        
    return  [  localTransVector, localRotVector ,  globalTransVector, globalRotVector ] 

## node e nodeDisp son dictionary ##
def defTrussValue( ele, node, nodeDisp, numberResults ):
    WorldPlane = rg.Plane.WorldXY
    TagEle = ele[0]
    propSection = ele[2]
    color = propSection[12]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    E = propSection[1]
    A = propSection[3]
    
    traslStart = pointDispWrapperDict.get( indexStart -1 , "never")
    traslEnd = pointDispWrapperDict.get( indexEnd -1 , "never")
    if len( traslStart ) == 2:
        traslStart = pointDispWrapperDict.get( indexStart -1 , "never")[0]
        traslEnd = pointDispWrapperDict.get( indexEnd -1 , "never")[0]
    pointStart = pointWrapperDict.get( indexStart -1 , "never")
    pointEnd = pointWrapperDict.get( indexEnd -1 , "never")
    #print( traslStart[1] )
    line = rg.LineCurve( pointStart,  pointEnd )

    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    versor = [ axis1, axis2, axis3 ] 
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localTraslStart = rg.Point3d( traslStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ traslStart , traslEnd ] )
    #print( vectorTrasform[0] )
    localTraslStart = vectorTrasform[0]
    uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
    uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
    uI3 = localTraslStart.Z # spostamento linea d'asse
    localTraslEnd = vectorTrasform[1]
    uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
    uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
    uJ3 = localTraslEnd.Z # spostamento linea d'asse
    ##-------------- displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    DivCurve = dg.linspace( 0, Length, numberResults )
    if DivCurve == None:
        DivCurve = [ 0, Length]

    globalTransVector = []
    localTransVector = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = dg.spostu(x, Length, uI3, uJ3)
        u3Vector = u3*axis3
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
        v1 =  x*( uJ1 - uI1 )/Length + uI1
        v1Vector = v1*axis1 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
        v2 =  x*( uJ2 - uI2 )/Length + uI2
        v2Vector = v2*axis2 
        ## RISULTANTE SPOSTAMENTI ##
        transResult = v1Vector + v2Vector + u3Vector
        localTransVector.append( transResult )
        
        globalTrasl = rg.Point3d( transResult ) 
        globalTrasl.Transform(xform2[1]) 
        globalTrasl.Transform(xform)
        globalTransVector.append( rg.Vector3d( globalTrasl ) )

    return  [ localTransVector, globalTransVector] 

#--------------------------------------------------------------------------
diplacementWrapper = AlpacaStaticOutput[0]
EleOut = AlpacaStaticOutput[2]

pointWrapper = []
transWrapper = []
rotWrapper = []

diplacementWrapper = AlpacaStaticOutput[0]
EleOut = AlpacaStaticOutput[2]
nodeValue = []
displacementValue = []

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

transLocal = []
rotLocal = []
transGlobal = []
rotGlobal = []
tag = []
for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == 'ElasticTimoshenkoBeam' :
        valueTBeam = defValueTimoshenkoBeamValue( ele, pointWrapperDict, pointDispWrapperDict, numberResults )
        transLocal.append(valueTBeam[0])
        rotLocal.append(valueTBeam[1])
        transGlobal.append(valueTBeam[2])
        rotGlobal.append(valueTBeam[3])
        tag.append( eleTag )
    elif eleType == 'Truss' :
        valueTruss = defTrussValue( ele, pointWrapperDict, pointDispWrapperDict, numberResults )
        transLocal.append(valueTruss[0])
        rotLocal.append([rg.Vector3d(0,0,0)]*len(valueTruss[0]))
        transGlobal.append(valueTruss[1])
        rotGlobal.append([rg.Vector3d(0,0,0)]*len(valueTruss[0]))
        tag.append( eleTag )

localTrans = th.list_to_tree( transLocal )
localRot = th.list_to_tree( rotLocal )
globalTrans = th.list_to_tree( transGlobal )
globalRot = th.list_to_tree( rotGlobal )
tagElement = tag
