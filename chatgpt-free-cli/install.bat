@echo off
echo Installing ChatGPT CLI OS-Independent...
pip install -r requirements.txt
pip install -e .
echo Installation complete! Try running: chatgpt --help
pause
