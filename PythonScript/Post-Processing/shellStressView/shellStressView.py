"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        stressView :  stress acting on the shell nodes.
        '0' - sigmaX ( membrane stress X ) ;
        '1' - sigmaY  ( membrane stress Y );
        '2' - sigmaXY ( membrane stress XY );
        '3' - tauX  ( transverse shear forces X );
        '4' - tauY ( transverse shear forces Y ).
        '5' - mX ( bending moment X ) ;
        '6' - my  ( bending moment Y );
        '7' - mxy ( bending moment XY  );
    Output:
        shell :  mesh that represent the shell.
        stressValue : valor of stress acting on the shell nodes.
        """

import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import Grasshopper as gh
import sys
import os
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

def ShellStressQuad( ele, node ):
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

def ShellStressTriangle( ele, node ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][2]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    
    
    ## CREO IL MODELLO  ##
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
def shellStressView( AlpacaStaticOutput, stressView ):

    global shell
    global stressValue

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

    shell4Tag = []
    shell3Tag = []
    for item in EleOut:
        if  len(item[1])  == 4:
             shell4Tag.append(item[0])

        if  len(item[1])  == 3:
             shell3Tag.append(item[0])

    ## Dict. for force ##
    #forceWrapperDict = dict( forceWrapper )
    #ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
    ghFilePath = ghenv.LocalScope.ghdoc.Path
    workingDirectory = os.path.dirname( ghFilePath )
    outputFile4 = os.path.join(workingDirectory, 'assembleData\\tensionShell4.out' )
    outputFile3 = os.path.join(workingDirectory, 'assembleData\\tensionShell3.out' )
    #---------------------------------------------------#
    tensionDic = []
      
    #print(len(tensionList)/len(shellTag))

    #print(stressView + 24)

    with open(outputFile4, 'r') as f:
        lines = f.readlines()
        if lines :
            tension4List = lines[0].split()

    #print( len( shell4Tag  ), len( tension4List ))

    for n,eleTag in enumerate(shell4Tag) :
        tensionShell = []
        for i in range( (n)*32, ( n + 1 )*32  ):
            tensionShell.append( float(tension4List[i]) )
        tensionView = [ tensionShell[ stressView ], tensionShell[ stressView + 8 ], tensionShell[ stressView + 16 ], tensionShell[ stressView + 24 ] ]
        tensionDic.append([ eleTag, tensionView ])

    with open(outputFile3, 'r') as f:
        lines = f.readlines()
        if lines :
            tension3List = lines[0].split()

    #print( len( shell3Tag  ), len( tension3List ))

    for n,eleTag in enumerate(shell3Tag) :
        tensionShell = []
        for i in range( (n)*32, ( n + 1 )*32  ): # invece di 32 dovrebbe essere
            tensionShell.append( float(tension3List[i]) )
        tensionView = [ tensionShell[ stressView ], tensionShell[ stressView + 8 ], tensionShell[ stressView + 16 ] ]
        tensionDic.append([ eleTag, tensionView ])

    stressDict = dict( tensionDic )
    stressValue = stressDict.values() 
    #print( stressDict.get(2))
    #print( stressDict )
    #print( tensionList[0], tensionList[8], tensionList[16], tensionList[24] )
    #print( tensionDic[0] )
    
    maxValue = []
    minValue = []
    for value in stressDict.values():
        maxValue.append( max( value ))
        minValue.append( min( value ))
        
    maxValue = max( maxValue )
    minValue = min( minValue )
    domainValues = [minValue, maxValue ] 

    shell = []
    for ele in EleOut :
        eleTag = ele[0]
        eleType = ele[2][0]
        if eleType == "ShellMITC4" :
            shellModel = ShellStressQuad( ele, pointWrapperDict )
            shell.append( shellModel )
        elif eleType == "shellDKGT" :
            #outputForce = forceWrapperDict.get( eleTag )
            shellModel = ShellStressTriangle( ele, pointWrapperDict )
            shell.append( shellModel )

    modelStress = []
    for shellEle, value in zip(shell,stressValue) :
        shellColor = shellEle.DuplicateMesh()
        shellColor.VertexColors.Clear()
        for j in range(0,shellEle.Vertices.Count):
            #print( value[j] )
            jetColor = gradient(value[j], minValue, maxValue, colorList )
            shellColor.VertexColors.Add( jetColor )
        modelStress.append( shellColor)

    return modelStress, stressValue, domainValues

checkData = True

if not AlpacaStaticOutput :
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if stressView is None :
    checkData = False
    msg = " input 'stressView' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    shell, stressValue, domainValues = shellStressView( AlpacaStaticOutput, stressView )