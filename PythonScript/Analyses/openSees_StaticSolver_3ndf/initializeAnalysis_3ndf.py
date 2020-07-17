import System
import os
import Grasshopper


ghFilePath = ghenv.LocalScope.ghdoc.Path

# delete file if already there
workingDirectory = os.path.dirname(ghFilePath) 
outputFileName = 'openSeesOutputWrapper.txt'

for dirpath, dirnames, filenames in os.walk(workingDirectory):
    for filename in filenames:
        if filename == outputFileName:
            file = os.path.join(dirpath,outputFileName)
            os.remove(file)
            #print("I removed the file")



ghFolderPath = os.path.dirname(ghFilePath)
outputFolder = os.path.join(ghFolderPath,'assembleData')
wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )


userObjectFolder = gh.Folders.DefaultUserObjectFolder
fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\LinearAnalyses\openSees_StaticSolver_3ndf.py')

fileName = '"' + fileName + '"'
wrapperFile = '"' + wrapperFile + '"'


staticAnalyses_3ndf = System.Diagnostics.ProcessStartInfo(fileName)
staticAnalyses_3ndf.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden
staticAnalyses_3ndf.Arguments = wrapperFile
process = System.Diagnostics.Process.Start(staticAnalyses_3ndf)
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
    #shellOutputWrapper = eval( lines[4].strip() )



AlpacaStaticOutput = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoadWrapper ])

