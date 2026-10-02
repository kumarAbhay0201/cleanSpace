@echo off
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --noconsole --name CleanSpace --add-data "frontend;frontend" --exclude-module pytest --exclude-module IPython --exclude-module numpy launcher.py
echo.
echo Built: dist\CleanSpace.exe
