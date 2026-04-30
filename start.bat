@echo off
cd /d C:\Users\ASUS\hallucination-detector
call venv\Scripts\activate
start chrome http://127.0.0.1:5001/landing
python fast_app.py
pause