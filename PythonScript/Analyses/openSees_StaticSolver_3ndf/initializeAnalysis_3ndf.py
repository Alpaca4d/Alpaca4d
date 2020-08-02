import System
import os
import Grasshopper as gh


ghFilePath = ghenv.Component.Attributes.Owner.OnPingDocument().FilePath

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
pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\LinearAnalyses\openSees_StaticSolver_3ndf.py')
    
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

