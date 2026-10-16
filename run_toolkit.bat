@echo off
title Atelier Yumia - Italian Translation Toolkit
chcp 65001 >nul
cd /d "%~dp0"
python src\yumia_cli.py
pause
