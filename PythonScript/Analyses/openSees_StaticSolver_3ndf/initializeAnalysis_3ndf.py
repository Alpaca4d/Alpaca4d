import System
import os
import Grasshopper


ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
#fileName = userObjectFolder + 'Alpaca\\core\\openSeesStaticSolver_Rev05_Debugging.py'
fileName = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\openSees_StaticSolver_3ndf\openSees_StaticSolver_3ndf.py'

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
    #shellOutputWrapper = eval( lines[4].strip() )



openSeesOutputWrapper = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoadWrapper ])

print( nodeDisplacementWrapper )
"""
with open(outputFile, 'r') as f:
    lines = f.readlines()
    nodeDisplacementWrapper = eval( lines[0].strip() )



openSeesOutputWrapper = ([nodeDisplacementWrapper])
"""