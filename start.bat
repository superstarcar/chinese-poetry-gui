@echo off
python launcher.py
if errorlevel 1 (
    echo Failed to start. Please make sure Python 3.6+ is installed.
    pause
)