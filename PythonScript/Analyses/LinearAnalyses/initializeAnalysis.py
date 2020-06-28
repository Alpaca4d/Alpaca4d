"""Generate a circular cross section
    Inputs:
        AlpacaModel: Assemble model to perform Static Analyses.
    Output:
       AlpacaStaticOutput: Analysed Alpaca model.
       maxDisplacement: Maximum displacement of structure [mm].
       """


import System
import os
import Grasshopper as gh

def InitializeStaticAnalysis(AlpacaModel):
    ghFilePath = ghenv.LocalScope.ghdoc.Path

    workingDirectory = os.path.dirname(ghFilePath) 
    outputFileName = 'openSeesOutputWrapper.txt'

    for dirpath, dirnames, filenames in os.walk(workingDirectory):
        for filename in filenames:
            if filename == outputFileName:
                file = os.path.join(dirpath,outputFileName)
                os.remove(file)



    ghFolderPath = os.path.dirname(ghFilePath)
    outputFolder = os.path.join(ghFolderPath,'assembleData')
    wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )


    #userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
    fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\LinearAnalyses\openSees_StaticSolver.py'


    staticAnalyses = System.Diagnostics.ProcessStartInfo(fileName)
    staticAnalyses.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden
    staticAnalyses.Arguments = wrapperFile
    process = System.Diagnostics.Process.Start(staticAnalyses)
    System.Diagnostics.Process.WaitForExit(process)

    ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
    ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py

    outputFile = os.path.join(outputFolder, outputFileName)

    with open(outputFile, 'r') as f:
        lines = f.readlines()
        nodeDisplacementWrapper = eval( lines[0].strip() )
        reactionWrapper = eval( lines[1].strip() )
        elementOutputWrapper = eval( lines[2].strip() )
        elementLoadWrapper = eval( lines[3].strip() )
        eleForceWrapper = eval( lines[4].strip() )


    AlpacaLinearStaticOutput = ([nodeDisplacementWrapper,
                            reactionWrapper,
                            elementOutputWrapper,
                            elementLoadWrapper,
                            eleForceWrapper])

    return AlpacaLinearStaticOutput

AlpacaStaticOutput = InitializeStaticAnalysis(AlpacaModel)
checkData = True

if not AlpacaModel:
    checkData = False
    msg = "input 'AlpacaModel' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    AlpacaLinearStaticOutput = InitializeStaticAnalysis(AlpacaModel)
    maxDisplacement = None
