@echo off
REM Script d'installation de l'automatisation nocturne pour FC Palestina
REM Ce script configure Windows Task Scheduler pour exécuter les mises à jour chaque nuit

echo ===============================================
echo    CONFIGURATION AUTOMATISATION NOCTURNE
echo         FC Palestina - Vinted Reviews
echo ===============================================
echo.

REM Obtenir le répertoire actuel
set SCRIPT_DIR=%~dp0
set BASE_DIR=%SCRIPT_DIR%..
set PYTHON_SCRIPT=%SCRIPT_DIR%nightly_automation.py

echo Répertoire de base : %BASE_DIR%
echo Script Python      : %PYTHON_SCRIPT%
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Vérifier que le script Python existe
if not exist "%PYTHON_SCRIPT%" (
    echo ERREUR: Script nightly_automation.py introuvable
    echo Chemin attendu: %PYTHON_SCRIPT%
    pause
    exit /b 1
)

echo ✅ Script d'automatisation trouvé
echo.

REM Créer la tâche programmée Windows
echo 🕐 Configuration de la tâche programmée...
echo Cette tâche s'exécutera chaque jour à 2h00 du matin

REM Supprimer l'ancienne tâche si elle existe
schtasks /delete /tn "FCPalestina_NightlyUpdate" /f >nul 2>&1

REM Créer la nouvelle tâche
schtasks /create ^
    /tn "FCPalestina_NightlyUpdate" ^
    /tr "python \"%PYTHON_SCRIPT%\"" ^
    /sc daily ^
    /st 02:00 ^
    /sd %date% ^
    /ru "SYSTEM" ^
    /rl HIGHEST ^
    /f

if errorlevel 1 (
    echo.
    echo ⚠️  Impossible de créer la tâche avec les privilèges SYSTEM
    echo Tentative avec l'utilisateur actuel...
    
    REM Essayer avec l'utilisateur actuel
    schtasks /create ^
        /tn "FCPalestina_NightlyUpdate" ^
        /tr "python \"%PYTHON_SCRIPT%\"" ^
        /sc daily ^
        /st 02:00 ^
        /sd %date% ^
        /f
    
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de la tâche programmée
        echo Vous pouvez la créer manuellement dans le Planificateur de tâches Windows
        echo.
        echo Paramètres suggérés:
        echo   Nom: FCPalestina_NightlyUpdate
        echo   Action: python "%PYTHON_SCRIPT%"
        echo   Déclencheur: Quotidien à 2h00
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Tâche programmée créée avec succès
echo.

REM Afficher les informations de la tâche
echo 📋 Informations de la tâche:
schtasks /query /tn "FCPalestina_NightlyUpdate" /fo table

echo.
echo ===============================================
echo            CONFIGURATION TERMINÉE
echo ===============================================
echo.
echo ✅ L'automatisation nocturne est maintenant configurée
echo 🕐 Exécution programmée : chaque jour à 2h00
echo 📋 Nom de la tâche : FCPalestina_NightlyUpdate
echo 📝 Logs disponibles dans : %BASE_DIR%\automation.log
echo.
echo 🛠️  COMMANDES UTILES:
echo.
echo   Tester maintenant:
echo   python "%PYTHON_SCRIPT%"
echo.
echo   Voir la tâche programmée:
echo   schtasks /query /tn "FCPalestina_NightlyUpdate"
echo.
echo   Exécuter la tâche manuellement:
echo   schtasks /run /tn "FCPalestina_NightlyUpdate"
echo.
echo   Supprimer la tâche:
echo   schtasks /delete /tn "FCPalestina_NightlyUpdate" /f
echo.
echo ===============================================

pause