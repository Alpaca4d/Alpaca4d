"""Calculate the Static Response of the structure
    Inputs:
        AlpacaModel: Assembled model to perform Static Analyses.
        TmaxAnalyses: Time Frame where the structure will be analyse
        GroundMotionDirection: Direction of the earthQuake. 1 = X, 2 = Y, 3 = Z
        GroundMotionValues: Acceleration values for each time step
        GroundMotionTimeStep: time step for each acceleration value
        GroundMotionFactor: Multiplier of the GroundMotionValues
        TimeStepIncrement: integration step size. Recomended value is 0.1 times the time step
        Damping: Damping value
        NewmarkGamma: Gamma value to implement the Newmark integrator.
        NewmarkBeta: Beta value to implement the Newmark integrator.
    Output:
       AlpacaGroundMotionOutput: Analysed Alpaca model.
       maxDisplacement: Maximum displacement of structure [mm].
       minDisplacement: Minimum displacement of structure [mm].
       """


import System
import os
import Grasshopper as gh

def InitializeGroundMotionAnalysis(AlpacaModel, TmaxAnalyses, GroundMotionDirection, GroundMotionValues, GroundMotionTimeStep, GroundMotionFactor, TimeStepIncrement, Damping, NewmarkGamma, NewmarkBeta):
    ghFilePath = ghenv.Component.Attributes.Owner.OnPingDocument().FilePath

    # delete file if already there
    workingDirectory = os.path.dirname(ghFilePath) 
    outputFileName = 'openSeesEarthQuakeAnalysisOutputWrapper.txt'

    for dirpath, dirnames, filenames in os.walk(workingDirectory):
        for filename in filenames:
            print(filename)
            if filename == outputFileName:
                file = os.path.join(dirpath,outputFileName)
                os.remove(file)


    ghFolderPath = os.path.dirname(ghFilePath)
    outputFolder = os.path.join(ghFolderPath,'assembleData')
    wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )



    earthQuakeSettings = []

    for item in GroundMotionValues:
        earthQuakeSettings.append( "GROUNDMOTIONVALUES {}".format(item) )

    for item in GroundMotionTimeStep:
        earthQuakeSettings.append( "GROUNDMOTIONTIMESTEP {}".format(item) )

    earthQuakeSettings.append( "GROUNDMOTIONDIRECTION {}".format(GroundMotionDirection) )
    earthQuakeSettings.append( "GROUNDMOTIONFACTOR {}".format(GroundMotionFactor) )
    earthQuakeSettings.append( "DAMPING {}".format(Damping) )
    earthQuakeSettings.append( "NEWMARKGAMMA {}".format(NewmarkGamma) )
    earthQuakeSettings.append( "NEWMARKBETA {}".format(NewmarkBeta) )
    earthQuakeSettings.append( "TMAXANALYSES {}".format(TmaxAnalyses) )
    earthQuakeSettings.append( "TIMESTEP {}".format(TimeStepIncrement) )


    earthQuakeSettingsFile = os.path.join( outputFolder,'earthQuakeSettingsFile.txt')

    with open(earthQuakeSettingsFile, 'w') as f:
        for item in earthQuakeSettings:
            f.write("%s\n" % item)


    userObjectFolder = gh.Folders.DefaultUserObjectFolder
    pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
    fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\EarthQuakeAnalysis\openSees_EarthQuakeAnalysis.py')


    fileName = '"' + fileName + '"'
    wrapperFile = '"' + wrapperFile + '"'
    earthQuakeSettingsFile = '"' + earthQuakeSettingsFile + '"'
    
    p = System.Diagnostics.Process()
    p.StartInfo.RedirectStandardOutput = False
    p.StartInfo.RedirectStandardError = True

    p.StartInfo.UseShellExecute = False
    p.StartInfo.CreateNoWindow = False
    
    p.StartInfo.FileName = pythonInterpreter
    p.StartInfo.Arguments = fileName + " " + wrapperFile + " " + earthQuakeSettingsFile
    p.Start()
    p.WaitForExit()
    
    
    msg = p.StandardError.ReadToEnd()
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)







    print("I have finished")

    ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
    ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py


    outputFile = os.path.join(outputFolder, outputFileName)

    with open(outputFile, 'r') as f:
        lines = f.readlines()
        nodeDispFilePath = lines[0]
        elementModalWrapper = eval( lines[1].strip() )
        nodeWrapper = eval( lines[2].strip() )
        maxDisplacement = lines[3]
        minDisplacement = lines[4]


    AlpacaGroundmotionOutput = [nodeDispFilePath, elementModalWrapper, nodeWrapper]

    return [AlpacaGroundmotionOutput, maxDisplacement, minDisplacement]

checkData = True

if not AlpacaModel:
    checkData = False
    msg = "input 'AlpacaModel' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if TmaxAnalyses is None:
    checkData = False
    msg = "input 'TmaxAnalyses' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if GroundMotionDirection is None:
    checkData = False
    msg = "input 'GroundMotionDirection' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if not GroundMotionValues:
    checkData = False
    msg = "input 'GroundMotionValues' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if not GroundMotionTimeStep:
    checkData = False
    msg = "input 'GroundMotionTimeStep' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if GroundMotionFactor is None:
    checkData = False
    msg = "input 'GroundMotionFactor' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if TimeStepIncrement is None:
    checkData = False
    msg = "input 'TimeStepIncrement' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if Damping is None:
    checkData = False
    msg = "input 'Damping' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if NewmarkGamma is None:
    checkData = False
    msg = "input 'NewmarkGamma' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if NewmarkBeta is None:
    checkData = False
    msg = "input 'NewmarkBeta' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    AlpacaGroundmotionOutput, maxDisplacement, minDisplacement = InitializeGroundMotionAnalysis(AlpacaModel, TmaxAnalyses, GroundMotionDirection, GroundMotionValues, GroundMotionTimeStep, GroundMotionFactor, TimeStepIncrement, Damping, NewmarkGamma, NewmarkBeta)