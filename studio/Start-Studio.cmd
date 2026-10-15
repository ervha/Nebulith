@echo off
chcp 65001 > nul
setlocal
if exist "%~dp0build\NebulithStudio.jar" (
  start "" javaw -Dfile.encoding=UTF-8 -jar "%~dp0build\NebulithStudio.jar"
) else (
  echo ビルドが見つかりません。まずビルドを実行してください:
  echo .venv-audit\Scripts\python.exe tools\build_studio.py
  pause
)
