@echo off
chcp 65001 > nul
cd /d "%~dp0"
title Installation - Sticky Note IA

echo.
echo  Sticky Note IA - Installation
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  Python n'est pas installe.
    echo  Telecharge-le sur : https://www.python.org/downloads/
    echo  Coche "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)

echo  Python detecte
echo.
echo  Installation des librairies...
pip install -r requirements.txt
if errorlevel 1 (
    echo  L'installation a echoue. Verifie ta connexion internet.
    pause
    exit /b 1
)

echo.
echo  Librairies installees
echo.
echo  Verification d'Ollama...

where ollama >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Ollama n'est pas installe sur ce PC.
    echo  Installe-le ici : https://ollama.com/download
    echo  Une fois installe, relance ce fichier.
    echo.
    goto fin
)

echo  Ollama detecte
echo.
echo  Telechargement du modele IA phi3:mini (environ 2Go)...
ollama pull phi3:mini
echo.
echo  Modele IA pret !

:fin
echo.
echo  Installation terminee !
echo  Lance l'app avec :  python main.py
echo.
pause
