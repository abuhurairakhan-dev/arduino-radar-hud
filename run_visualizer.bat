@echo off
title NEXUS-7 Ultrasonic Radar HUD Visualizer
echo ========================================================
echo    NEXUS-7 TACTICAL ULTRASONIC RADAR HUD SYSTEM
echo ========================================================
echo Starting Sci-Fi Radar Visualizer in Python Pygame...
python radar_scifi_hud.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo If Python or packages are missing, run:
    echo   pip install -r requirements.txt
    echo.
    pause
)

