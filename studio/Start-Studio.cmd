@echo off
setlocal
if exist "%~dp0build\NebulithStudio.jar" (
  javaw -jar "%~dp0build\NebulithStudio.jar"
) else (
  echo Build first: .venv-audit\Scripts\python.exe tools\build_studio.py
  pause
)
