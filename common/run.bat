@echo off
cls
 
title mg-soundboard Launcher

echo ================================================================
echo                    MG-SOUNDBOARD LAUNCHER
echo ================================================================

echo.
echo WARNING: Do not close this launcher window while the application is running.
echo.

echo To start the mg-soundboard application, Python will be executed.
echo Please wait...

python mg-soundboard_main.py

echo.
echo ================================================================
echo                    MG-SOUNDBOARD TERMINATED
echo ================================================================
echo.
echo The mg-soundboard application has been closed. You can close this window.
pause
