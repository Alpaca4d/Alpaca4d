"""Calculate the Natural Vibration of the structure
    Inputs:
        AlpacaModel: Assemble model to perform Modal Analyses.
        numEigenvalues: Number of modes to be calculated.
    Output:
       AlpacaModalOutput: Analysed Alpaca model.
       frequency: Frequencies of the corrisponding modes [Hz].
       period: Periods of the corrisponding modes [s].
       """


import System
import os
import Grasshopper as gh
import ghpythonlib.treehelpers as th # per data tree
import Rhino.Geometry as rg

def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]

def spectrum( ag, F0, S, n, Tb, Tc, Td, q, T ):

    if 0 <= T < Tb :
        return (ag*S*n*F0*(T/Tb + (1/(n*F0))*(1 - T/Tb)))/q
    elif Tb <= T < Tc :
        return  (ag*S*n*F0)/q
    elif Tc <= T < Td :
        return  (ag*S*n*F0*(Tc/T))/q
    elif  T >= Td :
        return  (ag*S*n*F0*(Tc*Td/T**2))/q


def InitializeModalAnalysis( AlpacaModel, numEigenvalues, ag, F0, S,n, Tb, Tc, Td, q ):
    if n is None :
        n = 0.55

    ghFilePath = ghenv.Component.Attributes.Owner.OnPingDocument().FilePath

    # delete file if already there
    workingDirectory = os.path.dirname(ghFilePath) 
    outputFileName = 'openSeesLinearDynamicOutputWrapper.txt'

    for dirpath, dirnames, filenames in os.walk(workingDirectory):
        for filename in filenames:
            #print(filename)
            if filename == outputFileName:
                file = os.path.join(dirpath,outputFileName)
                os.remove(file)


    ghFolderPath = os.path.dirname(ghFilePath)
    outputFolder = os.path.join(ghFolderPath,'assembleData')
    wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )



    userObjectFolder = gh.Folders.DefaultUserObjectFolder
    pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
    fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\LinearDynamicAnalysis\openSees_linearDynamicSolver.py')
    
    wrapperFile = '"' + wrapperFile + '"'
    fileName = '"' + fileName + '"'
    
    p = System.Diagnostics.Process()
    p.StartInfo.RedirectStandardOutput = True
    p.StartInfo.RedirectStandardError = True

    p.StartInfo.UseShellExecute = False
    p.StartInfo.CreateNoWindow = True
    
    p.StartInfo.FileName = pythonInterpreter
    p.StartInfo.Arguments = fileName + " " + wrapperFile + " " + str(numVibrationModes)
    p.Start()
    p.WaitForExit()
    
    
    msg = p.StandardError.ReadToEnd()
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)

    ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
    ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py

    outputFile = os.path.join(outputFolder, outputFileName)
    
    with open(outputFile, 'r') as f:
        lines = f.readlines()
        nodeModalDispWrapper = eval( lines[0].strip() )
        period = eval( lines[1].strip() )
        frequency = eval( lines[2].strip() )
        massPart = eval( lines[3].strip() )
        cPart = eval( lines[4].strip() )
        nodeMass = eval( lines[5].strip() )

    numberMode = numEigenvalues

    ForceX = []
    ForceY = []
    for nodeOutput, gamma, T in zip( nodeModalDispWrapper, cPart , period ):
        possNode = [ row[0] for row in nodeOutput ]
        nodeDisp = [ row[1] for row in nodeOutput ]
        Sa = spectrum( ag, F0, S, n, Tb, Tc, Td, q, T )
        nodeDispX = [ row[0] for row in nodeDisp ]
        nodeDispY = [ row[1] for row in nodeDisp ]
        Fx = []
        Fy = []
        for MassNode, nodeDispValueX, nodeDispValueY  in zip(nodeMass, nodeDispX, nodeDispY ):
            FXnode = MassNode*nodeDispValueX*gamma[0]*Sa
            Fx.append( FXnode )
            FYnode = MassNode*nodeDispValueY*gamma[1]*Sa
            Fy.append( FYnode )
        ForceX.append( Fx )
        ForceY.append( Fy )

    eta = 0.05
    Ex = []
    Ey = []

    for Ti, fxi, fyi in zip(period, ForceX, ForceY ):
        for Tj, fxj, fyj in zip(period, ForceX, ForceY ):
            Bij = Tj/Ti
            delta_ij = ( 8*eta**2*Bij**(3/2))/( (1 + Bij)*((1 - Bij )**2 + 4*eta**2*Bij ))

            Ex_node = []
            Ey_node = []
            for fxi_node, fyi_node, fxj_node, fyj_node in zip( fxi, fyi, fxj, fyj):

                Ex_node.append( delta_ij*fxi_node*fxj_node )  
                Ey_node.append( delta_ij*fyi_node*fyj_node )
            Ex.append( Ex_node )
            Ey.append( Ey_node )

    #print( len(Ex ))
    EX = []
    EY = []
    for i in range(0, len( Ex[0] )):
        EX.append( sum( [ row[i] for row in Ex ] ) )
        EY.append( sum( [ row[i] for row in Ey ] ) )
#------------------------------------------------------------------------------#

    possNodeForce = []
    for nodeCoord in  possNode:
        possNodeForce.append( rg.Point3d( nodeCoord[0], nodeCoord[1], nodeCoord[2], ) )



    #print(  [ row[1] for row in nodeModalDispWrapper[0] ] )

    massPart = th.list_to_tree( massPart )

    Ti = linspace(0, 3.00, 20)
    spectrumValor = []
    for T in Ti:
        spectrumValor.append( spectrum( ag, F0, S, n, Tb, Tc, Td, q, T ) )


    return [possNodeForce, period, frequency, massPart, spectrumValor, EX, EY ]

checkData = True

if not AlpacaModel:
    checkData = False
    msg = "input 'AlpacaModel' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if numVibrationModes is None:
    checkData = False
    msg = "input 'numEigenvalues' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    possNodeForce, period, frequency, massPart, spectrum, ForceX, ForceY = InitializeModalAnalysis(AlpacaModel, numVibrationModes, ag, F0, S, n,  Tb, Tc, Td, q )