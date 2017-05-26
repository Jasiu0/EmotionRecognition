@echo off

:: Sprawdzenie istnienia zainstalowanego pythona
echo.
echo Checking Python Module
python --version 2>NUL
if errorlevel 1 echo Python installed:                 Fail && exit /b
echo Python installed:               Pass

Python DrawPlot.py 
echo.
pause