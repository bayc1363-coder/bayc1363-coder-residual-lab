@echo off
setlocal EnableExtensions
title Copy residual-lab shortcut to Desktop

set "LAB_ROOT=C:\Users\bocst\projects\residual-lab"
set "LAUNCHER=%LAB_ROOT%\scripts\launch-residual-lab.bat"
if not exist "%LAUNCHER%" set "LAUNCHER=%~dp0launch-residual-lab.bat"
if not exist "%LAUNCHER%" (
  echo Could not find launch-residual-lab.bat
  pause
  exit /b 1
)

set "USER_DESK=%USERPROFILE%\Desktop"
set "PUBLIC_DESK=%PUBLIC%\Desktop"
set "BAT_NAME=Launch residual-lab.bat"

if exist "%USER_DESK%" (
  copy /Y "%LAUNCHER%" "%USER_DESK%\%BAT_NAME%" >nul
  echo Copied to %USER_DESK%\%BAT_NAME%
)
if exist "%PUBLIC_DESK%" (
  copy /Y "%LAUNCHER%" "%PUBLIC_DESK%\%BAT_NAME%" >nul
  echo Copied to %PUBLIC_DESK%\%BAT_NAME%
)

REM .lnk on the user Desktop pointing at the repo launcher (cwd = lab root).
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $desk = [Environment]::GetFolderPath('Desktop'); ^
   $lnk = $ws.CreateShortcut((Join-Path $desk 'residual-lab chat.lnk')); ^
   $lnk.TargetPath = '%LAUNCHER%'; ^
   $lnk.WorkingDirectory = '%LAB_ROOT%'; ^
   $lnk.WindowStyle = 1; ^
   $lnk.Description = 'residual-lab chat (local Gradio)'; ^
   $lnk.Save(); ^
   Write-Host ('Shortcut: ' + (Join-Path $desk 'residual-lab chat.lnk'))"

if exist "%PUBLIC_DESK%" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
     $lnk = $ws.CreateShortcut('%PUBLIC_DESK%\residual-lab chat.lnk'); ^
     $lnk.TargetPath = '%LAUNCHER%'; ^
     $lnk.WorkingDirectory = '%LAB_ROOT%'; ^
     $lnk.WindowStyle = 1; ^
     $lnk.Description = 'residual-lab chat (local Gradio)'; ^
     $lnk.Save(); ^
     Write-Host ('Public Desktop shortcut: %PUBLIC_DESK%\residual-lab chat.lnk')"
)

echo.
echo Double-click "residual-lab chat" or "Launch residual-lab.bat" on the Desktop.
pause
endlocal
