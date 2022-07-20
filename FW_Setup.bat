@echo off
if /I "%USERNAME%"=="TCoEAutoTest" (set varO=E:\Temp\temp.txt) else (set varO=%temp%/temp.txt)
set var1=%~dp0
cd\
cd %var1%\libs 
if /I "%USERNAME%"=="TCoEAutoTest" (
echo "TestIF"
call %WORKSPACE%\Setup\libs\setup.bat c:\pyetl) else (
call setup.bat c:\pyetl)
set var1=%~dp0
cd\
cd %var1%\libs
if /I "%USERNAME%"=="TCoEAutoTest" (
echo %WORKSPACE%\Setup\libs\dependency.bat
call %WORKSPACE%\Setup\libs\dependency.bat c:\pyetl\req.txt) else (
call dependency.bat c:\pyetl\req.txt)
echo.
set var1=%~dp0
cd\
echo Setting up project path...
cd %var1%\libs > %varO%
if /I "%USERNAME%"=="TCoEAutoTest" (cscript //nologo %WORKSPACE%\Setup\libs\projectpathsetup.vbs "%WORKSPACE%\Tests\" > %varO% ) else (
cscript //nologo projectpathsetup.vbs "%var1%" > %varO%)
echo Project path setup - [92mDone[0m
echo.
if /I "%USERNAME%"=="TCoEAutoTest" (del E:\Temp\temp.txt /f /q) else (del %temp%\temp.txt /f /q)

echo ====== Congratulations, below setups finished with just one click !! ======
echo.
echo 	             =^> [42mData-framework setup/upgrade[0m
echo 	             =^> [42mDependency management[0m
echo 	             =^> [42mFramework backup[0m
echo 	             =^> [42mEnviroment variable setup[0m
echo 	             =^> [42mPython project path setup[0m
echo.
pause
