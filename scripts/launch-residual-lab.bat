@echo off
setlocal EnableExtensions
title residual-lab chat

REM One-click launcher for DESKTOP-T4K7H74.
REM Copy this file (or a shortcut to it) onto your Desktop / Public Desktop.
REM Working dir is always the desk clone, not wherever the .bat lives.

set "LAB_ROOT=C:\Users\bocst\projects\residual-lab"
if not exist "%LAB_ROOT%\pyproject.toml" (
  echo residual-lab not found at %LAB_ROOT%
  echo Clone or unzip the lab there, then double-click this launcher again.
  pause
  exit /b 1
)
cd /d "%LAB_ROOT%"

REM Gradio opens the real URL. If 43123 is busy, the next free port is used
REM and written to out\ui-url.txt — do not hard-code 43123 in the browser.
set "RESIDUAL_LAB_OPEN_BROWSER=1"
set "PYTHONUNBUFFERED=1"

echo Starting residual-lab chat from %CD%
echo Browser should open to http://127.0.0.1:43123 (or the next free port).

REM Backup browser open after the UI writes out\ui-url.txt.
start "" /b powershell -NoProfile -Command "Start-Sleep -Seconds 4; $u='http://127.0.0.1:43123'; if (Test-Path 'out\ui-url.txt') { $lines=(Get-Content 'out\ui-url.txt'); if ($lines) { $u=$lines[0].Trim() } }; Start-Process $u"

py -3 -m residual_lab ui --host 127.0.0.1 --port 43123
if errorlevel 1 (
  echo.
  echo Failed. From %LAB_ROOT% run:  py -3 -m pip install -e .
  pause
)
endlocal
