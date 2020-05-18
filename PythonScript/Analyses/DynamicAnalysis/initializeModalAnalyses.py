import System
import os
import Grasshopper


ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name


# delete file if already there
workingDirectory = os.path.dirname(ghFilePath) 
outputFileName = 'openSeesModalOutputWrapper.txt'

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
fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\DynamicAnalysis\openSees_ModalSolver.py'


modalAnalyses = System.Diagnostics.ProcessStartInfo(fileName)
modalAnalyses.Arguments = wrapperFile + " " + str(numEigenvalues)
process = System.Diagnostics.Process.Start(modalAnalyses)
System.Diagnostics.Process.WaitForExit(process)

## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py

outputFile = outputPath + '\\openSeesModalOutputWrapper.txt'

with open(outputFile, 'r') as f:
    lines = f.readlines()
    nodeModalDispWrapper = eval( lines[0].strip() )
    elementModalWrapper = eval( lines[1].strip() )
    period = eval( lines[2].strip() )
    frequency = eval( lines[3].strip() )



openSeesOutputWrapper = ([nodeModalDispWrapper,
                        elementModalWrapper,
                        period,
                        frequency])