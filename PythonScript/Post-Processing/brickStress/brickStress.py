"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        stressView:  stress acting on the brick nodes.
            '0' - sigmaX (membrane stress X).
            '1' - sigmaY (membrane stress Y).
            '2' - sigmaZ (membrane stress XY).
            '3' - tauX  (transverse shear forces X).
            '4' - tauY (transverse shear forces Y).
            '5' - tauZ  (transverse shear forces Z).
    Output:
        brick:  mesh representing the brick.
        stressValue: values of stress acting on the brick nodes.
        """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

#---------------------------------------------------------------------------------------#
def Solid( ele, node ):
    
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
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
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

#--------------------------------------------------------------------------
def brickStressView( AlpacaStaticOutput, stressView ):

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    #print( ForceOut[0] )
    #print( ForceOut[1] )
    #nodalForce = AlpacaStaticOutput[5]

    #nodalForcerDict = dict( nodalForce )

    pointWrapper = []
    for index,item in enumerate(diplacementWrapper):
        pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    ## Dict. for point ##
    pointWrapperDict = dict( pointWrapper )

    EleTag = []
    for item in EleOut:
        if  len(item[1])  == 8:
             EleTag.append([item[0], 48])
        elif  len(item[0])  == 'FourNodeTetrahedron':
             EleTag.append([item[0], 24])

    ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
    workingDirectory = os.path.dirname(ghFilePath)
    outputFile = os.path.join(workingDirectory, 'assembleData\\tensionShell.out' )

    with open(outputFile, 'r') as f:
        lines = f.readlines()
        tensionList = lines[0].split()

    #print(len(tensionList)/len(shellTag))

    w = stressView
    #print(w + 24)
    tensionDic = []
    for n,eleTag in enumerate(EleTag) :
        tensionShell = []
        for i in range( (n)*eleTag[1] , ( n + 1 )*eleTag[1]  ):
            tensionShell.append( float(tensionList[i]) )
        if eleTag[1] == 48:
            tensionView = [ tensionShell[ w ], tensionShell[ w + 6 ], tensionShell[ w + 12 ], tensionShell[ w + 18 ], tensionShell[ w + 24 ], tensionShell[ w + 30 ], tensionShell[ w + 36 ], tensionShell[ w + 42 ] ]
        elif eleTag[1] == 24:
            tensionView = [ tensionShell[ w ], tensionShell[ w + 6 ], tensionShell[ w + 12 ], tensionShell[ w + 18 ]]
        tensionDic.append([ eleTag[0], tensionView ])

    stressDict = dict( tensionDic )
    stressValue = th.list_to_tree( stressDict.values() )
    #print( stressDict.get(2))
    #print( stressDict )
    #print( tensionList[0], tensionList[8], tensionList[16], tensionList[24] )
    #print( tensionDic[0] )
    '''
    maxValue = []
    minValue = []
    for value in stressDict.values():
        maxValue.append( max( value ))
        minValue.append( min( value ))
        
    maxValue = max( maxValue )
    minValue = min( minValue )
    print( maxValue, minValue )
    '''
    brick = []
    for ele in EleOut :
        eleTag = ele[0]
        eleType = ele[2][0]
        if eleType == "bbarBrick" :
            brickModel = Solid( ele, pointWrapperDict )
            brick.append( brickModel )
        elif eleType == "ShellDKGT" :
            outputForce = forceWrapperDict.get( eleTag )
            tetraModel = ShellTriangle( ele, pointWrapperDict )
            brick.append( tetraModel )

    return brick, stressValue

checkData = True

if not AlpacaStaticOutput:
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if stressView is None :
    checkData = False
    msg = " input 'stressView' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    brick, stressValue = brickStressView( AlpacaStaticOutput, stressView )
