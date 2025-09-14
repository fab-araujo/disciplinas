@echo off
setlocal
cd /d "%~dp0"

if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install pygame>=2.5.2

python main.py
