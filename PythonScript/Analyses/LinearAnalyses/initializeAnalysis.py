import System
import os
import Grasshopper


ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

#userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\LinearAnalyses\openSees_StaticSolver.py'


staticAnalyses = System.Diagnostics.ProcessStartInfo(fileName)
staticAnalyses.Arguments = wrapperFile
process = System.Diagnostics.Process.Start(staticAnalyses)
System.Diagnostics.Process.WaitForExit(process)

## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py

outputFile = outputPath + '\\openSeesOutputWrapper.txt'

with open(outputFile, 'r') as f:
    lines = f.readlines()
    nodeDisplacementWrapper = eval( lines[0].strip() )
    reactionWrapper = eval( lines[1].strip() )
    elementOutputWrapper = eval( lines[2].strip() )
    elementLoadWrapper = eval( lines[3].strip() )
    eleForceWrapper = eval( lines[4].strip() )
    nodalForceWrapper = eval( lines[5].strip() )


openSeesOutputWrapper = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoadWrapper,
                        eleForceWrapper,
                        nodalForceWrapper])