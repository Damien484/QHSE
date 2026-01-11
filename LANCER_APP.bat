@echo off
REM Script de lancement simplifié pour Windows
echo ============================================================
echo Lancement de l'application DUERP
echo ============================================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Lancer l'application
python run.py

pause
