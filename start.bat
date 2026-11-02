@echo off
title AutoViral AI Studio
echo ==============================================
echo       Starting AutoViral AI Studio...
echo ==============================================
echo Opening in your browser...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run app.py
pause
