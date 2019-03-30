@ECHO OFF

ECHO Creating virtual environment

py -3-32 -m venv venv


ECHO Installing packages

venv\Scripts\pip.exe install cython

venv\Scripts\pip.exe install -r requirements.txt
venv\Scripts\pip.exe install -r requirements_dev.txt

ECHO Finished

pause