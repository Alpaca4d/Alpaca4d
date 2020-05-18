import System
import os
import Grasshopper


ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name

# delete file if already there
workingDirectory = os.path.dirname(ghFilePath) 
outputFileName = 'openSeesEarthQuakeAnalysisOutputWrapper.txt'

for dirpath, dirnames, filenames in os.walk(workingDirectory):
    for filename in filenames:
        print(filename)
        if filename == outputFileName:
            file = os.path.join(dirpath,outputFileName)
            os.remove(file)


folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

#userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\EarthQuakeAnalysis\openSees_EarthQuakeAnalysis.py'


EarthQuakeAnalysis = System.Diagnostics.ProcessStartInfo(fileName)
EarthQuakeAnalysis.Arguments = wrapperFile + " " + str(GroundMotionDirection) + " " + str(GroundMotionFile) + " " + str(GroundMotionTimeStep) + " " + str(GroundMotionfactor) + " " + str(Damping) + " " + str(NewmarkGamma) + " " + str(NewmarkBeta)+ " " + str(TmaxAnalyses)
process = System.Diagnostics.Process.Start(EarthQuakeAnalysis)
System.Diagnostics.Process.WaitForExit(process)



print("I have finished")

## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py


outputFile = outputPath + '\\openSeesEarthQuakeAnalysisOutputWrapper.txt'

with open(outputFile, 'r') as f:
    lines = f.readlines()
    nodeDispFilePath = lines[0]
    elementModalWrapper = eval( lines[1].strip() )
    nodeWrapper = eval( lines[2].strip() )
    maxDisplacement = lines[3]
    minDisplacement = lines[4]


openSeesOutputWrapper = [nodeDispFilePath, elementModalWrapper, nodeWrapper]