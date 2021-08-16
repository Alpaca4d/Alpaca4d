"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        numberResults : number of discretizations for beam.
    Output:
       tagElement : number of the tag of Beam or Truss element .
       localTrans : Displacements related to the local axis ( 1-Red, 2-Green, 3-Blue).
       localRot : Rotation related to the local axis ( 1-Red, 2-Green, 3-Blue).
       globalTrans : Displacements related to the global axis ( XYZ ).
       globalRot : Rotation related to the global axis ( XYZ ).
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

#---------------------------------------------------------------------------------------#
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

def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]
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
    DivCurve = linspace( 0, Length, numberResults )
    if DivCurve == None:
        DivCurve = [ 0, Length]
        
    #s = dg.linspace(0,Length, len(PointsDivLength))
    AlphaY = alphat( E, G, Iy, Avz )
    AlphaZ = alphat( E, G, Iz, Avy )
    
    globalTransVector = []
    globalRotVector = []
    localTransVector = []
    localRotVector = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = spostu(x, Length, uI3, uJ3)
        u3Vector = u3*axis3
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
        v1 =  spostv(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        v1Vector = v1*axis1 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
        v2 =  spostw(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        v2Vector = v2*axis2 
        
        ## RISULTANTE SPOSTAMENTI ##
        transResult = v1Vector + v2Vector + u3Vector
        localTransVector.append( transResult )

        r2x =  thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        r1x =  psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        r3x = phix(x, Length, rI3, rJ3)
        
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
    
    traslStart = nodeDisp.get( indexStart -1 , "never")
    traslEnd = nodeDisp.get( indexEnd -1 , "never")
    if len( traslStart ) == 2:
        traslStart = nodeDisp.get( indexStart -1 , "never")[0]
        traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]

    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
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
    DivCurve = linspace( 0, Length, numberResults )
    if DivCurve == None:
        DivCurve = [ 0, Length]

    globalTransVector = []
    localTransVector = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = spostu(x, Length, uI3, uJ3)
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
def beamDisp( AlpacaStaticOutput, numberResults ):

    if numberResults is None :
       numberResults = 2 

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    nodeValue = []
    displacementValue = []

    pointWrapper = []
    dispWrapper = []
    for index,item in enumerate(diplacementWrapper):
        nodeValue.append( item[0] )
        displacementValue.append( item[1] )
        print( item[0] )
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

    return tagElement, localTrans, localRot, globalTrans, globalRot


checkData = True

if not AlpacaStaticOutput :
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    tagElement, localTrans, localRot, globalTrans, globalRot = beamDisp( AlpacaStaticOutput , numberResults )
