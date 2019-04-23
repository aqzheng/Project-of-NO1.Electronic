@echo off
set /a num=%1,num2=2
shift /0
:parallel
if %num% leq %num2% (
    goto end
)
set str=%1
set /a num=%num%-1
if not exist "%str%" (
    goto end
)
start /min cmd /c call single.bat %str%
shift /0
goto parallel
:end

set str=%1
if exist "%str%" (
    start /wait /min cmd /c call single.bat %str%
)
shift /0

set str=%1
if exist "%str%" (
    start /wait /min cmd /c call single.bat %str%
)
