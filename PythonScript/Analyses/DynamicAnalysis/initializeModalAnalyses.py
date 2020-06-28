"""Generate a circular cross section
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

def InitializeModalAnalysis(AlpacaModel, numEigenvalues):
    ghFilePath = ghenv.LocalScope.ghdoc.Path

    # delete file if already there
    workingDirectory = os.path.dirname(ghFilePath) 
    outputFileName = 'openSeesModalOutputWrapper.txt'

    for dirpath, dirnames, filenames in os.walk(workingDirectory):
        for filename in filenames:
            print(filename)
            if filename == outputFileName:
                file = os.path.join(dirpath,outputFileName)
                os.remove(file)


    ghFolderPath = os.path.dirname(ghFilePath)
    outputFolder = os.path.join(ghFolderPath,'assembleData')
    wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )

    #userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
    fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\DynamicAnalysis\openSees_ModalSolver.py'


    modalAnalyses = System.Diagnostics.ProcessStartInfo(fileName)
    modalAnalyses.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden
    modalAnalyses.Arguments = wrapperFile + " " + str(numVibrationModes)
    process = System.Diagnostics.Process.Start(modalAnalyses)
    System.Diagnostics.Process.WaitForExit(process)

    ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
    ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py

    outputFile = os.path.join(outputFolder, outputFileName)

    with open(outputFile, 'r') as f:
        lines = f.readlines()
        nodeModalDispWrapper = eval( lines[0].strip() )
        elementModalWrapper = eval( lines[1].strip() )
        period = eval( lines[2].strip() )
        frequency = eval( lines[3].strip() )


    AlpacaModalOutputWrapper = ([nodeModalDispWrapper,
                            elementModalWrapper,
                            period,
                            frequency])

    return [AlpacaModalOutputWrapper, period, frequency]

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
    AlpacaModalOutput, period, frequency = InitializeModalAnalysis(AlpacaModel, numVibrationModes)