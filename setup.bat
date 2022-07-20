@echo off
if /I "%USERNAME%"=="TCoEAutoTest" (set varO=E:\Temp\temp.txt) else (set varO=%temp%/temp.txt)
echo Setting up environment variable...
setx PYTHONPATH %1 > %varO%
echo Environment variable setup - [92mDone[0m
echo.
if exist %1 (
echo Starting backup of %1...
set bkp=c:\pybkp\pyetl_bkp
if exist %bkp% ( del %bkp% /f /s /q )
xcopy %1 %bkp% /e /i /y /s > %varO%
echo Backup of %1 taken at %bkp% - [92mDone[0m
echo.
)
if not exist %1 (
echo Cloning data framework...
cd\
cd C:\
if /I "%USERNAME%"=="TCoEAutoTest" (
git clone ssh://git@bitbucket.sunlifecorp.com/scm/tcoeicas/tcoe-data-test-automation-fw.git %1 > %varO% ) else (
git clone https://bitbucket.sunlifecorp.com/scm/tcoeicas/tcoe-data-test-automation-fw.git %1 > %temp%\temp.txt)
) else (
echo Updating data framework...
cd /d %1
git fetch --all > %varO%
git reset --hard origin/master > %varO%
)
echo Framework Setup/upgrade - [92mDone[0m
echo.
ping 127.0.0.1 -n 0 > %varO%
if /I "%USERNAME%"=="TCoEAutoTest" (del E:\Temp\temp.txt /f /q) else (del %temp%\temp.txt /f /q)


