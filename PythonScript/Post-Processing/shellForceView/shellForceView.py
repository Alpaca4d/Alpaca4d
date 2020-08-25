"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        viewForce :  forces acting on the shell nodes.
        if you enter '0' view Fx ( forces in direction X ) ;
        if you enter '1' view Fy  ( forces in direction Y ).
        if you enter '2' view Fz  ( forces in direction Z ).
        if you enter '3' view Mx ( Moments in direction X ) ;
        if you enter '4' view My  ( Moments in direction Y ).
        if you enter '5' view Mz  ( Moments in direction Z ).
    Output:
       modelForce : view color mesh outputs which represents the trend of the chosen stress .
       ForceValue : values ​​of the chosen forces acting on the shell nodes.
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

#---------------------------------------------------------------------------------------#
def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]

def gradient(value, valueMin, valueMax, colorList ):

    if colorList == [] :
        listcolor = [ rs.CreateColor( 201, 0, 0 ),
                    rs.CreateColor( 240, 69, 7),
                    rs.CreateColor( 251, 255, 0 ),
                    rs.CreateColor( 77, 255, 0 ),
                    rs.CreateColor( 0, 255, 221 ),
                    rs.CreateColor( 0, 81, 255 )]
    else :
        listcolor = colorList

    n = len( listcolor )
    domain = linspace( valueMin, valueMax, n)
    #print( domain )
    
    for i in range(1,n+1):
        if  domain[i-1] <= value <= domain[i] :
            return listcolor[ i-1 ]
        elif  valueMax <= value <= valueMax + 0.0000000000001 :
            return listcolor[ -1 ]
        elif  valueMin - 0.0000000000001 <= value <= valueMin  :
            return listcolor[ 0 ]

def ShellQuad( ele, node):
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][2]
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
    return  shellModel 

def ShellTriangle( ele, node ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][2]
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
    
    return  shellModel

#--------------------------------------------------------------------------
def shellForceView( AlpacaStaticOutput, viewForce ):

    global modelForce
    global ForceValue

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    ForceOut = AlpacaStaticOutput[4]
    #print( ForceOut[0] )
    #print( ForceOut[1] )
    #nodalForce = openSeesOutputWrapper[5]

    #nodalForcerDict = dict( nodalForce )

    pointWrapper = []
    for index,item in enumerate(diplacementWrapper):
        pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    ## Dict. for point ##
    pointWrapperDict = dict( pointWrapper )


    forceWrapper = []

    for item in ForceOut:
        index = item[0]
        if len(item[1]) == 24: #6* numo nodi = 24 ,elementi quadrati
            Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
            Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
            Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
            Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
            Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
            Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
            Fw = rg.Vector3d( item[1][18], item[1][19], item[1][20] ) # risultante nodo w
            Mw = rg.Vector3d( item[1][21], item[1][22], item[1][23] )
            forceOut = [[ Fi.X, Fj.X, Fk.X, Fw.X ],
                        [ Fi.Y, Fj.Y, Fk.Y, Fw.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z, Fw.Z ],
                        [ Mi.X, Mj.X,  Mk.X, Mw.X ],
                        [ Mi.Y, Mj.Y, Mk.Y, Mw.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z, Mw.Z ]]
        elif len(item[1]) == 18: #6* numo nodi = 18 ,elementi triangolae
            Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
            Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
            Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
            Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
            Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
            Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
            forceOut = [[ Fi.X, Fj.X, Fk.X ],
                        [ Fi.Y, Fj.Y, Fk.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z ],
                        [ Mi.X, Mj.X,  Mk.X ],
                        [ Mi.Y, Mj.Y, Mk.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z ]]
        forceWrapper .append( [index, forceOut ])

    ## Dict. for force ##
    forceWrapperDict = dict( forceWrapper )
    ####
    ForceView = []
    tag = []
    shell = []
    for ele in EleOut :
        eleTag = ele[0]
        eleType = ele[2][0]
        if eleType == "ShellMITC4" :
            tag.append( eleTag )
            outputForce = forceWrapperDict.get( eleTag )
            ForceView.append( outputForce[viewForce] )
            shellModel = ShellQuad( ele, pointWrapperDict )
            shell.append( shellModel )
        elif eleType == "shellDKGT" :
            tag.append( eleTag )
            outputForce = forceWrapperDict.get( eleTag )
            ForceView.append( outputForce[viewForce] )
            shellModel = ShellTriangle( ele, pointWrapperDict )
            shell.append( shellModel )
            
    #tagElement = th.list_to_tree( tag )
    ForceValue =  ForceView 
    
    maxValue = []
    minValue = []
    for value in ForceView:
        maxValue.append( max( value ))
        minValue.append( min( value ))

    maxValue = max( maxValue )
    minValue = min( minValue )
    domainValues = [minValue, maxValue ]

    
    modelForce = []
    """
    for shellEle, value in zip(shell,ForceView) :
        shellColor = shellEle.DuplicateMesh()
        shellColor.VertexColors.Clear()

        for j in range(0,shellEle.Vertices.Count):
            #print( value[j] )
            jetColor = gradient( value[j], minValue, maxValue, colorList )
            shellColor.VertexColors.Add( jetColor )
        modelForce.append( shellColor)
    """
    for shellEle, value in zip(shell,ForceView) :
        shellColor = shellEle.DuplicateMesh()
        shellColor.VertexColors.Clear()
        faceforce = value[ face ]
        Color = gradient( faceforce, minValue, maxValue, colorList )
        shellColor.VertexColors.CreateMonotoneMesh( Color )
        modelForce.append( shellColor)

    
    return modelForce, ForceValue, domainValues

checkData = True

if not AlpacaStaticOutput:
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if viewForce is None :
    checkData = False
    msg = " input 'viewForce' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    shell, ForceValue, domainValues = shellForceView( AlpacaStaticOutput, viewForce  )