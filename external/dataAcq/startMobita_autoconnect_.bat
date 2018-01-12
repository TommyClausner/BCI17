set batdir=%~dp0
rem Search for the buffer executable
if exist "%batdir%buffer\bin\win32\mobita2ft.exe" ( set buffexe="%batdir%buffer\bin\win32\mobita2ft.exe" )
if exist "%batdir%buffer\win32\mobita2ft.exe" ( set buffexe="%batdir%buffer\win32\mobita2ft.exe" )
if exist "%batdir%mobita2ft.exe" ( set buffexe="%batdir%mobita2ft.exe" )

@Echo off
echo Select which Mobita to connect to:
echo =============
echo.
echo 1) 0130018
echo 2) 0130019
echo 3) 0120009
echo 4) 0120008
echo 5) 0120016
echo 6) 0120035
echo.
set /p num=type number:
if "%num%"=="1" set mob=0130018
if "%num%"=="2" set mob=0130019
if "%num%"=="3" set mob=0120009
if "%num%"=="4" set mob=0120008
if "%num%"=="5" set mob=0120016
if "%num%"=="6" set mob=0120035

set ssid="Mobita_071%mob%"
 
for /f "tokens=1* delims=: " %%a in ('netsh wlan show interfaces') do if %%a == Name set activeAdapter=%%b

:findNetwork
echo Searching for mobita
rem specify interface here?
rem for /f "tokens=1* delims=: " %%a in ('netsh wlan show networks') do if %%a == %ssid% set networkFound = 1

rem if NOT %networkFound% == 1 ( 
rem	echo Network %ssid% not found. Retrying in 3 sec
rem	ping 127.0.0.1 -n 3 > nul
rem	goto :findNetwork
rem )


netsh wlan add profile filename="%batdir%mobita_wifi_profile.xml" interface="%activeAdapter%"
netsh wlan set profileparameter mobita_connection SSIDname="%ssid%" keyMaterial="MOBITA%mob%" connectionType=ibss
echo =============
echo "Connecting to %ssid% using %activeAdapter%"

rem Weird windows hack to sleep for 2 secs to allow the buffer server to start
ping 127.0.0.1 -n 5 > nul

netsh wlan connect name=mobita_connection ssid="%ssid%" interface="%activeAdapter%"

rem Weird windows hack to sleep for 2 secs to allow the buffer server to start
ping 127.0.0.1 -n 3 > nul

start /b "mobita2ft" %buffexe% 10.11.12.13:4242 localhost:1972 50 4

