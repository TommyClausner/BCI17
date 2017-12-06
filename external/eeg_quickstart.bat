setlocal enabledelayedexpansion
set batdir=%~dp0
cd %batdir%

set dataacq=%1
if "%dataacq%"=="" ( 
set dataacq=mobita
)
set sigproc=%2

echo Starting the java buffer server \(background\)
rem wmic process call create "dataAcq/startJavaNoSaveBuffer.bat" | find "ProcessId"
start dataAcq\startJavaBuffer.bat

rem Weird windows hack to sleep for 2 secs to allow the buffer server to start
ping 127.0.0.1 -n 3 > nul


echo Starting the data acquisation device %dataacq% \(background\)
if "%dataacq%"=="mobita" (
  start dataAcq\startMobita.bat localhost 2
) else if "%dataacq%"=="biosemi" (
  start dataAcq\startBiosemi.bat
) else (
  echo Dont recognise the eeg device type
)
rem dataacqpid=$!

if defined sigproc (
    if "%sigproc%"=="1" (
    echo Starting the default signal processing function \(background\)
    start  .\matlab\signalProc\startSigProcBuffer.bat
    rem sigprocpid=$!
    rem sigprocpid = %%G
    rem echo %sigprocpid%
    
    )
)




rem This is added to find the PID!
@echo off &setlocal
title EEG_quickstart

setlocal EnableDelayedExpansion
set "uid="
for /l %%i in (1 1 128) do (set /a "bit=!random!&1" &set "uid=!uid!!bit!")
for /f "tokens=2 delims==" %%i in (
  'WMIC Process WHERE "Name='cmd.exe' AND CommandLine LIKE '%%!uid!%%'" GET ParentProcessID /value'
) do for /f %%j in ("%%i") do (endlocal &set "PID=%%j")
for /f "tokens=1* delims=:" %%i in ('tasklist /fo "LIST" /fi "PID eq %PID%" /v') do (
  for /f "tokens=*" %%k in ("%%j") do set "WindowTitle=%%k"
)


echo PID         = %PID%
echo WindowTitle = "%WindowTitle%"

>pids.txt echo %PID%


rem From here it is jason's script again


echo Starting the event viewer
dataAcq\startJavaEventViewer.bat

rem Cleanup all the processes we started
rem TODO: make this work, getting the pid of started process seems very hard in windows....
rem taskkill /pid %bufferpid%
rem taskkill /pid %dataacqpid%
rem taskkill /pid %sigprocpid%
