@echo off
echo ========================================
echo   Push to GitHub - chinese-poetry-gui
echo ========================================
echo.
echo Step 1: Go to https://github.com/new
echo Step 2: Create repository named: chinese-poetry-gui
echo Step 3: Do NOT initialize with README
echo Step 4: Press any key here to continue...
pause
echo.
echo Pushing to GitHub...
git push -u origin master
echo.
if errorlevel 1 (
    echo Push failed! Please check:
    echo - GitHub repository exists
    echo - You have access permissions
    echo - Your git credentials are configured
) else (
    echo Success! View at: https://github.com/superstarcar/chinese-poetry-gui
)
pause