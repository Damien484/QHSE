@echo off
REM Nettoyer le cache Python et relancer l'application
echo ============================================================
echo Nettoyage du cache Python
echo ============================================================
echo.

REM Supprimer tous les __pycache__
echo Suppression des dossiers __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Supprimer les fichiers .pyc
echo Suppression des fichiers .pyc...
del /s /q *.pyc 2>nul

echo.
echo Cache nettoyé !
echo.
echo ============================================================
echo Lancement de l'application DUERP
echo ============================================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Lancer l'application
python run.py

pause
