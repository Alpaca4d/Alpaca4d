import sys
import os
import math
import time
from datetime import date
import openseespy.opensees as ops



ExpireDate = date(2020, 10, 1)
actualDay = date.today()
remainingDate = (ExpireDate - actualDay).days


if remainingDate < 0:
    sys.exit("the temporary license has expired. Please contact Alpaca Developer at alpaca4d@gmail.com to renew the license")


filename = sys.argv[1]
earthQuakeSettingsFile = sys.argv[2]

#filename = r'C:\Users\FORMAT\Desktop\groundMotion Test\assembleData\openSeesModel.txt'
#earthQuakeSettingsFile = r'C:\Users\FORMAT\Desktop\groundMotion Test\assembleData\earthQuakeSettingsFile.txt'


workingDirectory = os.path.split(filename)[0]
inputName = os.path.split(filename)[1]



with open(filename, 'r') as f:
    lines = f.readlines()
    openSeesNode = eval( lines[0].strip() )
    GeomTransf = eval( lines[1].strip() )
    openSeesBeam = eval( lines[2].strip() )
    openSeesSupport = eval( lines[3].strip() )
    openSeesNodeLoad = eval( lines[4].strip() )
    openSeesNodalMass = eval( lines[5].strip() )
    openSeesBeamLoad = eval( lines[6].strip() )
    openSeesMatTag = eval( lines[7].strip() )
    openSeesShell = eval(lines[8].strip() )
    openSeesSecTag = eval(lines[9].strip() )
    openSeesSolid = eval(lines[10].strip() )



oNodes = openSeesNode
gT = GeomTransf
openSeesBeam = openSeesBeam
oSupport = openSeesSupport
oNodeLoad = openSeesNodeLoad
oBeamLoad = openSeesBeamLoad
MatTag = openSeesMatTag
openSeesShell = openSeesShell
openSeesSecTag = openSeesSecTag
openSeesSolid = openSeesSolid
oMass = openSeesNodalMass



ops.wipe()

# MODEL
# ------------------------------

# Create ModelBuilder (with three-dimensions and 6 DOF/node):

ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
#model('basic', '-ndm', ndm, '-ndf', ndf=ndm*(ndm+1)/2)

##INPUT VARIABLE IS NODES CORDINATES OF STRUCTUR IN GRASSHOPER ##

## CREATE NODES IN OPENSEES ##


for i in range(0,len(oNodes)):
    nodeTag = oNodes[i][0] + 1
    ops.node( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] )

## CREATE MATERIAL IN OPENSEES ##

#print(MatTag) # to adjust

for item in MatTag:
    materialDimension = item[0].split("_")[1]
    materialType = item[0].split("_")[2]
    matTag = item[1][0]
    E = item[1][1][0]
    if materialDimension == 'uniaxialMaterial':
        ops.uniaxialMaterial(materialType, matTag , E)
    elif materialDimension == 'nDMaterial':
        ops.nDMaterial('ElasticIsotropic', matTag, E, 0.3)


for item in openSeesSecTag:
    typeSection = item[0].split("_")[1]
    secTag = int(item[1][0])
    E_mod = float( item[1][1][1][1] )
    nu = float( item[1][1][1][3] )
    h = float( item[1][1][0] )
    rho = float( item[1][1][1][4] )
    if typeSection == 'ElasticMembranePlateSection':
        ops.section(typeSection, secTag, E_mod, nu, h, rho)
        #print( 'ops.section( {0}, {1}, {2}, {3}, {4}, {5})'.format( typeSection, int(secTag), float(E_mod), float(nu), float(h), float(rho) ) )
## CREATE ELEMENT IN OPENSEES ##

# Define geometric transformation:
for i in range(0, len(gT)):
    tag = gT[i][0]
    vec = gT[i][1]
    ops.geomTransf('Linear', tag , *vec)


elementProperties = []

for n in range(0, len(openSeesBeam)):

    eleTag = openSeesBeam[n][1] + 1
    eleType = openSeesBeam[n][0]
    indexStart = openSeesBeam[n][2][0] + 1
    indexEnd = openSeesBeam[n][2][1] + 1
    eleNodes = [indexStart, indexEnd]
    
    A = openSeesBeam[n][3]
    E = openSeesBeam[n][4]
    G = openSeesBeam[n][5]
    Jxx = openSeesBeam[n][6] 
    Iy = openSeesBeam[n][7] 
    Iz = openSeesBeam[n][8]
    Avz = openSeesBeam[n][11]
    Avy = openSeesBeam[n][12]
    geomTag = int(openSeesBeam[n][9])
    massDens = openSeesBeam[n][10]
    orientVector = openSeesBeam[n][13]
    sectionGeomProperties = openSeesBeam[n][14]     # it is a list with [shape, base, height]
    matTag = openSeesBeam[n][15]
    color = openSeesBeam[n][16]   

    elementProperties.append([ eleTag, [eleType, E, G, A, Avz, Avy, Jxx, Iy, Iz, orientVector, sectionGeomProperties, matTag, color] ])


    if eleType is 'Truss':

        ops.element( eleType , eleTag , *[indexStart, indexEnd], float(A), matTag ) # TO CONTROL!!!
        

    elif eleType is 'ElasticTimoshenkoBeam':

        ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag , '-mass', massDens,'-lMass')

for item in openSeesShell:

    eleType = item[0]
    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    secTag = item[3]
    #print('secTag = ' + str(secTag))
    thick = item[4]
    #print('thick = ' + str(thick))
    color = item[5]

    elementProperties.append([ eleTag, [eleType, thick ,color] ])

    if (eleType == 'ShellMITC4') or (eleType == 'shellDKGT'):

        ops.element( eleType , eleTag, *eleNodes, secTag)
        #ops.element( eleType , eleTag, *eleNodes, secTag)

for item in openSeesSolid:

    eleType = item[0]
    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    matTag = item[3]
    #print('secTag = ' + str(secTag))
    force = item[4]
    #print( force)
    color = item[5]

    elementProperties.append([ eleTag, [eleType,color] ])

    if (eleType == 'bbarBrick') or (eleType == 'FourNodeTetrahedron'):

        ops.element( eleType , eleTag, *eleNodes, matTag, *force)                           
# transform elementproperties to  Dict to call the object by tag
elementPropertiesDict = dict(elementProperties)

# SUPPORT #

for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1

    ops.fix( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3], oSupport[i][4], oSupport[i][5], oSupport[i][6] )

## LOAD ##
## LOAD ##

# create TimeSeries
ops.timeSeries('Constant', 1)

# create a plain load pattern
ops.pattern('Plain', 1, 1)

## assemble load ##
for i in range(0, len(oNodeLoad)):

    nodetag = oNodeLoad[i][0] + 1
    Force = oNodeLoad[i][1]
    ops.load( nodetag, *Force )

elementLoad = []

for item in openSeesBeamLoad:
    eleTags = item[0] + 1
    Wy = item[1][0]
    Wz = item[1][1]
    Wx = item[1][2]
    loadType = item[2]
    #ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wy, Wz, Wx) we need to understand why is wrong
    ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wz, Wy, Wx)
    elementLoad.append([ eleTags, Wy, Wz, Wx, loadType] )



for i in range(len(oMass)):
    nodeTag = oMass[i][0] + 1
    massValues = oMass[i][1]
    ops.mass(nodeTag, *massValues)

# ------------------------------
# Start of analysis generation
# ------------------------------

ops.system("BandSPD")
ops.numberer('Plain')
# create constraint handler
ops.constraints("Transformation") # to allow Diaphgram constrain
# create integrator
ops.integrator("LoadControl",  1.0 )
# create algorithm
ops.algorithm("Newton")
# create analysis object
ops.analysis("Static")
# perform the analysis
ops.analyze(1)

ops.loadConst('-time', 0.0) #maintain constant gravity loads and reset time to zero



with open(earthQuakeSettingsFile, 'r') as f:
    earthQuakeSettingLines = f.readlines()



GroundMotionValues = []
GroundMotionTimeStep = []



for line in earthQuakeSettingLines:
    l = line.split()

    if l[0] == "GROUNDMOTIONVALUES":
        GroundMotionValues.append( l[1] )

    elif l[0] == "GROUNDMOTIONTIMESTEP":
        GroundMotionTimeStep.append( l[1] )

    elif l[0] == "GROUNDMOTIONDIRECTION":
        GMdirection = int(l[1])

    elif l[0] == "GROUNDMOTIONFACTOR":
        GMfact = float(l[1])

    elif l[0] == "DAMPING":
        damping = float(l[1])

    elif l[0] == "NEWMARKGAMMA":
        NewmarkGamma = float(l[1])

    elif l[0] == "NEWMARKBETA":
        NewmarkBeta = float(l[1])

    elif l[0] == "TMAXANALYSES":
        tAnalyses = float(l[1])

    elif l[0] == "TIMESTEP":
        timeStep = float(l[1])



print(f"GroundMotionValues = {GroundMotionValues}")
print(f'GroundMotionTimeStep = {GroundMotionTimeStep}')
print(f'GMfact = {GMfact}')
print(f"GMdirection = {GMdirection}")


# to make it more reliable
if len(GroundMotionValues) == 1:
    ops.timeSeries('Path', 2, '-filePath', GroundMotionValues[0], '-dt', float(GroundMotionTimeStep[0]), '-factor', GMfact, '-prependZero')

else:
# time series with values for time and force
    GroundMotionValues = [ float(item) for item in GroundMotionValues ]
    GroundMotionTimeStep = [ float(item) for item in GroundMotionTimeStep ]
    ops.timeSeries('Path', 2, '-values', *GroundMotionValues, '-time', *GroundMotionTimeStep, '-factor', GMfact)



ops.pattern('UniformExcitation', 2, GMdirection, '-accel', 2) 
Lambda = ops.eigen('-fullGenLapack', 1)[0] # eigenvalue mode 1
Omega = math.pow(Lambda, 0.5)



betaKcomm = 2 * (damping/Omega)
alphaM = 0.0                # M-prop. damping; D = alphaM*M 
betaKcurr = 0.0     # K-proportional damping;      +beatKcurr*KCurrent
betaKinit = 0.0 # initial-stiffness proportional damping      +beatKinit*Kini

ops.rayleigh(alphaM,betaKcurr, betaKinit, betaKcomm) # RAYLEIGH damping


nodeDispFilePath = os.path.join(workingDirectory, "DFree.out")

ops.recorder('Node', '-file', nodeDispFilePath ,'-time', '-node', '-dof', 1, 2, 3, 4, 5, 6, 'disp')



ops.wipeAnalysis()
ops.constraints('Transformation')
ops.numberer('Plain')
ops.system('BandGeneral')

ops.algorithm('Newton')
ops.test('NormDispIncr', 1e-8, 1000, 1)

 
ops.integrator('Newmark', NewmarkGamma, NewmarkBeta)

ops.analysis('Transient')


# Perform the transient analysis
ok = 0
tCurrent = ops.getTime()



print('--------------------------------------------------------')
print('                       Alpaca4D                         ')
print('                                                        ')
print('--------------------------------------------------------')
print('                  Analyses has started                  ')
print('--------------------------------------------------------')


timer = []
disp = []

while ok == 0 and tCurrent < tAnalyses:
    
    ok = ops.analyze(1, timeStep)
    
    # if the analysis fails try initial tangent iteration
    if ok != 0:
        print("regular newton failed .. lets try an initail stiffness for this step")
        ops.test('NormDispIncr', 1.0e-12,  10)
        ops.algorithm('ModifiedNewton', '-initial')
        ok =analyze( 1, timeStep)
        if ok == 0:
            print("that worked .. back to regular newton")
        ops.test('NormDispIncr', 1.0e-12,  10 )
        ops.algorithm('Newton')

    tCurrent = ops.getTime()
    #print(f"Analyses step: {tCurrent}")


print("Ground Motion Analyses Finished")


#----------------------------------------------
# THIS PART HAS TO BE DECIDE WITH DOMENICO
# SOME USEFULL OUTPUT FOR FUTURE OPTIMISATION


## some problem happening here

dt = []
displacement = []

with open(nodeDispFilePath, 'r') as f:
    lines = f.readlines()
    for n, line in enumerate(lines):
        if (n % 10) == 0:
            line = line.strip().split(" ")
            dt.append( line[0] )
            displacementTemp = line[1:]
            n = 6
            displacementTime = [displacementTemp[i:i + n] for i in range(0, len(displacementTemp), n)]
            displacement.append(displacementTime)
        else:
            break

# TAKING THE VALUE IN A SINGLE DIRECTION BUT WE SHOULD DO IT FOR VECTOR



maximum = []
for values in displacement:
    for value in values:
        maximum.append(float(value[GMdirection-1]))

maximum.sort()
maxDisplacement = maximum[-1]
minDisplacement = maximum[0]



elementOutputWrapper = []

elementTagList = ops.getEleTags()

for elementTag in elementTagList:
    elementOutputWrapper.append([ elementTag, ops.eleNodes(elementTag), elementPropertiesDict.setdefault(elementTag) ])

elementOutputWrapper = elementOutputWrapper
## nodal coord
nodeWrapper = []
for nodeTag in ops.getNodeTags():
    Node = ops.nodeCoord( nodeTag )
    nodeWrapper.append([ nodeTag, Node ]) # cordinate nodo
#-----------------------------------------------------


openSeesModalOutputWrapper = ([nodeDispFilePath,
                               elementOutputWrapper,
                               nodeWrapper,
                               maxDisplacement,
                               minDisplacement])


outputFileName = os.path.join(workingDirectory, 'openSeesEarthQuakeAnalysisOutputWrapper.txt')


print(outputFileName)
with open(outputFileName, 'w') as f:
    for item in openSeesModalOutputWrapper:
        f.write("%s\n" % item)

ops.wipe()