@echo off
REM Script pour mettre à jour automatiquement les avis Vinted réels
REM À exécuter périodiquement (par exemple via le planificateur de tâches Windows)

echo ==============================================
echo    MISE A JOUR AUTOMATIQUE AVIS VINTED
echo ==============================================

REM Aller dans le dossier du projet
cd /d "c:\Users\linkl\Desktop\FCpalestina"

REM Activer l'environnement Python si nécessaire
echo [INFO] Démarrage de la mise à jour des avis...

REM Exécuter le script de mise à jour
python scripts\update_vinted_reviews.py

REM Vérifier le code de sortie
if %errorlevel% == 0 (
    echo [SUCCESS] Mise à jour terminée avec succès !
    echo [INFO] Vous pouvez maintenant actualiser votre site web
) else (
    echo [ERROR] Erreur lors de la mise à jour
    echo [INFO] Consultez les logs pour plus de détails
)

echo.
echo Appuyez sur une touche pour continuer...
pause > nul