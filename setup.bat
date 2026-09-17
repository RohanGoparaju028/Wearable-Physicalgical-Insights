@echo off
REM ==============================================================================
REM Cross-platform setup script for Windows (Command Prompt / PowerShell)
REM Sets up a virtual environment, installs dependencies, and runs the pipeline.
REM ==============================================================================

echo === [1/3] Setting up Python Virtual Environment (.venv) ===
if not exist ".venv" (
    python -m venv .venv
    echo Created virtual environment in .venv\
) else (
    echo Existing virtual environment found in .venv\
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo === [2/3] Installing Dependencies ===
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo All dependencies installed successfully.

echo === [3/3] Running Data Analytics Pipeline ===
python run_analysis.py

echo.
echo ==============================================================================
echo  Project execution complete!
echo  To launch the interactive dashboard, run:
echo    call .venv\Scripts\activate.bat
echo    streamlit run dashboard\app.py
echo ==============================================================================
pause
