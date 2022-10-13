@ECHO OFF
set PATH=%~dp0\opensees-bin;%~dp0\tcl\bin;%~dp0\hdf5;%~dp0\bin;%~dp0\plugins;%PATH%
IF [%2] == [] (
	ECHO "RUNNING AS SEQUENTIAL"
	OpenSeesSP.exe %1
)
IF NOT [%2] == [] (
	ECHO "RUNNING AS PARALLEL"
	mpiexec.hydra.exe -n %2 OpenSeesSP.exe %1
)
