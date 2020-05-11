import sys
import os
import openseespy.opensees as ops
import math
import time
import matplotlib.pyplot as plt


filename = sys.argv[1]
#filename = r'C:\Users\FORMAT\Desktop\EarthQuakeTest\assembleData\openSeesModel.txt'
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
    eleNodes = [ indexStart, indexEnd]
    
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

    if (eleType == 'ShellDKGQ') or (eleType == 'ShellDKGT'):

        ops.element( eleType , eleTag, *eleNodes, secTag)

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

ops.loadConst('-time', 0.0)	#maintain constant gravity loads and reset time to zero


#applying Dynamic Ground motion analysis
GMdirection = int(sys.argv[2])
GMfile = str(sys.argv[3])

GMfact = float(sys.argv[5])
dt = float(sys.argv[4])			# time step for input ground motion

ops.timeSeries('Path', 2, '-dt', dt, '-filePath', GMfile, '-factor', GMfact, '-prependZero')
ops.pattern('UniformExcitation', 2, GMdirection, '-accel', 2) 



Lambda = ops.eigen('-fullGenLapack', 1)[0] # eigenvalue mode 1
Omega = math.pow(Lambda, 0.5)


xDamp = float(sys.argv[6])				# 2% damping ratio
betaKcomm = 2 * (xDamp/Omega)
alphaM = 0.0				# M-prop. damping; D = alphaM*M	
betaKcurr = 0.0		# K-proportional damping;      +beatKcurr*KCurrent
betaKinit = 0.0 # initial-stiffness proportional damping      +beatKinit*Kini

ops.rayleigh(alphaM,betaKcurr, betaKinit, betaKcomm) # RAYLEIGH damping


nodeDispFilePath = os.path.join(workingDirectory, "DFree.out")
ops.recorder('Node', '-file', nodeDispFilePath ,'-time', '-node', '-dof', 1, 2, 3, 'disp')

ops.wipeAnalysis()
ops.constraints('Transformation')
ops.numberer('Plain')
ops.system('BandGeneral')
ops.test('EnergyIncr', 1e-12, 10)
ops.algorithm('Newton')

NewmarkGamma = float(sys.argv[7])	
NewmarkBeta = float(sys.argv[8])	
ops.integrator('Newmark', NewmarkGamma, NewmarkBeta)
ops.analysis('Transient')

# Perform the transient analysis
ok = 0
tCurrent = ops.getTime()
tAnalyses = float(sys.argv[9])			# End of the analyses
timeStep = dt * 0.1				# Increment 10% of the time series step?
print("starting Analyse")

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


    #u2 = ops.nodeDisp(2,1)
    #timer.append(tCurrent)
    #disp.append(u2)


'''
print("Ground Motion Analyses Finished")
ops.wipe()

plt.plot(timer, disp)
plt.ylabel('Horizontal Displacement of node 3 (in)')
plt.xlabel('Time (s)')

plt.show()
'''

time.sleep(2)


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
                               nodeWrapper])


length = len(filename)-len(inputName)
filefolder = filename[0:length]
outputFileName = filefolder + 'openSeesEarthQuakeAnalysisOutputWrapper.txt'

with open(outputFileName, 'w') as f:
    for item in openSeesModalOutputWrapper:
        f.write("%s\n" % item)

