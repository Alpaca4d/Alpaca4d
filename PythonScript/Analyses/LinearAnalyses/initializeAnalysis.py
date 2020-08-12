"""Calculate the Static Response of the structure
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
    
    ghFilePath = ghenv.Component.Attributes.Owner.OnPingDocument().FilePath
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

    userObjectFolder = gh.Folders.DefaultUserObjectFolder
    pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
    fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\LinearAnalyses\openSees_StaticSolver.py')
    
    fileName = '"' + fileName + '"'
    wrapperFile = '"' + wrapperFile + '"'

    
    p = System.Diagnostics.Process()
    p.StartInfo.RedirectStandardOutput = True
    p.StartInfo.RedirectStandardError = True

    p.StartInfo.UseShellExecute = False
    p.StartInfo.CreateNoWindow = True
    
    p.StartInfo.FileName = pythonInterpreter
    p.StartInfo.Arguments = fileName + " " + wrapperFile
    p.Start()
    p.WaitForExit()
    
    
    msg = p.StandardError.ReadToEnd()
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)


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


checkData = True

if not AlpacaModel:
    checkData = False
    msg = "input 'AlpacaModel' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    AlpacaStaticOutput = InitializeStaticAnalysis(AlpacaModel)