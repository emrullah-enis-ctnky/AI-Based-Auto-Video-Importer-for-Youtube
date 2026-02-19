@echo off
echo Starting Windows build process...

:: 1. Create a clean virtual environment
echo Creating virtual environment...
python -m venv venv_build
call venv_build\Scripts\activate

:: 2. Install dependencies
echo Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: 3. Run PyInstaller
echo Running PyInstaller...
pyinstaller youtube_importer.spec --clean --noconfirm

echo ------------------------------------------------
echo Build complete! The executable is in 'dist\youtube_importer.exe'
echo ------------------------------------------------
pause
deactivate
