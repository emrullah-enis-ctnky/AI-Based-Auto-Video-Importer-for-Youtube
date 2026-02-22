import subprocess
import sys
import os
import importlib.metadata
from .logger import logger

# PyPI name mappings
# Sometimes PyPI package names in requirements.txt (e.g. google-api-python-client)
# don't perfectly match the distribution name registered under importlib.
# importlib generally normalizes dashes to dashes, but maps differ mostly on imports, not package installs.
# So importlib.metadata.version("google-api-python-client") usually works!

def get_requirements():
    """
    Reads the requirements.txt file from the project root.
    """
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")
    if not os.path.exists(requirements_path):
        logger.warning(f"requirements.txt bulunamadı: {requirements_path}")
        return []
    
    with open(requirements_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def check_and_install_dependencies():
    """
    Checks if required packages are installed, and installs them if missing.
    """
    # PyInstaller executable'ı içindeysek bağımlılık kontrolü/kurulumu yapma
    if getattr(sys, 'frozen', False):
        return

    logger.info("Bağımlılıklar kontrol ediliyor...")
    requirements = get_requirements()
    
    if not requirements:
        return

    missing_packages = []
    for requirement in requirements:
        # Extract package name (handle versions like package==1.0.0)
        package_name = requirement.split("==")[0].split(">=")[0].split("<=")[0].strip()
        
        try:
            importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            missing_packages.append(requirement)

    if missing_packages:
        logger.warning(f"Eksik paketler bulundu: {', '.join(missing_packages)}")
        logger.info("Eksik paketler yükleniyor, lütfen bekleyin...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            logger.success("Tüm bağımlılıklar başarıyla yüklendi.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Paket yükleme sırasında hata oluştu: {str(e)}")
            sys.exit(1)
    else:
        logger.debug("Tüm bağımlılıklar zaten yüklü.")

if __name__ == "__main__":
    check_and_install_dependencies()
