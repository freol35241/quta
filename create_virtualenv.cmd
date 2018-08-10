@ECHO OFF

ECHO Creating virtual environment

py -3.5-32 -m venv venv


ECHO Installing packages

venv\Scripts\pip.exe install cython

venv\Scripts\pip.exe install -r requirements.txt

ECHO Finished

pause