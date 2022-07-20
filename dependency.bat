@echo off
echo Setting up environment...
if /I "%USERNAME%"=="TCoEAutoTest" (set varO=E:\Temp\temp.txt) else (set varO=%temp%/temp.txt)
cd\
if /I "%USERNAME%"=="TCoEAutoTest" (
python.exe -m pip install --index https://tcoeautotest:AP4M3C54DkFSBAtfn5VHA7YuV44HxXjFHAmpsP@artifactory.sunlifecorp.com/artifactory/api/pypi/pypi-virtual/simple --trusted-host artifactory.sunlifecorp.com -r %1 --user  > %varO% ) else (
python.exe -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r %1 --user  > %varO% )
ping 127.0.0.1 -n 0 > %varO%

echo Environment setup - [92mDone[0m
if /I "%USERNAME%"=="TCoEAutoTest" (del E:\Temp\temp.txt /f /q) else (del %temp%\temp.txt /f /q)
