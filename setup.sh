#!/usr/bin/env bash
# ==============================================================================
# Cross-platform setup script for macOS and Linux
# Sets up a virtual environment, installs dependencies, and runs the pipeline.
# ==============================================================================

set -e

echo "=== [1/3] Setting up Python Virtual Environment (.venv) ==="
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created virtual environment in .venv/"
else
    echo "Existing virtual environment found in .venv/"
fi

# Activate virtual environment
source .venv/bin/activate

echo "=== [2/3] Installing Dependencies ==="
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "All dependencies installed successfully."

echo "=== [3/3] Running Data Analytics Pipeline ==="
python run_analysis.py

echo ""
echo "=============================================================================="
echo " Project execution complete!"
echo " To launch the interactive dashboard, run:"
echo "   source .venv/bin/activate"
echo "   streamlit run dashboard/app.py"
echo "=============================================================================="
