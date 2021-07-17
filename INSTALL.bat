@echo off
python --version > find /i "Python 3.8" >nul 2>&1
if errorlevel 1 (
   echo Wrong or no version of Python found :/
   echo Try downloading and installing the right version of Python from
   echo "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe"
   echo Restart your computer afterwards!
) else (
   python --version
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
)
@pause