import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import System as sy #DV
import sys

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

def defValueTimoshenkoBeamValue( ele, node, nodeDisp ):
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
    Length = line.GetLength()
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
    return  [  localTransVector, localRotVector , globalTransVector, globalRotVector ] 

## node e nodeDisp son dictionary ##
def defTrussValue( ele, node, nodeDisp, scale ):
    
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
    
    return  [ globalTransVector ] 

#--------------------------------------------------------------------------
diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]

pointWrapper = []
transWrapper = []
rotWrapper = []

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

transLocal = []
rotLocal = []
transGlobal = []
rotGlobal = []
tag = []
for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == 'ElasticTimoshenkoBeam' :
        valueTBeam = defValueTimoshenkoBeamValue( ele, pointWrapperDict, pointDispWrapperDict )
        transLocal.append(valueTBeam[0])
        rotLocal.append(valueTBeam[1])
        transGlobal.append(valueTBeam[2])
        rotGlobal.append(valueTBeam[3])
        tag.append( eleTag )
    elif eleType == 'Truss' :
        valueTruss = defTrussValue( ele, pointWrapperDict, pointDispWrapperDict )
        transLocal.append(valueTruss[0])
        rotLocal.append([0,0,0]*len(valueTruss[0]))
        transGlobal.append(valueTruss[1])
        rotGlobal.append([0,0,0]*len(valueTruss[0]))
        tag.append( eleTag )

localTrans = transLocal
localRot = rotLocal
globalTrans = transGlobal
globalRot = rotGlobal
tagElement = tag