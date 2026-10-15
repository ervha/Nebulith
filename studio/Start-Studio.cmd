@echo off
setlocal enabledelayedexpansion

:: Prefer the standalone package when available.
if exist "%~dp0build\dist\NebulithStudio.exe" (
  start "" "%~dp0build\dist\NebulithStudio.exe" %*
  exit /b 0
)

set "JAVA_EXE="

:: 1. Check system PATH for javaw
where javaw >nul 2>nul
if !errorlevel! equ 0 set "JAVA_EXE=javaw"

:: 2. Check Android Studio bundled JBR
if not defined JAVA_EXE (
  if exist "C:\Program Files\Android\Android Studio\jbr\bin\javaw.exe" (
    set "JAVA_EXE=C:\Program Files\Android\Android Studio\jbr\bin\javaw.exe"
  )
)

:: 3. Check JAVA_HOME
if not defined JAVA_EXE (
  if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\javaw.exe" (
      set "JAVA_EXE=%JAVA_HOME%\bin\javaw.exe"
    )
  )
)

:: 4. Fallback to console java if javaw is not found
if not defined JAVA_EXE (
  where java >nul 2>nul
  if !errorlevel! equ 0 set "JAVA_EXE=java"
)
if not defined JAVA_EXE (
  if exist "C:\Program Files\Android\Android Studio\jbr\bin\java.exe" (
    set "JAVA_EXE=C:\Program Files\Android\Android Studio\jbr\bin\java.exe"
  )
)

if not defined JAVA_EXE (
  echo [ERROR] Java runtime not found.
  echo Please install Java or Android Studio.
  pause
  exit /b 1
)

set "JAR_PATH=%~dp0build\NebulithStudio.jar"
if not exist "%JAR_PATH%" (
  echo [ERROR] Studio JAR not found at %JAR_PATH%
  echo Please build first: .venv-audit\Scripts\python.exe tools\build_studio.py
  pause
  exit /b 1
)

start "" "!JAVA_EXE!" -Dfile.encoding=UTF-8 -jar "%JAR_PATH%"
