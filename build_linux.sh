#!/bin/bash
set -e

echo "Starting Linux build process..."

# 1. Create a clean virtual environment
echo "Creating virtual environment..."
python3 -m venv venv_build
source venv_build/bin/activate

# 2. Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# 3. Run PyInstaller
echo "Running PyInstaller..."
pyinstaller youtube_importer.spec --clean --noconfirm

echo "------------------------------------------------"
echo "Build complete! The executable is in 'dist/youtube_importer'"
echo "You can run it with: ./dist/youtube_importer"
echo "------------------------------------------------"

# 4. Cleanup
deactivate
# rm -rf venv_build
